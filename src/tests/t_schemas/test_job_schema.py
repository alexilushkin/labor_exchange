import pytest

from fixtures.jobs import JobFactory
from queries import jobs as jobs_query
from fixtures.users import UserFactory
from schemas import JobInSchema, JobUpdateSchema
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_create_wrong_minimum_salary(sa_session):
    with pytest.raises(ValidationError):

        job = JobInSchema(
            title="Кассир",
            description="Сидение на кассе",
            salary_from=-10,
            salary_to=12000,
            is_active=True
        )


@pytest.mark.asyncio
async def test_create_wrong_maximum_salary(sa_session):
    with pytest.raises(ValidationError):

        job = JobInSchema(
            title="Менеджер",
            description="Менеджер по продажам",
            salary_from=100000,
            salary_to=50000,
            is_active=True
        )


@pytest.mark.asyncio
async def test_update_wrong_minimum_salary(sa_session):
    with pytest.raises(ValidationError):
        job = JobUpdateSchema(
            title="Кассир",
            description="Сидение на кассе",
            salary_from=-10,
            salary_to=12000,
            is_active=True
        )


@pytest.mark.asyncio
async def test_update_wrong_maximum_salary(sa_session):
    with pytest.raises(ValidationError):
        job = JobUpdateSchema(
            title="Менеджер",
            description="Менеджер по продажам",
            salary_from=100000,
            salary_to=50000,
            is_active=True
        )
