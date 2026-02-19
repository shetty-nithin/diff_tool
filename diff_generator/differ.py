from .lcs import build_lcs_table
import collections
import re

def generate_diff_using_plain_lcs(A_norm, B_norm, A_raw, B_raw):
    dp = build_lcs_table(A_norm, B_norm)
    i, j = len(A_norm), len(B_norm)
    result = []

    while i > 0 and j > 0:
        #print(f"i = {i} and A[i-1] = {A[i-1]}")
        #print(f"j = {j} and B[j-1] = {B[j-1]}\n")
        if A_norm[i-1] == B_norm[j-1]:
            result.append(("equal", A_raw[i-1], B_raw[j-1]))
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            result.append(("delete", A_raw[i-1], None))
            i -= 1
        else:
            result.append(("insert", None, B_raw[j-1]))
            j -= 1

    while i > 0:
        result.append(("delete", A_raw[i-1], None))
        i -= 1

    while j > 0:
        result.append(("insert", None, B_raw[j-1]))
        j -= 1

    return result[::-1]

def generate_diff_using_myers_algorithm(file1_lines, file2_lines):
    line_to_id = {}
    id_to_line = []
    
    def normalize(line):
        return re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', '[TIME]', line.strip()).strip()

    vec1_norm = [normalize(l) for l in file1_lines]
    vec2_norm = [normalize(l) for l in file2_lines]

    def myers_diff(a_norm, b_norm, a_raw, b_raw):
        n, m = len(a_norm), len(b_norm)
        v = {1: 0}
        trace = []

        for d in range(n + m + 1):
            v_copy = v.copy()
            trace.append(v_copy)
            for k in range(-d, d + 1, 2):
                if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                    x = v[k + 1]
                else:
                    x = v[k - 1] + 1
                
                y = x - k
                while x < n and y < m and a_norm[x] == b_norm[y]:
                    x, y = x + 1, y + 1
                v[k] = x
                
                if x >= n and y >= m:
                    return backtrack(trace, a_raw, b_raw)

    def backtrack(trace, a_raw, b_raw):
        x, y = len(a_raw), len(b_raw)
        results = []

        for d in range(len(trace) - 1, -1, -1):
            v = trace[d]
            k = x - y

            if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                prev_k = k + 1
            else:
                prev_k = k - 1
            
            prev_x = v[prev_k]
            prev_y = prev_x - prev_k
            
            while x > prev_x and y > prev_y:
                results.append(('equal', a_raw[x-1], b_raw[y-1]))
                x, y = x - 1, y - 1
            
            if d > 0:
                if x > prev_x:
                    results.append(('delete', a_raw[x-1], None))
                elif y > prev_y:
                    results.append(('insert', None, b_raw[y-1]))

            x, y = prev_x, prev_y
            
        return results[::-1]

    return myers_diff(vec1_norm, vec2_norm, file1_lines, file2_lines)
