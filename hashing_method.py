import collections
from utils.file_reader import read_file

def get_diff(file1_lines, file2_lines):
    line_to_id = {}
    id_to_line = []
    
    def tokenize(lines):
        encoded = []
        for line in lines:
            line = line.rstrip() # Clean trailing whitespace
            if line not in line_to_id:
                line_to_id[line] = len(id_to_line)
                id_to_line.append(line)
            encoded.append(line_to_id[line])
        return encoded

    vec1 = tokenize(file1_lines)
    vec2 = tokenize(file2_lines)

    """
    CORE ALGORITHM: Myers Diff (Greedy Version)
    This finds the shortest path from (0,0) to (len1, len2) in an edit graph.
    """
    def myers_diff(a, b):
        n, m = len(a), len(b)
        v = {1: 0}
        trace = []

        for d in range(n + m + 1):
            v_copy = v.copy()
            trace.append(v_copy)
            for k in range(-d, d + 1, 2):
                if k == -d or (k != d and v[k - 1] < v[k + 1]):
                    x = v[k + 1]
                else:
                    x = v[k - 1] + 1
                
                y = x - k
                while x < n and y < m and a[x] == b[y]:
                    x, y = x + 1, y + 1
                v[k] = x
                
                if x >= n and y >= m:
                    return backtrack(trace, a, b)

    def backtrack(trace, a, b):
        x, y = len(a), len(b)
        results = []
        for d in range(len(trace) - 1, -1, -1):
            v = trace[d]
            k = x - y
            if k == -d or (k != d and v[k - 1] < v[k + 1]):
                prev_k = k + 1
            else:
                prev_k = k - 1
            
            prev_x = v[prev_k]
            prev_y = prev_x - prev_k
            
            while x > prev_x and y > prev_y:
                results.append(('equal', a[x-1]))
                x, y = x - 1, y - 1
            
            if d > 0:
                if x > prev_x:
                    results.append(('delete', a[x-1]))
                elif y > prev_y:
                    results.append(('insert', b[y-1]))
            x, y = prev_x, prev_y
            
        return results[::-1]

    # Run the algorithm
    diff_instructions = myers_diff(vec1, vec2)

    report = []
    for tag, line_id in diff_instructions:
        content = id_to_line[line_id]
        if tag == 'equal':
            report.append(f"  {content}")
        elif tag == 'delete':
            report.append(f"- {content}")
        elif tag == 'insert':
            report.append(f"+ {content}")
            
    return "\n".join(report)

# --- Test Case ---
log_v1 = read_file("input/A.txt")
log_v2 = read_file("input/B.txt")    

print("LOG DIFF REPORT:\n" + "="*20)
print(get_diff(log_v1, log_v2))
