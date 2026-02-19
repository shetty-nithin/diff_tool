from utils.file_reader import read_file
from renderer.html_renderer import render_html
from diff_generator.differ import generate_diff_using_myers_algorithm

if __name__ == "__main__":
    output_path = "output/diff.html"
    
    try:
        log_v1 = read_file("input/a.txt")
        log_v2 = read_file("input/b.txt")
    except Exception as e:
        print(f"Error reading files: {e}")
        exit(1)

    diff_data = generate_diff_using_myers_algorithm(log_v1, log_v2)
    
    html_report = render_html(diff_data)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_report)

    print(f"Success! Difference report generated using hashing tricks and myers algorithm.")
