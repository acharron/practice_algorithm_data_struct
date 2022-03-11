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

    n_queen_solver = n_queen.NQueen(n)

    timelog.start()

    n_queen_solver.preprocess_starting_position()

    timelog.mid("Starting position created")

    # Solve
    timelog.IS_QUIET = True
    n_queen_solver.solve_min_conflict_hill_climbing_no_backtrack()
    timelog.end()


if __name__ == '__main__':
    # test_min_heap()
    # test_rod_cutting()
    test_n_queen()
    timelog.IS_QUIET = True
    # n_queen_solver = n_queen.NQueen(pow(10, 5))
    # cProfile.run('n_queen_solver.preprocess_starting_position()', sort="cumulative")
    # cProfile.run('n_queen_solver.solve_min_conflict_hill_climbing_no_backtrack()', sort="cumulative")
