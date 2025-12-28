from typing import List
INTEGER_MAX = 1000000000

# Iteratif (Bottom-Up)
def coin_change_iterative(coins: List[int], n: int):
    k = len(coins)
    dp = [INTEGER_MAX] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        for j in range(k):
            if i - coins[j] >= 0:
                if dp[i - coins[j]] + 1 < dp[i]:
                   dp[i] = dp[i - coins[j]] + 1

    if dp[n] == INTEGER_MAX:
        return -1
    else:
        return dp[n]

# Rekursif (Top-Down)
def coin_change_recursive(coins: List[int], n: int):
    k = len(coins)
    dp = [-1] * (n + 1)

    return solve(coins, dp, k, n)

def solve(coins: List[int], dp: List[int], k: int, n: int):
    if n == 0:
        return 0
    elif n < 0:
        return INTEGER_MAX
    elif dp[n] != -1:
        return dp[n]
    
    dp[n] = INTEGER_MAX

    for i in range(k):
        sub = solve(coins, dp, k, n - coins[i])
        if sub + 1 < dp[n]:
            dp[n] = sub + 1

    if dp[n] >= INTEGER_MAX:
        return -1
    else:
        return dp[n]


# coba coab optimalisasi
# Iteratif
def coin_change_iterative_early(k, n):
    dp = [INTEGER_MAX] * (n + 1)
    dp[0] = 0

    for i in range(len(k)):
        coin = k[i]
        if coin <= n:
            dp[coin] = 1

    for amount in range(1, n + 1):
        for i in range(len(k)):
            coin = k[i]
            if amount - coin >= 0:
                if dp[amount - coin] + 1 < dp[amount]:
                    dp[amount] = dp[amount - coin] + 1

    if dp[n] >= INTEGER_MAX:
        return -1
    return dp[n]

# Rekursif
def coin_change_recursive_optimized(k, n):
    dp = [-1] * (n + 1)

    def solve(n):
        if n == 0:
            return 0
        elif n < 0:
            return INTEGER_MAX

        for i in range(len(k)):
            if k[i] == n:
                return 1

        if dp[n] != -1:
            return dp[n]

        min_result = INTEGER_MAX

        for i in range(len(k)):
            sub = solve(n - k[i])
            if sub + 1 < min_result:
                min_result = sub + 1

        dp[n] = min_result
        return min_result

    result = solve(n)

    if result >= INTEGER_MAX:
        return -1
    return result
