import pytest

from schemas import UserInSchema
from fastapi import status
from queries import user as user_query
from schemas import LoginSchema

@pytest.mark.asyncio
async def test_login(sa_session, client_app):
    user = UserInSchema(
        name="Uchpochmak",
        email="bashkort@example.com",
        password="eshkere!",
        password2="eshkere!",
        is_company=False
    )

    new_user = await user_query.create(sa_session, user_schema=user)
    sa_session.add(new_user)
    sa_session.flush()

    login = LoginSchema(
        email=user.email,
        password="eshkere!"
    )

    log_attempt = await client_app.post('/auth', json=login.dict())

    assert log_attempt.status_code == status.HTTP_200_OK
    assert log_attempt.json()['token_type'] == "Bearer"


@pytest.mark.asyncio
async def test_login_wrong_email(sa_session, client_app):
    user = UserInSchema(
        name="Uchpochmak",
        email="bashkort@example.com",
        password="eshkere!",
        password2="eshkere!",
        is_company=False
    )

    new_user = await user_query.create(sa_session, user_schema=user)
    sa_session.add(new_user)
    sa_session.flush()

    login = LoginSchema(
        email="cool" + user.email,
        password="eshkere!"
    )

    log_attempt = await client_app.post('/auth', json=login.dict())

    assert log_attempt.status_code == status.HTTP_401_UNAUTHORIZED
    assert log_attempt.json()['detail'] == "Некорректное имя пользователя или пароль"


@pytest.mark.asyncio
async def test_login_wrong_password(sa_session, client_app):
    user = UserInSchema(
        name="Uchpochmak",
        email="bashkort@example.com",
        password="eshkere!",
        password2="eshkere!",
        is_company=False
    )

    new_user = await user_query.create(sa_session, user_schema=user)
    sa_session.add(new_user)
    sa_session.flush()

    login = LoginSchema(
        email=user.email,
        password="sasha_eshkere!"
    )

    log_attempt = await client_app.post('/auth', json=login.dict())

    assert log_attempt.status_code == status.HTTP_401_UNAUTHORIZED
    assert log_attempt.json()['detail'] == "Некорректное имя пользователя или пароль"

