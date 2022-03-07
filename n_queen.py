

start_pos = [1, 0, 4, 3, 1]


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


def calc_conflicts_for_row(positions, row):
    n = len(positions)
    res = []
    for col in range(0, n):
        number_conflicts = 0
        # Check for column conflict
        for r in range(0, row):
            if positions[r] == col:
                number_conflicts += 1
                break
        for r in range(row + 1, n):
            if positions[r] == col:
                number_conflicts += 1
                break
        # Check for diag -i -i (top left)
        i = 1
        while (col - i) >= 0 and (row - i) >= 0:
            if positions[row - i] == col - i:
                number_conflicts += 1
                break
            i += 1
        # Check for diag -i +i (bottom left)
        i = 1
        while (col - i) >= 0 and (row + i) < n:
            if positions[row + i] == col - i:
                number_conflicts += 1
                break
            i += 1
        # Check for diag +i -i (top right)
        i = 1
        while (col + i) < n and (row - i) >= 0:
            if positions[row - i] == col + i:
                number_conflicts += 1
                break
            i += 1
        # Check for diag +i +i (bottom right)
        i = 1
        while (col + i) < n and (row + i) < n:
            if positions[row + i] == col + i:
                number_conflicts += 1
                break
            i += 1
        # Add to res
        res.append(number_conflicts)
    return res

