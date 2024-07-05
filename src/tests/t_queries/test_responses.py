import pytest
from queries import user as user_query
from queries import jobs as jobs_query
from queries import responses as responses_query
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from schemas import UserInSchema
from schemas import JobInSchema
from schemas import ResponseSchema
from models import Response
from pydantic import ValidationError
from queries.utils import OrderBy, FilterBySalary, FilterByActiveness


@pytest.mark.asyncio
async def test_delete_some_responses(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    company = UserFactory.build()
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    response_first = ResponseFactory.build()
    response_first.user_id = user.id
    response_first.job_id = job.id
    sa_session.add(response_first)
    sa_session.flush()

    response_second = ResponseFactory.build()
    response_second.user_id = user.id
    response_second.job_id = job.id
    sa_session.add(response_second)
    sa_session.flush()

    response = [response_first, response_second]

    response_sample = await responses_query.delete_some_responses(sa_session, responses=response)
    response_search_first = await responses_query.get_response_by_id(sa_session, response_first.user_id)
    response_search_second = await responses_query.get_response_by_id(sa_session, response_second.user_id)
    assert response_sample
    assert len(response_sample) == 2
    assert response_search_first is None
    assert response_search_second is None


@pytest.mark.asyncio
async def test_get_response_by_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    company = UserFactory.build()
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    response = ResponseFactory.build()
    response.user_id = user.id
    response.job_id = job.id
    sa_session.add(response)
    sa_session.flush()

    id = response.id

    response_sample = await responses_query.get_response_by_id(sa_session, id)
    assert response_sample is not None
    assert response_sample.id == id


@pytest.mark.asyncio
async def test_get_response_by_job_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    company = UserFactory.build()
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    response = ResponseFactory.build()
    response.user_id = user.id
    response.job_id = job.id
    sa_session.add(response)
    sa_session.flush()

    id = job.id

    response_sample = await responses_query.get_response_by_job_id(sa_session, job_id=id)
    assert response_sample is not None
    assert response_sample[0].job_id == id


@pytest.mark.asyncio
async def test_get_response_by_user_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    company = UserFactory.build()
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    response = ResponseFactory.build()
    response.user_id = user.id
    response.job_id = job.id
    sa_session.add(response)
    sa_session.flush()

    response_first = await responses_query.get_response_by_user_id(sa_session, user_id=user.id, choice=1)
    response_second = await responses_query.get_response_by_user_id(sa_session, user_id=company.id, choice=0)
    assert response_first
    assert len(response_first) == 1
    assert response_first[0].user_id == user.id
    assert response_second
    assert len(response_second) == 1
    assert response_second[0].job.user_id == company.id


@pytest.mark.asyncio
async def test_response_job(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    company = UserFactory.build()
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    user_id = user.id
    job_id = job.id
    message = "Всегда об этом мечтал!"

    new_response = await responses_query.response_job(sa_session, user_id=user_id, job_id=job_id, message=message)
    assert new_response is not None
    assert new_response.user_id == user_id
    assert new_response.job_id == job_id
    assert new_response.message == "Всегда об этом мечтал!"


@pytest.mark.asyncio
async def test_update_job(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    company = UserFactory.build()
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    response = ResponseFactory.build()
    response.user_id = user.id
    response.job_id = job.id
    sa_session.add(response)
    sa_session.flush()

    response.message = "Обновлённый отклик"
    updated_response = await responses_query.update_response(sa_session, response=response)
    assert response.id == updated_response.id
    assert updated_response.message == "Обновлённый отклик"


@pytest.mark.asyncio
async def test_delete_response(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    company = UserFactory.build()
    sa_session.add(company)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = company.id
    sa_session.add(job)
    sa_session.flush()

    response = ResponseFactory.build()
    response.user_id = user.id
    response.job_id = job.id
    sa_session.add(response)
    sa_session.flush()

    id = response.id

    response_sample = await responses_query.delete_response(sa_session, response=response)
    response_search = await responses_query.get_response_by_id(sa_session, id)
    assert response_sample
    assert response_search is None
