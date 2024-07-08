import pytest

from fixtures.responses import ResponseFactory
from models import User
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from schemas import JobInSchema, JobUpdateSchema, UserInSchema, UserUpdateSchema
from fastapi import status

@pytest.mark.asyncio
async def test_read_users(sa_session, client_app):

    all_users = await client_app.get('/users?limit=100&skip=0')
    assert all_users.status_code == status.HTTP_200_OK
    assert len(all_users.json()) == 1


@pytest.mark.asyncio
async def test_create_user(sa_session, client_app):
    user = UserInSchema(
        name="Uchpochmak",
        email="bashkort@example.com",
        password="eshkere!",
        password2="eshkere!",
        is_company=False
    )
    all_users = await client_app.post('/users', json=user.dict())
    assert all_users.status_code == status.HTTP_200_OK
    assert all_users.json()['email'] == user.email


@pytest.mark.asyncio
async def test_update_user(sa_session, client_app, current_user: User):
    sa_session.add(current_user)
    sa_session.flush()
    user = UserUpdateSchema(
        name="Саша",
        email=current_user.email,
        is_company=False
    )
    id = current_user.id
    all_users = await client_app.put(f'/users?id={id}', json=user.dict())
    assert all_users.status_code == status.HTTP_200_OK
    assert all_users.json()['name'] == "Саша"


@pytest.mark.asyncio
async def test_update_missed_user(sa_session, client_app, current_user: User):
    sa_session.add(current_user)
    sa_session.flush()
    user = UserUpdateSchema(
        name="Саша",
        email=current_user.email,
        is_company=False
    )
    id = current_user.id+1
    all_users = await client_app.put(f'/users?id={id}', json=user.dict())
    assert all_users.status_code == status.HTTP_404_NOT_FOUND
    assert all_users.json()['detail'] == "Пользователь не найден"


@pytest.mark.asyncio
async def test_update_person(sa_session, client_app, current_user: User):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()
    user = UserUpdateSchema(
        name="Саша",
        email=current_user.email,
        is_company=True
    )

    company = UserFactory.build()
    company.is_company = True
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.is_active = True
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    response_first = ResponseFactory.build()
    response_first.user_id = current_user.id
    response_first.job_id = job.id
    sa_session.add(response_first)
    sa_session.flush()

    id = current_user.id
    all_users = await client_app.put(f'/users?id={id}', json=user.dict())
    assert all_users.status_code == status.HTTP_403_FORBIDDEN
    assert all_users.json()['detail'] == "Удалите все свои отклики"


@pytest.mark.asyncio
async def test_update_company(sa_session, client_app, current_user: User):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()
    user = UserUpdateSchema(
        name="Саша",
        email=current_user.email,
        is_company=False
    )

    job = JobFactory.build()
    job.is_active = True
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()

    id = current_user.id
    all_users = await client_app.put(f'/users?id={id}', json=user.dict())
    assert all_users.status_code == status.HTTP_403_FORBIDDEN
    assert all_users.json()['detail'] == "Удалите все свои вакансии"
