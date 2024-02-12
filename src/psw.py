import secrets
import string


def generate_password(length=12, key='vagmr', chars=string.ascii_letters + string.digits + string.punctuation):
    password = key
    for i in range(length - len(key)):
        password += secrets.choice(chars)
    return password
