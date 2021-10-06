ROW_COUNT = 25
COL_COUNT = 25

CELL_SIZE = 4


def field_gen():
    field = {}
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            key = (r, c)
            field[key] = True

    # TODO Код генерирования очередного состояния поля


def get_polygon_data(field):
    # TODO Код преобразования переданного состояния поля в список координат ломанной
    return []


def main():
    result = []
    for field in field_gen():
        polygon_data = get_polygon_data(field)
        result.append(polygon_data)

    # TODO Код записи на диск выходного JSON-файла


if __name__ == '__main__':
    main()
