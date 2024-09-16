def count_homonyms(surnames):
    surname_count = {}

    for surname in surnames:
        surname_count.setdefault(surname, 0)
        surname_count[surname] += 1

    total_homonyms = 0
    for count in surname_count.values():
        if count > 1:
            total_homonyms += count

    return total_homonyms

def main():
    n = int(input("Введите количество сотрудников: "))
    surnames = [input("Введите фамилию сотрудника: ").strip() for _ in range(n)]

    print(f"Количество однофамильцев: {count_homonyms(surnames)}")

if __name__ == "__main__":
    main()
