

start_pos = [1, 0, 4, 3, 2]


def util_print_board(positions):
    n = len(positions)
    for row in range(0, n):
        res = ""
        for col in range(0, n):
            if positions[row] == col:
                res += "👑"
            elif (col + row) % 2 == 0:
                res += "⬛"
            else:
                res += "⬜"
        print(res)


