ROW_COUNT = 25
COL_COUNT = 25

CELL_SIZE = 4


def field_gen():
    field = {}
    for row in range(ROW_COUNT):
        for col in range(COL_COUNT):
            key = (row, col)
            field[key] = True

    yield field

    for sum_limit in range(0, COL_COUNT + ROW_COUNT - 2):
        for row in range(ROW_COUNT):
            for col in range(COL_COUNT):
                field[(row, col)] = (row + col) > sum_limit

        yield field


def get_polygon_data(field):
    # Формирование списка отрезков
    segments_set = set()
    for row in range(ROW_COUNT):
        for col in range(COL_COUNT):
            if not field[(row, col)]:
                continue

            # Верхняя граница ячейки
            if not field.get((row - 1, col), False):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = (col + 1) * CELL_SIZE
                y2 = row * CELL_SIZE
                segments_set.add(((x1, y1), (x2, y2)))

            # Правая граница ячейки
            if not field.get((row, col + 1), False):
                x1 = (col + 1) * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = (col + 1) * CELL_SIZE
                y2 = (row + 1) * CELL_SIZE
                segments_set.add(((x1, y1), (x2, y2)))

            # Нижняя граница ячейки
            if not field.get((row + 1, col), False):
                x1 = col * CELL_SIZE
                y1 = (row + 1) * CELL_SIZE
                x2 = (col + 1) * CELL_SIZE
                y2 = (row + 1) * CELL_SIZE
                segments_set.add(((x1, y1), (x2, y2)))

            # Левая граница ячейки
            if not field.get((row, col - 1), False):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = col * CELL_SIZE
                y2 = (row + 1) * CELL_SIZE
                segments_set.add(((x1, y1), (x2, y2)))

    # TODO Тестовый код. В дальнейшем - удалить
    # print('Количество сегментов:', len(segments_set), '\n')

    return []


def main():
    result = []
    for field in field_gen():

        # TODO Тестовый код. В дальнейшем - удалить
        # for r in range(ROW_COUNT):
        #     for c in range(COL_COUNT):
        #         print('X' if field[(r, c)] else '.', end='')
        #     print()

        polygon_data = get_polygon_data(field)
        result.append(polygon_data)

    # TODO Код записи на диск выходного JSON-файла


if __name__ == '__main__':
    main()
