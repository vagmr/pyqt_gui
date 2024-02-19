from secrets import choice
from string import ascii_lowercase, digits, punctuation, ascii_uppercase
from random import randint, choices


def generate_password(length=16, key='vagmr', chars=ascii_uppercase):
    password_list = []
    letters_list = [choice(chars) for _ in range(randint(4, 8))]
    digits_list = [choice(digits)
                   for _ in range(3, 6)]
    punctuation_list = [choice(punctuation) for _ in range(
        length - len(letters_list) - len(digits_list))]
    length = randint(5, 10)
    key = choices(key+ascii_lowercase, k=length)
    password_list = letters_list + digits_list + punctuation_list + key
    password = ''.join(password_list)
    return password


if __name__ == '__main__':
    print(generate_password())
