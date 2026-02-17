from .lcs import build_lcs_table

def generate_diff(A_norm, B_norm, A_raw, B_raw):
    dp = build_lcs_table(A_norm, B_norm)
    i, j = len(A_norm), len(B_norm)
    result = []

    while i > 0 and j > 0:
        #print(f"i = {i} and A[i-1] = {A[i-1]}")
        #print(f"j = {j} and B[j-1] = {B[j-1]}\n")
        if A_norm[i-1] == B_norm[j-1]:
            result.append(("equal", A_raw[i-1]))
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            result.append(("delete", A_raw[i-1]))
            i -= 1
        else:
            result.append(("insert", B_raw[j-1]))
            j -= 1

    while i > 0:
        result.append(("delete", A_raw[i-1]))
        i -= 1

    while j > 0:
        result.append(("insert", B_raw[j-1]))
        j -= 1

    return result[::-1]
