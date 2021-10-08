import json

ROW_COUNT = 25
COL_COUNT = 25

CELL_SIZE = 4


def create_new_field():
    field = {}
    for row in range(ROW_COUNT):
        for col in range(COL_COUNT):
            key = (row, col)
            field[key] = True

    return field


def to_right_field_gen():
    field = create_new_field()
    yield field

    for sum_limit in range(0, COL_COUNT + ROW_COUNT - 2):
        for row in range(ROW_COUNT):
            for col in range(COL_COUNT):
                field[(row, col)] = (row + col) > sum_limit

        yield field


def to_left_field_gen():
    field = create_new_field()
    yield field

    for sum_limit in range(COL_COUNT + ROW_COUNT - 2, 0, -1):
        for row in range(ROW_COUNT):
            for col in range(COL_COUNT):
                field[(row, col)] = (row + col) < sum_limit

        yield field


def get_polygon_data(field):
    # Этап первый - Формирование множества отрезков
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

    # Этап второй - Упорядочивание множества отрезков в единый список точек
    segments_list = list(segments_set)
    point_a, point_b = segments_list.pop()
    point_list = [point_a, point_b]

    # Пока еще есть отрезки в исходном списке отрезков, продолжаем...
    while segments_list:
        next_segments_list = []

        for point_1, point_2 in segments_list:
            point_a, point_b = point_list[0], point_list[-1]

            if point_a == point_1:
                point_list = [point_2, *point_list]
                continue

            if point_a == point_2:
                point_list = [point_1, *point_list]
                continue

            if point_b == point_1:
                point_list = [*point_list, point_2]
                continue

            if point_b == point_2:
                point_list = [*point_list, point_1]
                continue

            next_segments_list.append((point_1, point_2))

        segments_list = next_segments_list

    # Усекаем последнюю - дублирующую - точку
    point_list = point_list[:-1]

    # Оптимизируем список точек, удаляя лишние точки
    tmp_point_list = []
    for index in range(len(point_list)):
        prev_index = index - 1 if index > 0 else len(point_list) - 1
        next_index = index + 1 if index < (len(point_list) - 1) else 0
        x1, y1 = point_list[prev_index]
        x2, y2 = point_list[next_index]
        dx, dy = x1 - x2, y1 - y2
        tmp_point_list.append((point_list[index], dx != 0 and dy != 0))

    point_list = [(value[0][0], value[0][1]) for value in filter(lambda value: value[1], tmp_point_list)]

    return point_list


def main():
    left_list = []
    for field in to_left_field_gen():
        polygon_data = get_polygon_data(field)
        left_list.append(polygon_data)

    right_list = []
    for field in to_right_field_gen():
        polygon_data = get_polygon_data(field)
        right_list.append(polygon_data)

    result = {
        'to_left': left_list,
        'to_right': right_list
    }

    with open('pattern.json', 'wt') as file:
        file.write(json.dumps(result, indent=2, sort_keys=False, ensure_ascii=False))


if __name__ == '__main__':
    main()
