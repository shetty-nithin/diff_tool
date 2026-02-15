from .lcs import build_lcs_table

def generate_diff(A, B):
    dp = build_lcs_table(A, B)
    i, j = len(A), len(B)
    result = []

    while i > 0 and j > 0:
        print(f"i = {i} and A[i-1] = {A[i-1]}")
        print(f"j = {j} and B[j-1] = {B[j-1]}\n")
        if A[i-1] == B[i-1]:
            result.append(("equal", A[i-1]))
            i -= 1
            j -= 1
        elif dp[i-1][j] >= dp[i][j-1]:
            result.append(("delete", A[i-1]))
            i -= 1
        else:
            result.append(("insert", B[j-1]))
            j -= 1

    while i > 0:
        result.append(("delete", A[i-1]))
        i -= 1

    while j > 0:
        result.append(("insert", B[j-1]))
        j -= 1

    print(result)
    return result[::-1]
