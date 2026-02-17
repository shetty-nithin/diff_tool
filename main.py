from utils.file_reader import read_file
from utils.normalize import normalize_line
from diff_generator.differ import generate_diff
from renderer.html_renderer import render_html 

def main():
    A_raw = read_file("input/A.txt")
    B_raw = read_file("input/B.txt")
    output = "output/diff.html"
    
    A_norm = [normalize_line(l) for l in A_raw]
    B_norm = [normalize_line(l) for l in B_raw]

    diff = generate_diff(A_norm, B_norm, A_raw, B_raw) 
    html = render_html(diff)

    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

    print("Diff generated successfully!")

if __name__ == "__main__":
    main()
