import random

import timelog

start_pos = []
current_pos = []
n = 0
queens_left = {i for i in range(n)}
queens_done = set()


def init_start_pos_v0_1(size: int):
    """最初のQのポジションを指定する
    v0.1 : 各行にランダムでQを置く"""
    global start_pos
    global current_pos
    global n
    n = size
    start_pos = [-1 for x in range(n)]
    for i in range(n):
        start_pos[i] = random.randrange(0, n)
    current_pos = start_pos


def init_start_pos_v0_2(size: int):
    """最初のQのポジションを指定する
    v0.2 : 各行にQを置く時点で conflict が少ないところに置く (random between ties)"""
    global start_pos
    global current_pos
    global n
    n = size
    start_pos = [-1 for x in range(n)]
    for r in range(n):
        # Move queen to a cell with min conflict (random between ties)
        new_col = fetch_col_with_min_conflict_in_row(start_pos, r)
        start_pos[r] = new_col
        # timelog.mid(f"init_start_pos_v0_2() : Placing new queen at {(r, new_col)}(row, col)")
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
    # Worst case : no queens -> no break -> check all rows : O(n)
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


def fetch_random_queen_in_conflict():
    """現在conflict中のQを探す : ランダムなQを見て、conflictがない限り別のQを検討"""
    random_queen_order = [x for x in range(n)]
    random.shuffle(random_queen_order)
    for queen_row in random_queen_order:
        queen_col = current_pos[queen_row]
        conflicts = calc_conflicts_for_cell(current_pos, queen_row, queen_col)
        if conflicts != 0:
            return queen_row
    return -1


# FIXME : Bottleneck
def fetch_col_with_min_conflict_in_row(positions, row):
    """ある行の中, min-conflict であるセルを返す"""
    # 行の全てのセルのconflict数を計算
    row_conflicts = calc_conflicts_for_row(positions, row)
    # その中のminのセルを選択 (同点ならランダム)
    min_conflict = min(row_conflicts)
    candidate_cols = [i for i, e in enumerate(row_conflicts) if e == min_conflict]
    new_col = random.choice(candidate_cols)
    return new_col


def step_choose_random():
    global current_pos
    timelog.mid("step_choose_random() : start")

    # Fetch a random queen in conflict
    # At the start, lots of conflicts, easy to find one, not too long
    # In the end, worst case O(n^2)
    queen_row = fetch_random_queen_in_conflict()
    if queen_row == -1:
        print("No queen in conflict found, no more conflicts?")
        return
    queen_col = current_pos[queen_row]
    # print(f"Random queen in conflict: {queen_col, queen_row} (col, row)")
    timelog.mid("step_choose_random() : after fetching a random queen in conflict")

    # Move the queen to the cell with the min-conflict in the row (random between ties)
    # O(n^2)
    new_col = fetch_col_with_min_conflict_in_row(current_pos, queen_row)
    timelog.mid("step_choose_random() : after fetching the min-conflict col in the row")

    current_pos[queen_row] = new_col
    timelog.mid("step_choose_random() : end")


def naive_min_conflict_no_backtrack():
    """v0.2 : min-conflict を利用して、ランダムでQを選ぶ
    v0.1 よりQの選び方、計算の数を減らしている、少しだけの改善
    var-left / var-done は実装なし、backtrackも利用していない"""
    max_steps = 10000
    s = 1
    found_solution = False

    while s < max_steps and found_solution is False:
        # Find if there is still a conflict : pick a queen and check until a conflict is found
        timelog.mid("naive_min_conflict_no_backtrack() : New while loop step")
        has_conflict = False
        for r in range(n):
            # O(n^2) : n * calc_conflicts_for_cell
            # Worst case (no conflict) for calc_conflicts_for_cell : O(n)
            c = current_pos[r]
            conflicts = calc_conflicts_for_cell(current_pos, r, c)
            if conflicts != 0:
                has_conflict = True
                break
        # If no more conflicts, then stop
        timelog.mid("naive_min_conflict_no_backtrack() : After finding if there is a queen conflict")
        if not has_conflict:
            print("DONE")
            # print(f"Final no conflict position: {current_pos}")
            found_solution = True
            print(f"Steps = {s}")
            return
        else:
            step_choose_random()
        # Increment step
        s += 1

