from utils.file_reader import read_file
from diff_generator.differ import generate_diff
from renderer.html_renderer import render_html 

def main():
    A = read_file("input/A.txt")
    B = read_file("input/B.txt")
    output = "output/diff.html"

    diff = generate_diff(A, B) 
    html = render_html(diff)

    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

    print("Diff generated successfully!")

if __name__ == "__main__":
    main()
