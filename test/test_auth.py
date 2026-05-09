from fastapi import HTTPException
from ..router.auth import get_db, authenticate_user, SECRET_KEY, ALGORITHM, create_access_token, get_current_user
from .utils import *
from datetime import timedelta
from jose import jwt


app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, 'dattavenkat', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username
    authenticated_user = authenticate_user('wrongusername', 'dattavenkat', db)
    assert authenticated_user is False
    authenticated_user = authenticate_user(test_user.username, 'kkkm', db)
    assert authenticated_user is False





def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)
    decode_token = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM], options={'verfiy_signature': False})
    assert decode_token['sub'] == username
    assert decode_token['id'] == user_id
    assert decode_token['role'] == role



@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token=token)
    assert user == {'username': 'testuser', 'id': 1, 'user_role': 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate user'