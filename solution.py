from PIL import Image, ImageGrab
import numpy as np

black_color = [0, 0, 0, 255]


def process_cell(left_high_x, left_high_y, cell_len, cell_width, array) -> int:
    is_empty = True
    is_cross = array[left_high_x + cell_len // 2][left_high_y + cell_width // 2] == black_color
    for i in range(left_high_x + 1, left_high_x + cell_len - 1):
        for j in range(left_high_y + 1, left_high_y + cell_width - 1):
            if array[i][j] == black_color:
                is_empty = False
    if is_empty:
        return 0
    if is_cross:
        return 1
    return 2


if __name__ == '__main__':
    img = Image.open('image.png')
    np_arr = np.asarray(img, dtype='uint8')
    arr = np_arr.tolist()

    first_dim, second_dim, third_dim = np_arr.shape
    # Можем считать, что third_dim = 4 всегда

    # Выясняем толщину линий
    line_thickness = 0

    A_x = 0
    A_y = 0
    # Ищем координаты точки А
    for i in range(first_dim):
        for j in range(second_dim):
            if black_color == arr[i][j]:
                if line_thickness == 0:
                    A_y = j
                line_thickness += 1
            elif line_thickness > 0:
                break
        if line_thickness > 0:
            A_x = i
            break

    # Теперь выясним размеры девяти клеток, т.е. найдем длину и ширину
    # Для этого ищем координаты точки B
    B_x = 0
    B_y = A_y
    for i in range(A_x, first_dim):
        if black_color == arr[i][B_y - 1]:
            B_x = i
            break
    extreme_cell_length = B_x - A_x

    center_cell_length = 0
    for i in range(B_x + line_thickness, first_dim):
        if arr[i][B_y - 1] == black_color:
            break
        center_cell_length += 1
    # И координаты точки C
    C_x = A_x
    C_y = 0
    for j in range(A_y + line_thickness, second_dim):
        if black_color == arr[C_x][j]:
            C_y = j
            break

    center_cell_width = C_y - A_y - line_thickness - 1

    # И координаты точки D
    D_x = B_x
    D_y = 0
    for j in range(B_y, 0, -1):
        if black_color != arr[D_x][j]:
            D_y = j
            break
    extreme_cell_width = B_y - D_y - 1

    P_x = A_x
    P_y = A_y - extreme_cell_width

    offset_x = [0, extreme_cell_length + line_thickness, extreme_cell_length + center_cell_length + 2 * line_thickness]
    offset_y = [0, extreme_cell_width + line_thickness, extreme_cell_width + center_cell_width + 2 * line_thickness]

    cell_length = [extreme_cell_length, center_cell_length, extreme_cell_length]
    cell_width = [extreme_cell_width, center_cell_width, extreme_cell_width]

    field = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    for i in range(3):
        for j in range(3):
            field[i][j] = process_cell(P_x + offset_x[i], P_y + offset_y[j], cell_length[i], cell_width[j], arr)

    print(field)
    im = Image.fromarray(np.asarray(arr, dtype='uint8'))
    im.show()

