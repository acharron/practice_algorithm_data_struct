import math
import random
import time
from collections import deque

import timelog


class NQueen:
    def __init__(self, n: int):
        self.n = n
        self.current_pos = [-1 for x in range(n)]
        self.queens_on_col = [0] * n
        self.queens_on_up_diag = [0] * (2 * n - 1)
        self.queens_on_down_diag = [0] * (2 * n - 1)

        self.queens_in_conflict = set()

        # Constant for queen placement (preprocess)
        self.TRIES_THRESH = 5 * math.floor(n / 10)  # ランダムでセルを試して、上限10回やってみる

    def preprocess_starting_position(self):
        number_non_optimal_cells = 0

        # ここが breakthrough! 「次試してみる col」 random_col の取得は昔
        #   random_col = random.randrange(0, self.n)
        # でやっていたが、かなりのボトルネックだった
        # deque を利用して「初期ポジションの時、一回利用した col をそもそも試さない (必ずコンフリクトがあるから)」の改善！
        random_cell_picker = list(range(self.n))
        random.shuffle(random_cell_picker)
        random_cell_picker = deque(random_cell_picker)

        # それぞれのrowに1個のクイーンを置く
        for r in range(self.n):
            tries = 0
            least_worst_col = -1  # 今まで見たセルの中で一番マシ
            least_worst_conflicts = 1000000  # ただ高い数字
            # 最悪の場合、conflictがないセルを探す回数は TRIES_THRESH 回までにする
            while tries < self.TRIES_THRESH:
                # ランダムでセルを選択して、conflict数を計算
                random_col = random_cell_picker.popleft()   # GOOD!!
                # random_col = random.randrange(0, self.n)  # Bad
                conflict = self.calc_conflicts_for_cell(r, random_col)
                if conflict == 0:
                    # conflictがないセルを見つけた！これでもう終了
                    least_worst_col = random_col
                    break
                elif conflict < least_worst_conflicts:
                    # 今まで見たcolよりconflicts数が少ないなら、「今まで一番まし」に保存する
                    least_worst_col = random_col
                    least_worst_conflicts = conflict
                if tries == self.TRIES_THRESH - 1:
                    # 諦める
                    number_non_optimal_cells += 1  # 諦めて合計で妥協したセルの数
                    self.event_move_queen_in_conflict_position(r, least_worst_col)
                random_cell_picker.append(random_col)  # 試してみたが、今回の r だとコンフリクトが起きてるので、 picker の尻尾に戻す (また今度別の r で試せる)
                tries += 1

            # ボードにクイーンを入れる
            self.current_pos[r] = least_worst_col
            self.add_queen(r, least_worst_col)

        print(f"Starting position done, {number_non_optimal_cells} cells with conflicts")

    def solve_min_conflict_hill_climbing_no_backtrack(self):
        max_steps = 10000
        s = 1
        found_solution = False

        start_time = time.process_time()

        # 課題を解く処理の開始
        while s < max_steps and found_solution is False:
            timelog.mid("solve_min_conflict_hill_climbing_no_backtrack() : New while loop step")
            # もし150秒以上かかってしまうなら、もう中断終了
            if time.process_time() - start_time > 150:
                print(f"Too long, spent more than 150s, aborting, at step {s}")
                break

            # conflictがまだあるか？
            has_conflict = self.check_if_still_has_conflicts()

            # もう conflict がない場合、正常終了
            if not has_conflict:
                found_solution = True
                print("DONE")
                print(f"Steps = {s}")
                return
            # else 次のステップ : クイーンを選択してポジションを直してみる
            else:
                self.step_hill_climbing()
            # ステップ数++
            s += 1

    def step_hill_climbing(self):
        # conflict中のクイーンを取得
        queen_row = self.fetch_random_queen_in_conflict()
        if queen_row == -1:
            print("No queen in conflict found, no more conflicts")
            return

        # クイーンのrowにもっともconflictが少ないセルを検索
        new_col = self.fetch_col_with_min_conflict_in_row(queen_row)

        # クイーンを移動
        cur_col = self.current_pos[queen_row]

        self.remove_queen(queen_row, cur_col)
        self.add_queen(queen_row, new_col)
        self.current_pos[queen_row] = new_col
        if self.calc_conflicts_for_cell(queen_row, new_col) > 0:
            self.event_move_queen_in_conflict_position(queen_row, new_col)

    def check_if_still_has_conflicts(self):
        if len(self.queens_in_conflict) > 0:
            return True
        else:
            print("check_if_still_has_conflicts() : queens_in_conflict set is empty, let's check all queens to be sure")

        has_conflict = False
        for r in range(self.n):
            c = self.current_pos[r]
            conflicts = self.calc_conflicts_for_cell(r, c)
            if conflicts != 0:
                has_conflict = True
                break
        print(f"check_if_still_has_conflicts() : After checking all cells, has_conflict = {has_conflict}")
        return has_conflict

    def calc_conflicts_for_cell(self, row, col):
        number_conflicts = 0
        if self.current_pos[row] == col:
            # ここにQがあるので、自分と conflict してしまうような扱いにならないように -3 を与える
            number_conflicts -= 3

        number_conflicts += self.queens_on_col[col]
        number_conflicts += self.queens_on_up_diag[row + col]
        number_conflicts += self.queens_on_down_diag[self.n - 1 + col - row]

        return number_conflicts

    def calc_conflicts_for_row(self, row):
        conflicts_in_row = [0] * self.n
        for col in range(0, self.n):
            number_conflicts = self.calc_conflicts_for_cell(row, col)
            conflicts_in_row[col] = number_conflicts
        return conflicts_in_row

    def fetch_col_with_min_conflict_in_row(self, row):
        """ある行の中, min-conflict であるセルを返す"""
        # 現在のrowの全てのセルのconflict数を計算
        row_conflicts = self.calc_conflicts_for_row(row)
        # その中のminのセルを選択 (同点ならランダム)
        min_conflict = min(row_conflicts)
        candidate_cols = [i for i, e in enumerate(row_conflicts) if e == min_conflict]
        new_col = random.choice(candidate_cols)
        return new_col

    def fetch_random_queen_in_conflict(self):
        """現在conflict中のQを探す : ランダムなQを見て、conflictがない限り別のQを検討"""
        # conflict中のクイーンのsetから試していく
        # だんだんpopしていくので最終的に全てがなくなるはず
        while len(self.queens_in_conflict) > 0:
            queen_row, queen_col = self.queens_in_conflict.pop()
            conflicts = self.calc_conflicts_for_cell(queen_row, queen_col)
            if conflicts != 0:
                return queen_row

        # In the last resort, we didn't find any queen in the set which was still in conflict
        # So let's try all the queens to find where there is still a conflict...
        print("No more queen in the queens_in_conflict set !")
        for queen_row in range(self.n):
            queen_col = self.current_pos[queen_row]
            conflicts = self.calc_conflicts_for_cell(queen_row, queen_col)
            if conflicts != 0:
                return queen_row
        # conflictとなっているクイーンを見つからない、もう終わり
        return -1

    def remove_queen(self, row, col):
        self.queens_on_col[col] -= 1
        self.queens_on_up_diag[row + col] -= 1
        self.queens_on_down_diag[self.n - 1 + col - row] -= 1

    def add_queen(self, row, col):
        self.queens_on_col[col] += 1
        self.queens_on_up_diag[row + col] += 1
        self.queens_on_down_diag[self.n - 1 + col - row] += 1

    def event_move_queen_in_conflict_position(self, row, col):
        """「今から置くクイーンは、どこかとconflictしているので、 queens_in_conflict を更新"""
        # 置くクイーン(Qa)を登録
        self.queens_in_conflict.add((row, col))
        # そのクイーン(Qa)がどことconflictしているかを探す
        # conflict しているクイーン(Qb, Qc, ...)も queens_in_conflict に登録
        # 同じカラムでconflictしているか？
        try:
            # Check if there is one on the same column
            # But don't count the current queen!
            # Remove the current queen temporarily, just for the column check
            self.current_pos[row] = -1
            has_same_col_queen_row = self.current_pos.index(col)
            self.queens_in_conflict.add((has_same_col_queen_row, col))
        except ValueError:
            # no queen on the same column
            pass
        self.current_pos[row] = col

        # Check for diag -i -i (top left)
        i = 1
        while (col - i) >= 0 and (row - i) >= 0:
            if self.current_pos[row - i] == col - i:
                self.queens_in_conflict.add((row - i, col - i))
                break
            i += 1

        # Check for diag -i +i (bottom left)
        i = 1
        while (col - i) >= 0 and (row + i) < self.n:
            if self.current_pos[row + i] == col - i:
                self.queens_in_conflict.add((row + i, col - i))
                break
            i += 1

        # Check for diag +i -i (top right)
        i = 1
        while (col + i) < self.n and (row - i) >= 0:
            if self.current_pos[row - i] == col + i:
                self.queens_in_conflict.add((row - i, col + i))
                break
            i += 1

        # Check for diag +i +i (bottom right)
        i = 1
        while (col + i) < self.n and (row + i) < self.n:
            if self.current_pos[row + i] == col + i:
                self.queens_in_conflict.add((row + i, col + i))
                break
            i += 1


