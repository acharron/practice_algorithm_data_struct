import cProfile

import dynamic_rod_cutting
import n_queen
import timelog
from min_heap import MinHeap


def test_min_heap():
    heap = MinHeap()
    print(heap)
    heap.build_heap()
    print(f"{heap}  (Final heap)")
    heap.extract_min()
    heap.insert(2)


def test_rod_cutting():
    length = 8
    revenue = dynamic_rod_cutting.find_max_revenue(length)
    print(revenue)
    dynamic_rod_cutting.print_best_cuts(length)


def test_n_queen():
    n = pow(10, 6)
    # Make the starting position
    timelog.start()
    n_queen.init_start_pos_v0_4(n)
    timelog.mid("Starting position created")

    # Solve
    timelog.IS_QUIET = True
    # n_queen.util_print_board(n_queen.current_pos)
    n_queen.solve_min_conflict_hill_climbing_no_backtrack()
    # n_queen.util_print_board(n_queen.current_pos)
    timelog.end()


if __name__ == '__main__':
    # test_min_heap()
    # test_rod_cutting()
    test_n_queen()
    timelog.IS_QUIET = True
    # cProfile.run('n_queen.init_start_pos_v0_4(1000000)', sort="cumulative")
    # cProfile.run('n_queen.solve_min_conflict_hill_climbing_no_backtrack()', sort="cumulative")
