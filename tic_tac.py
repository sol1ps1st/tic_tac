ZERO_CHAR = "[O]"  # Нолик
CROSS_CHAR = "[X]"  # Крестик
# EMPTY_CHAR = chr(0x25AD)  # Пустая клетка
EMPTY_CHAR = "[ ]"  # Пустая клетка
YES_CHAR = 'y'  # Положительное подтверждение от пользователя
MAX_FIELD_SIZE = 99  # Максимальный размер поля (кол-во строк)


def show_position(state):
    if not state["end_game"]:
        print(
            "\nСейчас ход",
            "крестиком." if state["is_cross_step"] else "ноликом."
        )
    print("Текущее состояние:")
    pretty_filed = state["field"].copy()
    pretty_filed.insert(
        0,
        [""] + list(map(lambda n: str(n).center(3), range(1, state["size"] + 1)))
    )
    for i in range(1, size + 1):
        pretty_filed[i] = [str(i)] + pretty_filed[i]

    for row in pretty_filed:
        for v in row:
            print(f"{v:3s}", end="")
        print()


def is_win_or_draw(state):
    size = state["size"]
    field = state["field"]
    x_line = tuple(CROSS_CHAR for _ in range(size))
    o_line = tuple(ZERO_CHAR for _ in range(size))

    all_rows = [tuple(line) for line in field]  # Все строки на поле
    all_columns = list(zip(*field))  # Все столбцы на поле
    # Сформируем диагонали:
    main_diagonal = []  # Главная
    sec_diagonal = []  # Побочная
    for i in range(size):
        for j in range(size):
            if i == j:
                main_diagonal.append(field[i][j])
            if j + i == size - 1:
                sec_diagonal.append(field[i][j])
    all_lines = all_rows + all_columns + [tuple(main_diagonal)] + [tuple(sec_diagonal)]

    if x_line in all_lines or o_line in all_lines:
        print(
            "\nВыиграл игрок, ставивший", "нолики!" if state["is_cross_step"] else "крестики!\n"
        )
        state["end_game"] = True
        return True
    if len(["" for line in field if EMPTY_CHAR in line]) == 0:
        # Ничья, больше нет ходов
        print(
            "\nНичья.\n"
        )
        state["end_game"] = True
        return True
    return False


def init_field(size):
    return [[EMPTY_CHAR for _ in range(size)] for _ in range(size)]


def move(state, row, col):
    if 0 >= row > state["size"] or 0 >= col > state["size"]:
        print(f"Идекс строки и сталбца должен быть в диапазоне от 1 до {size}. Попробуйте еще!")
    if state["field"][row-1][col-1] != EMPTY_CHAR:
        print(f"Ячейка {row},{col} уже занята. Попробуйте еще!")
    else:
        state["field"][row-1][col-1] = CROSS_CHAR if state["is_cross_step"] else ZERO_CHAR
        state["is_cross_step"] = not state["is_cross_step"]


def read_move_coords(size):
    while True:
        print(
            "Укажите координаты вашего следующего",
            "крестика." if state["is_cross_step"] else "нолика."
        )
        try:
            row, col = tuple(
                map(
                    int,
                    input("Введите номер строки и столбца, разделенные пробелом: ").split()
                )
            )
            if not (0 < row <= size and 0 < col <= size):
                raise ValueError(f"Строка и столбец должны быть в интервале от 1 до {size} включительно.")
            return row, col
        except ValueError as e:
            print(f"{str(e)}")
            print("Попробуйте еще раз.")
        else:
            break


def read_size():
    while True:
        print(f"Введите размер поля от 1 до {MAX_FIELD_SIZE}: ")
        size = input().strip()
        if size.isdigit():
            size = int(size)
            if 0 < size <= MAX_FIELD_SIZE:
                return size
        print("Введенный размер некорректен.")


if __name__ == "__main__":
    first_game = True
    while True:
        print(
            "Хотите сыграть в",
            "новую" if not first_game else "",
            f"игру? ({YES_CHAR} - да, любой другой символ - нет)"
        )
        first_game = False
        if input().strip() != YES_CHAR:
            break
        size = read_size()
        state = {
            "field": init_field(size),
            "size": size,
            "is_cross_step": True,
            "end_game": False,
        }
        while not is_win_or_draw(state):
            show_position(state)
            row, col = read_move_coords(state["size"])
            move(state, row, col)
        show_position(state)
        print()
    print("Игра окончена. Вы восхитительны, приходите еще!")
