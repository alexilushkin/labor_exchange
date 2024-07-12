import factory
from models import Job
from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)

    title = factory.Faker("job", locale="ru-RU")
    description = factory.Faker("paragraph", locale="ru-RU")
    salary_from = factory.Faker("pyint", min_value=10000, max_value=1000000)
    salary_to = factory.LazyAttribute(lambda f: f.salary_from + 10000)
    is_active = factory.Faker("pybool")
    created_at = factory.LazyFunction(datetime.utcnow)
