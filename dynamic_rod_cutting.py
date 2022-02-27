

prices = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 32]
buffer = [0]
optimal_cut = [0]


def find_max_revenue_rec(rod_length: int):
    if len(buffer) - 1 >= rod_length:
        return buffer[rod_length]
    max_revenue = 0
    for i in range(1, min(len(prices), rod_length + 1)):
        max_revenue = max(max_revenue, prices[i] + find_max_revenue_rec(rod_length - i))
    buffer.insert(rod_length, max_revenue)
    return max_revenue


def find_max_revenue(rod_length: int):
    for j in range(1, rod_length + 1):
        buf = 0
        optimal_cut.insert(j, 0)
        for i in range(1, min(len(prices), j+1)):
            if buf < prices[i] + buffer[j - i]:
                buf = prices[i] + buffer[j - i]
                optimal_cut[j] = i  # Stores the best first cut
        buffer.insert(j, buf)
    return buffer[rod_length]


def print_best_cuts(rod_length: int):
    if len(optimal_cut) < rod_length + 1:
        find_max_revenue(rod_length)  # Init the result and optimal cuts buffers

    res = f"Best cuts for {rod_length} is : "
    i = rod_length
    while i > 0:
        res += f"{optimal_cut[i]} "
        i = i - optimal_cut[i]
    print(res)

