import pytest
from queries import jobs as jobs_query
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from schemas import JobInSchema
from queries.utils import OrderBy, FilterBySalary, FilterByActiveness


@pytest.mark.asyncio
async def test_get_all_jobs(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    all_jobs = await jobs_query.get_all_jobs(sa_session, FilterBySalary.NO, FilterByActiveness.NO, OrderBy.NO, 100, 0, 0)
    assert all_jobs
    assert len(all_jobs) == 1
    assert all_jobs[0] == job

@pytest.mark.asyncio
async def test_get_jobs_by_salary(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    job.salary_from = 20000
    sa_session.add(job)
    sa_session.flush()

    all_jobs = await jobs_query.get_all_jobs(sa_session, FilterBySalary.MIN, FilterByActiveness.NO, OrderBy.NO, 100, 0, 20000)
    assert all_jobs
    assert len(all_jobs) == 1
    assert all_jobs[0] == job
    assert all_jobs[0].salary_from == 20000


@pytest.mark.asyncio
async def test_get_active_jobs(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    job.is_active = True
    sa_session.add(job)
    sa_session.flush()

    all_jobs = await jobs_query.get_all_jobs(sa_session, FilterBySalary.NO, FilterByActiveness.ACT, OrderBy.NO, 100, 0, 0)
    assert all_jobs
    assert len(all_jobs) == 1
    assert all_jobs[0] == job
    assert all_jobs[0].is_active == True

@pytest.mark.asyncio
async def test_get_job_by_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    id = job.id

    job_sample = await jobs_query.get_job_by_id(sa_session, id)
    assert job_sample is not None
    assert job_sample.id == id


@pytest.mark.asyncio
async def test_get_all_jobs_by_user_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    id = user.id

    job_sample = await jobs_query.get_all_jobs_by_user_id(sa_session, id, 100)
    assert job_sample
    assert len(job_sample) == 1
    assert job_sample[0].user_id == id


@pytest.mark.asyncio
async def test_create_job(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    job = JobInSchema(
        title="Охранник",
        description="Охрана кукурузы",
        salary_from=15000,
        salary_to=35000,
        is_active=True
    )

    id = user.id

    new_job = await jobs_query.create_job(sa_session, job_schema=job, user_id=id)
    assert new_job is not None
    assert new_job.user_id == id
    assert new_job.title == "Охранник"


@pytest.mark.asyncio
async def test_update_job(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    job.title = "Обновлённая работа"
    updated_job = await jobs_query.update(sa_session, job=job)
    assert job.id == updated_job.id
    assert updated_job.title == "Обновлённая работа"


@pytest.mark.asyncio
async def test_delete_job(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    id = job.id

    job_sample = await jobs_query.delete_job(sa_session, job=job)
    job_search = await jobs_query.get_job_by_id(sa_session, job_id=id)
    assert job_sample
    assert job_search is None
