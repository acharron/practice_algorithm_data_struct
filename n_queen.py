import random
import time

import timelog

start_pos = []
current_pos = []
n = 0
queens_on_col = []
queens_on_up_diag = []
queens_on_down_diag = []
conflicts_in_row_buffer = []

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
    global queens_on_col
    global queens_on_up_diag
    global queens_on_down_diag
    global conflicts_in_row_buffer
    # Init global arrays
    n = size
    start_pos = [-1 for x in range(n)]
    queens_on_col = [0] * n
    queens_on_up_diag = [0] * (2 * n - 1)
    queens_on_down_diag = [0] * (2 * n - 1)
    conflicts_in_row_buffer = [0] * n

    # Place queens
    for r in range(n):
        # Move queen to a cell with min conflict (random between ties)
        new_col = fetch_col_with_min_conflict_in_row(start_pos, r)
        # Add queen on board
        start_pos[r] = new_col
        add_queen(r, new_col)
        # timelog.mid(f"init_start_pos_v0_2() : Placing new queen at {(r, new_col)}(row, col)")
    current_pos = start_pos


def init_start_pos_v0_4(size: int):
    """最初のQのポジションを指定する
    v0.4 : 'good enough min-conflict' : Don't check every col, just a sample T
    Pick at random a col, check if it has less than C conflicts
    If not, pick another random col and check
    If not, pick another random col and check, ... : max numbers of tries = T
    If at the last try (Tth try) we still don't have < C conflicts, just pick the min between all those tested so far"""

    global start_pos
    global current_pos
    global n
    global queens_on_col
    global queens_on_up_diag
    global queens_on_down_diag
    global conflicts_in_row_buffer
    # Init global arrays
    n = size
    start_pos = [-1 for x in range(n)]
    queens_on_col = [0] * n
    queens_on_up_diag = [0] * (2 * n - 1)
    queens_on_down_diag = [0] * (2 * n - 1)
    conflicts_in_row_buffer = [0] * n

    # Constants for queen placement
    CONFLICT_THRESH = 0  # できれば、置くセルが2つ以下のconflictになっている
    TRIES_THRESH = 100000  # ランダムでセルを試して、上限10回やってみる
    number_non_optimal_cells = 0

    # Place queens
    for r in range(n):
        new_col = -1
        tries = 0
        least_worst_col = -1
        least_worst_conflicts = 1000000  # infinity のような高い数字
        # Try at most T times
        while tries < TRIES_THRESH:
            # Pick a col at random, check if it has < C conflicts
            random_col = random.randrange(0, n)
            conflict = calc_conflicts_for_cell(start_pos, r, random_col)
            if conflict <= CONFLICT_THRESH:
                # Good enough col found! when can exit
                least_worst_col = random_col
                break
            elif conflict < least_worst_conflicts:
                # 今まで見たcolよりconflicts数が少ないなら、「今まで一番まし」に保存する
                least_worst_col = random_col
                least_worst_conflicts = conflict
            if tries == TRIES_THRESH - 1:
                number_non_optimal_cells += 1  # 諦めて妥協したセルの数
            tries += 1

        # Add queen on board
        start_pos[r] = least_worst_col
        add_queen(r, least_worst_col)
        # timelog.mid(f"init_start_pos_v0_2() : Placing new queen at {(r, new_col)}(row, col)")

    print(f"Starting position done, {number_non_optimal_cells} cells with conflicts")
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
    if positions[row] == col:
        # ここにQがあるので、自分と conflict してしまうような扱いにならないように -3 を与える
        number_conflicts -= 3

    number_conflicts += queens_on_col[col]
    number_conflicts += queens_on_up_diag[row + col]
    number_conflicts += queens_on_down_diag[n - 1 + col - row]

    return number_conflicts


def calc_conflicts_for_row(positions, row):
    global conflicts_in_row_buffer
    for col in range(0, n):
        number_conflicts = calc_conflicts_for_cell(positions, row, col)
        # Add to res
        conflicts_in_row_buffer[col] = number_conflicts
    return conflicts_in_row_buffer


all_tries = 0
all_time = 0


# FIXME : Bottleneck : When very few conflicts left, we have to check all queens -> O(n)
def fetch_random_queen_in_conflict():
    global all_tries
    global all_time
    """現在conflict中のQを探す : ランダムなQを見て、conflictがない限り別のQを検討"""
    start_time = time.process_time()
    s = 0
    random_queen_order = [x for x in range(n)]
    random.shuffle(random_queen_order)
    for queen_row in random_queen_order:
        queen_col = current_pos[queen_row]
        conflicts = calc_conflicts_for_cell(current_pos, queen_row, queen_col)
        if conflicts != 0:
            all_tries += s
            all_time += time.process_time() - start_time
            return queen_row
        s += 1
    return -1


# FIXME : Bottleneck : O(n^2)
def fetch_col_with_min_conflict_in_row(positions, row):
    """ある行の中, min-conflict であるセルを返す"""
    # 行の全てのセルのconflict数を計算
    row_conflicts = calc_conflicts_for_row(positions, row)
    # その中のminのセルを選択 (同点ならランダム)
    min_conflict = min(row_conflicts)
    candidate_cols = [i for i, e in enumerate(row_conflicts) if e == min_conflict]
    new_col = random.choice(candidate_cols)
    return new_col


def remove_queen(row, col):
    global queens_on_col
    global queens_on_up_diag
    global queens_on_down_diag
    queens_on_col[col] -= 1
    queens_on_up_diag[row + col] -= 1
    queens_on_down_diag[n - 1 + col - row] -= 1


def add_queen(row, col):
    global queens_on_col
    global queens_on_up_diag
    global queens_on_down_diag
    queens_on_col[col] += 1
    queens_on_up_diag[row + col] += 1
    queens_on_down_diag[n - 1 + col - row] += 1


def step_choose_random():
    global current_pos
    timelog.mid("step_choose_random() : start")

    # Fetch a random queen in conflict
    # At the start, lots of conflicts, easy to find one, not too long
    # In the end, worst case, check all queens to find the one without conflict
    queen_row = fetch_random_queen_in_conflict()
    if queen_row == -1:
        print("No queen in conflict found, no more conflicts?")
        return
    cur_col = current_pos[queen_row]
    # print(f"Random queen in conflict: {queen_col, queen_row} (col, row)")
    timelog.mid("step_choose_random() : after fetching a random queen in conflict")

    # Move the queen to the cell with the min-conflict in the row (random between ties)
    # O(n^2)
    new_col = fetch_col_with_min_conflict_in_row(current_pos, queen_row)
    timelog.mid("step_choose_random() : after fetching the min-conflict col in the row")

    # Move queen
    remove_queen(queen_row, cur_col)
    add_queen(queen_row, new_col)
    current_pos[queen_row] = new_col
    timelog.mid("step_choose_random() : end")


def naive_min_conflict_no_backtrack():
    """v0.2 : min-conflict を利用して、ランダムでQを選ぶ
    v0.1 よりQの選び方、計算の数を減らしている、少しだけの改善
    var-left / var-done は実装なし、backtrackも利用していない"""
    max_steps = 10000
    s = 1
    found_solution = False

    start_time = time.process_time()

    while s < max_steps and found_solution is False:
        # Safeguard against too long execution
        if time.process_time() - start_time > 150:
            print(f"Too long, spent more than 150s, at step {s}")
            break

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
            found_solution = True
            print(f"Steps = {s}")
            print(f"Finished the solve. Fetching a random queen in conflict "
                  f"took {all_tries} steps and {all_time:.4f} seconds")
            return
        else:
            step_choose_random()
        # Increment step
        s += 1
