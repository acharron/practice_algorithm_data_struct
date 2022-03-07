import random

start_pos = []
current_pos = []
n = 0
queens_left = {i for i in range(n)}
queens_done = set()


def init_start_pos(size: int):
    global start_pos
    global current_pos
    global n
    n = size
    start_pos = [-1 for x in range(n)]
    for i in range(n):
        start_pos[i] = random.randrange(0, n)
    current_pos = start_pos


def util_print_board(positions):
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


def calc_conflicts_for_cell(positions, row, col):
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

    return number_conflicts


def calc_conflicts_for_row(positions, row):
    res = []
    for col in range(0, n):
        number_conflicts = calc_conflicts_for_cell(positions, row, col)
        # Add to res
        res.append(number_conflicts)
    return res


def step():
    global current_pos

    # Calculer le nombre de conflits pour chaque reine
    conflicts_for_each_queen = []
    for r in range(n):
        c = current_pos[r]
        conflicts = calc_conflicts_for_cell(current_pos, r, c)
        conflicts_for_each_queen.append(conflicts)
    # print(f"Current conflicts for each queen: {conflicts_for_each_queen}")
    # print(f"{max(conflicts_for_each_queen)}")

    # Prendre une reine qui est en conflit au hasard
    rows_with_queen_in_conflict = [i for i, e in enumerate(conflicts_for_each_queen) if e != 0]
    # print(f"Queens with conflicts: {rows_with_queen_in_conflict}")

    queen_row = random.choice(rows_with_queen_in_conflict)
    queen_col = current_pos[queen_row]
    # print(f"Random queen in conflict: {queen_col, queen_row} (col, row)")

    # La bouger sur une case avec le min-conflit dans sa row (au hasard si tie)
    row_conflicts = calc_conflicts_for_row(current_pos, queen_row)
    min_conflict = min(row_conflicts)
    candidate_cols = [i for i, e in enumerate(row_conflicts) if e == min_conflict]
    # print(f"Moving the queen into one of those cols: {candidate_cols}")
    new_col = random.choice(candidate_cols)
    # print(f"Moving to {(new_col, queen_row)}")

    current_pos[queen_row] = new_col


def naive_min_conflict_no_backtrack():
    max_steps = 10000
    s = 1
    found_solution = False

    while s < max_steps and found_solution is False:
        # Calculer le nombre de conflits pour chaque reine
        conflicts_for_each_queen = []
        for r in range(n):
            c = current_pos[r]
            conflicts = calc_conflicts_for_cell(current_pos, r, c)
            conflicts_for_each_queen.append(conflicts)
        # If no more conflicts, then stop
        if max(conflicts_for_each_queen) == 0:
            print(f"Final no conflict position: {current_pos}")
            found_solution = True
            print(f"Steps = {s}")
            # return "Done"
        else:
            step()
        # Increment step
        s += 1

