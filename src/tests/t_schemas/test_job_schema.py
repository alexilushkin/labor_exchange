import pytest
from queries import jobs as jobs_query
from fixtures.users import UserFactory
from schemas import JobInSchema
from pydantic import ValidationError
@pytest.mark.asyncio
async def test_create_wrong_minimum_salary(sa_session):
    with pytest.raises(ValidationError):
        user = UserFactory.build()
        sa_session.add(user)
        sa_session.flush()

        job = JobInSchema(
            title="Кассир",
            description="Сидение на кассе",
            salary_from=-10,
            salary_to=12000,
            is_active=True
        )

        id = user.id

        await jobs_query.create_job(sa_session, job_schema=job, user_id=id)


@pytest.mark.asyncio
async def test_create_wrong_maximum_salary(sa_session):
    with pytest.raises(ValidationError):
        user = UserFactory.build()
        sa_session.add(user)
        sa_session.flush()

        job = JobInSchema(
            title="Менеджер",
            description="Менеджер по продажам",
            salary_from=100000,
            salary_to=50000,
            is_active=True
        )

        id = user.id

        await jobs_query.create_job(sa_session, job_schema=job, user_id=id)