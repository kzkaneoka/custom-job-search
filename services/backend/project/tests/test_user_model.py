from project.tests.utils import add_user, recreate_db


def test_passwords_are_random(test_app):
    recreate_db()
    user_one = add_user("test_passwords_are_random1", "test_passwords_are_random1@test.com", "test_password")
    user_two = add_user("test_passwords_are_random2", "test_passwords_are_random2@test.com", "test_password")
    assert user_one.password != user_two.password

def test_encode_auth_token(test_app):
    user = add_user('test_encode_auth_token', 'test_encode_auth_token@test.com', 'test_password')
    auth_token = user.encode_auth_token(user.id)
    assert isinstance(auth_token, bytes)
