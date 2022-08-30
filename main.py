from solution import Solution


solution = Solution()

menu = 'Номера действий:\n' \
       '1 - Извлечь реплики с приветствием – где менеджер поздоровался\n' \
       '2 - Извлечь реплики, где менеджер представил себя\n' \
       '3 - Извлечь название менеджера\n' \
       '0 - Завершить работу\n' \
       'Введите номер действия: '

while True:
    x = input(menu)

    if not x.isnumeric():
        raise Exception('Введенное значение не число, досрочное завершение программы')

    x = int(x)

    if x == 0:
        break
    elif x == 1:
        data = solution.get_greeting_phrases()
        print(data.head(15))
    elif x == 2:
        data = solution.get_introduced_himself()
        print(data.head(15))
    elif x == 3:
        names_managers = solution.get_names_managers()
        print(names_managers)

