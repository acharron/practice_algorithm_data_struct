import dynamic_rod_cutting
import n_queen
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
    n_queen.util_print_board(n_queen.start_pos)
    print(n_queen.calc_conflicts_for_row(n_queen.start_pos, 1))


if __name__ == '__main__':
    # test_min_heap()
    # test_rod_cutting()
    test_n_queen()

