import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def main():
    print("================== HASHING PASSWORD ===================")
    s = input('Введите свой пароль: ')
    password = hash_password(s)
    print('Ваш хешированный пароль:', password)
    print("=======================================================")


if __name__ == "__main__":
    main()