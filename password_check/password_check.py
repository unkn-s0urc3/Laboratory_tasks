digits = set("0123456789")
special_chars = set("!@#$%^&*(),.?\":{}|<>")
upper_case = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
lower_case = set("abcdefghijklmnopqrstuvwxyz")

def password_check(password):
    password_set = set(password)

    if len(password) < 8:
        print("Пароль должен содержать не менее 8 символов.")
        return False
    if not password_set & digits:
        print("Пароль должен содержать хотя бы одну цифру.")
        return False
    if not password_set & special_chars:
        print("Пароль должен содержать хотя бы один специальный символ (!@#$%^&*(),.?\":{}|<> и др.).")
        return False
    if not password_set & upper_case:
        print("Пароль должен содержать хотя бы одну букву в верхнем регистре.")
        return False
    if not password_set & lower_case:
        print("Пароль должен содержать хотя бы одну букву в нижнем регистре.")
        return False
    return True


def main():
    while True:
        password = input("Введите пароль: ")
        if password_check(password):
            print(f"Ваш пароль '{password}' соответствует всем требованиям безопасности!")
            break


if __name__ == "__main__":
    main()