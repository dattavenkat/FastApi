from fastapi import status
from ..router.Users import get_db, get_current_user
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user




def test_get_user(test_user):
    response = client.get("/Users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['email'] == 'datta@gmail.com'
    assert response.json()['username'] == 'codingwithruby'



def test_put_item(test_user):
    response = client.put("/Users/todo", json={"password": "dattavenkat",
                                               "new_password": "venkat_kumar"})
    assert response.status_code == status.HTTP_204_NO_CONTENT



def test_not_put_item(test_user):
    response = client.put("/Users/todo", json={"password": "datta_venkat",
                                               "new_password": "venkat_kumar"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}


def test_phone_number(test_user):
    response = client.put("/Users/phone_number",  params={"passer": "88888883"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    assert model.phone_number == '88888883'







