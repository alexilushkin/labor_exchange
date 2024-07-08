import pytest

from models import User
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from schemas import JobInSchema, JobUpdateSchema
from fastapi import status


@pytest.mark.asyncio
async def test_read_jobs(sa_session, client_app):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    all_jobs = await client_app.get('/jobs?filter_by_salary=%D0%9E%D1%82%D1%81%D1%83%D1%82%D1%81%D1%82%D0%B2%D1%83%D0%B5%D1%82&filter_by_activeness=%D0%9E%D1%82%D1%81%D1%83%D1%82%D1%81%D1%82%D0%B2%D1%83%D0%B5%D1%82&order_by=%D0%9E%D1%82%D1%81%D1%83%D1%82%D1%81%D1%82%D0%B2%D1%83%D0%B5%D1%82&limit=100&skip=0&salary=0')
    assert all_jobs.status_code == status.HTTP_200_OK
    assert len(all_jobs.json()) == 1
    assert all_jobs.json()[0]['title'] == job.title


@pytest.mark.asyncio
async def test_read_my_jobs(sa_session, client_app, current_user: User):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()

    id = current_user.id

    all_jobs = await client_app.get(f'/jobs/{id}')

    assert all_jobs.status_code == status.HTTP_200_OK
    assert len(all_jobs.json()) == 1
    assert all_jobs.json()[0]['title'] == job.title


@pytest.mark.asyncio
async def test_read_missed_jobs(sa_session, client_app, current_user: User):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()

    id = current_user.id

    all_jobs = await client_app.get(f'/jobs/{id+1}')

    assert all_jobs.status_code == status.HTTP_404_NOT_FOUND
    assert all_jobs.json()['detail'] == "Пользователь не найден"


@pytest.mark.asyncio
async def test_read_wrong_jobs(sa_session, client_app, current_user: User):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()

    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    id = user.id

    all_jobs = await client_app.get(f'/jobs/{id}')

    assert all_jobs.status_code == status.HTTP_404_NOT_FOUND
    assert all_jobs.json()['detail'] == "Пользователь не найден"


@pytest.mark.asyncio
async def test_read_jobs_for_users(sa_session, client_app, current_user: User):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    id = current_user.id

    all_jobs = await client_app.get(f'/jobs/{id}')

    assert all_jobs.status_code == status.HTTP_403_FORBIDDEN
    assert all_jobs.json()['detail'] == "Вы соискатель. Вакансии создаются компаниями"


@pytest.mark.asyncio
async def test_create_job(sa_session, client_app, current_user: User):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    new_job = JobInSchema(
        title="Охранник",
        description="Охрана кукурузы",
        salary_from=15000,
        salary_to=35000,
        is_active=True
    )

    all_jobs = await client_app.post('/jobs', json=new_job.dict())

    assert all_jobs.status_code == status.HTTP_200_OK
    assert all_jobs.json()['title'] == "Охранник"


@pytest.mark.asyncio
async def test_create_job_for_users(sa_session, client_app, current_user: User):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    new_job = JobInSchema(
        title="Охранник",
        description="Охрана кукурузы",
        salary_from=15000,
        salary_to=35000,
        is_active=True
    )

    all_jobs = await client_app.post('/jobs', json=new_job.dict())

    assert all_jobs.status_code == status.HTTP_403_FORBIDDEN
    assert all_jobs.json()['detail'] == "Вы соискатель. Вакансии создаются компаниями"


@pytest.mark.asyncio
async def test_update_job(sa_session, client_app, current_user: User):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()

    new_job = JobUpdateSchema(
        title="Охранник",
        description="Охрана кукурузы",
        salary_from=15000,
        salary_to=35000,
        is_active=True
    )

    id = job.id

    all_jobs = await client_app.put(f'/jobs?id={id}', json=new_job.dict())

    assert all_jobs.status_code == status.HTTP_200_OK
    assert all_jobs.json()['title'] == "Охранник"


@pytest.mark.asyncio
async def test_update_missed_job(sa_session, client_app, current_user: User):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()

    new_job = JobUpdateSchema(
        title="Охранник",
        description="Охрана кукурузы",
        salary_from=15000,
        salary_to=35000,
        is_active=True
    )

    id = job.id+1

    all_jobs = await client_app.put(f'/jobs?id={id}', json=new_job.dict())

    assert all_jobs.status_code == status.HTTP_404_NOT_FOUND
    assert all_jobs.json()['detail'] == "Вакансия не найдена"


@pytest.mark.asyncio
async def test_update_foreign_job(sa_session, client_app, current_user: User):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    new_job = JobUpdateSchema(
        title="Охранник",
        description="Охрана кукурузы",
        salary_from=15000,
        salary_to=35000,
        is_active=True
    )

    id = job.id

    all_jobs = await client_app.put(f'/jobs?id={id}', json=new_job.dict())

    assert all_jobs.status_code == status.HTTP_404_NOT_FOUND
    assert all_jobs.json()['detail'] == "Это не ваша вакансия"


@pytest.mark.asyncio
async def test_delete_job(sa_session, client_app, current_user: User):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()

    id = job.id

    all_jobs = await client_app.delete(f'/jobs?id={id}')

    assert all_jobs.status_code == status.HTTP_200_OK
    assert all_jobs.json()['title'] == job.title


@pytest.mark.asyncio
async def test_delete_missed_job(sa_session, client_app, current_user: User):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()

    id = job.id

    await client_app.delete(f'/jobs?id={id}')
    all_jobs = await client_app.delete(f'/jobs?id={id}')

    assert all_jobs.status_code == status.HTTP_404_NOT_FOUND
    assert all_jobs.json()['detail'] == "Вакансия не найдена"


@pytest.mark.asyncio
async def test_delete_foreign_job(sa_session, client_app, current_user: User):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    id = job.id

    await client_app.delete(f'/jobs?id={id}')
    all_jobs = await client_app.delete(f'/jobs?id={id}')

    assert all_jobs.status_code == status.HTTP_404_NOT_FOUND
    assert all_jobs.json()['detail'] == "Это не ваша вакансия"
