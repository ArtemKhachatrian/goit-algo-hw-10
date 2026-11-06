import timeit

COINS = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount, coins=COINS):
    result = {}
    for coin in sorted(coins, reverse=True):
        if amount >= coin:
            count, amount = divmod(amount, coin)
            result[coin] = count
    return result


def find_min_coins(amount, coins=COINS):
    INF = float("inf")
    min_coins = [0] + [INF] * amount
    last_coin = [0] * (amount + 1)

    for s in range(1, amount + 1):
        for coin in coins:
            if coin <= s and min_coins[s - coin] + 1 < min_coins[s]:
                min_coins[s] = min_coins[s - coin] + 1
                last_coin[s] = coin

    if min_coins[amount] == INF:
        return {}

    result = {}
    while amount > 0:
        coin = last_coin[amount]
        result[coin] = result.get(coin, 0) + 1
        amount -= coin
    return dict(sorted(result.items()))


def benchmark():
    for amount in [113, 1_000, 10_000, 100_000, 1_000_000]:
        n = 200 if amount <= 10_000 else 1
        g = timeit.timeit(lambda: find_coins_greedy(amount), number=n) / n
        d = timeit.timeit(lambda: find_min_coins(amount), number=n) / n
        same = sum(find_coins_greedy(amount).values()) == sum(find_min_coins(amount).values())
        print(f"{amount:>9} | greedy {g*1000:10.5f} ms | dp {d*1000:12.3f} ms | same count: {same}")


if __name__ == "__main__":
    print(find_coins_greedy(113))
    print(find_min_coins(113))    
    benchmark()