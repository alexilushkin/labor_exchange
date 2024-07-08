import pytest

from models import User
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from schemas import JobInSchema, JobUpdateSchema, ResponseSchema, ResponseUpdateSchema
from fastapi import status


@pytest.mark.asyncio
async def test_read_all_my_responses_for_users(sa_session, client_app, current_user: User):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    company = UserFactory.build()
    company.is_company = True
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    response_first = ResponseFactory.build()
    response_first.user_id = current_user.id
    response_first.job_id = job.id
    sa_session.add(response_first)
    sa_session.flush()

    all_responses = await client_app.get('/responses')

    assert all_responses.status_code == status.HTTP_200_OK
    assert len(all_responses.json()) == 1
    assert all_responses.json()[0]['message'] == response_first.message


@pytest.mark.asyncio
async def test_read_all_my_responses_for_company(sa_session, client_app, current_user: User):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    user = UserFactory.build()
    user.is_company = False
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()

    response_first = ResponseFactory.build()
    response_first.user_id = user.id
    response_first.job_id = job.id
    sa_session.add(response_first)
    sa_session.flush()

    all_responses = await client_app.get('/responses')

    assert all_responses.status_code == status.HTTP_200_OK
    assert len(all_responses.json()) == 1
    assert all_responses.json()[0]['message'] == response_first.message


@pytest.mark.asyncio
async def test_response_job(sa_session, client_app, current_user: User):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    company = UserFactory.build()
    company.is_company = True
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.is_active = True
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    job_id = job.id
    message = "Класс, всегда об этом мечтал"

    all_responses = await client_app.post(f'/responses?job_id={job_id}&message={message}')

    assert all_responses.status_code == status.HTTP_200_OK
    assert all_responses.json()['message'] == message

@pytest.mark.asyncio
async def test_response_job_for_company(sa_session, client_app, current_user: User):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    company = UserFactory.build()
    company.is_company = True
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.is_active = True
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    job_id = job.id
    message = "Класс, всегда об этом мечтал"

    all_responses = await client_app.post(f'/responses?job_id={job_id}&message={message}')

    assert all_responses.status_code == status.HTTP_403_FORBIDDEN
    assert all_responses.json()['detail'] == "Вы работодатель. На вакансии откликаются соискатели"

@pytest.mark.asyncio
async def test_response_inactive_job(sa_session, client_app, current_user: User):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    company = UserFactory.build()
    company.is_company = True
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.is_active = False
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    job_id = job.id
    message = "Класс, всегда об этом мечтал"

    all_responses = await client_app.post(f'/responses?job_id={job_id}&message={message}')

    assert all_responses.status_code == status.HTTP_403_FORBIDDEN
    assert all_responses.json()['detail'] == "Вакансия не является активной"


@pytest.mark.asyncio
async def test_response_missed_job(sa_session, client_app, current_user: User):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    job_id = 1
    message = "Класс, всегда об этом мечтал"

    all_responses = await client_app.post(f'/responses?job_id={job_id}&message={message}')

    assert all_responses.status_code == status.HTTP_404_NOT_FOUND
    assert all_responses.json()['detail'] == "Работа не найдена"


@pytest.mark.asyncio
async def test_update_response(sa_session, client_app, current_user: User):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

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

    updated_response = ResponseUpdateSchema(
        job_id=job.id,
        message="Класс, всегда об этом мечтал"
    )
    id = response_first.id

    all_responses = await client_app.put(f'/responses?id={id}', json=updated_response.dict())

    assert all_responses.status_code == status.HTTP_200_OK
    assert all_responses.json()['message'] == "Класс, всегда об этом мечтал"


@pytest.mark.asyncio
async def test_update_missed_response(sa_session, client_app, current_user: User):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

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

    updated_response = ResponseUpdateSchema(
        message="Класс, всегда об этом мечтал"
    )
    id = response_first.id

    all_responses = await client_app.put(f'/responses?id={id+1}', json=updated_response.dict())

    assert all_responses.status_code == status.HTTP_404_NOT_FOUND
    assert all_responses.json()['detail'] == "Отклик не найден"


@pytest.mark.asyncio
async def test_update_foreign_response(sa_session, client_app, current_user: User):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

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
    response_first.user_id = current_user.id+1
    response_first.job_id = job.id
    sa_session.add(response_first)
    sa_session.flush()

    updated_response = ResponseUpdateSchema(
        message="Класс, всегда об этом мечтал"
    )
    id = response_first.id

    all_responses = await client_app.put(f'/responses?id={id}', json=updated_response.dict())

    assert all_responses.status_code == status.HTTP_404_NOT_FOUND
    assert all_responses.json()['detail'] == "Это не ваш отклик"


@pytest.mark.asyncio
async def test_delete_response(sa_session, client_app, current_user: User):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    company = UserFactory.build()
    company.is_company = True
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    response_first = ResponseFactory.build()
    response_first.user_id = current_user.id
    response_first.job_id = job.id
    sa_session.add(response_first)
    sa_session.flush()

    id = response_first.id

    all_responses = await client_app.delete(f'/responses?id={id}')

    assert all_responses.status_code == status.HTTP_200_OK
    assert all_responses.json()['message'] == response_first.message


@pytest.mark.asyncio
async def test_delete_missed_response(sa_session, client_app, current_user: User):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    company = UserFactory.build()
    company.is_company = True
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    response_first = ResponseFactory.build()
    response_first.user_id = current_user.id
    response_first.job_id = job.id
    sa_session.add(response_first)
    sa_session.flush()

    id = response_first.id

    await client_app.delete(f'/responses?id={id}')
    all_responses = await client_app.delete(f'/responses?id={id}')

    assert all_responses.status_code == status.HTTP_404_NOT_FOUND
    assert all_responses.json()['detail'] == "Отклик не найден"

@pytest.mark.asyncio
async def test_delete_foreign_response(sa_session, client_app, current_user: User):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    company = UserFactory.build()
    company.is_company = True
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    response_first = ResponseFactory.build()
    response_first.user_id = current_user.id+1
    response_first.job_id = job.id
    sa_session.add(response_first)
    sa_session.flush()

    id = response_first.id

    all_responses = await client_app.delete(f'/responses?id={id}')

    assert all_responses.status_code == status.HTTP_404_NOT_FOUND
    assert all_responses.json()['detail'] == "Это не ваш отклик"

