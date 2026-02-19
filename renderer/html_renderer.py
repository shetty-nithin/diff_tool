from utils.escape import escape_html

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Custom Diff Viewer</title>
<style>
body {{
    font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica;
    background: #f6f8fa;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    background: white;
}}
td {{
    padding: 6px 10px;
    vertical-align: top;
    font-size: 14px;
}}
.ln {{
    width: 50px;
    text-align: right;
    color: #6a737d;
    background: #f6f8fa;
}}
.code {{
    font-family: monospace;
    white-space: pre-wrap;
}}
tr.delete {{ background: #ffeef0; }}
tr.insert {{ background: #e6ffed; }}
tr.equal {{ background: white; }}
</style>
</head>
<body>

<h2>Custom Diff Viewer</h2>

<table>
{rows}
</table>

</body>
</html>
"""

def render_html(diff):
    rows = []
    left_ln = right_ln = 1

    for tag, left_text, right_text in diff:
        left_escaped = escape_html(left_text.rstrip("\n")) if left_text else ""
        right_escaped = escape_html(right_text.rstrip("\n")) if right_text else ""

        if tag == "equal":
            rows.append(row("equal", left_ln, right_ln, left_escaped, right_escaped))
            left_ln += 1
            right_ln += 1

        elif tag == "delete":
            rows.append(row("delete", left_ln, "", left_escaped, ""))
            left_ln += 1

        elif tag == "insert":
            rows.append(row("insert", "", right_ln, "", right_escaped))
            right_ln += 1

    return HTML_TEMPLATE.format(rows="\n".join(rows))


def row(cls, lno, rno, left, right):
    left_display = left if left.strip() != "" else "&nbsp;"
    right_display = right if right.strip() != "" else "&nbsp;"
    return f"""
<tr class="{cls}">
    <td class="ln">{lno}</td>
    <td class="code">{left_display}</td>
    <td class="ln">{rno}</td>
    <td class="code">{right_display}</td>
</tr>
"""
