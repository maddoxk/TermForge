import glob
import sys
import re

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def check_alignments():
    golden_files = glob.glob("stories/**/*.golden.txt", recursive=True)
    failed = False

    for file_path in golden_files:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]
            
        # Check for right-side border alignment
        right_borders = []
        for i, line in enumerate(lines):
            plain = ansi_escape.sub('', line)
            # Find the position of the last border character
            if len(plain) > 0 and plain[-1] in ('│', '┐', '┘', '┤', '┐', '┘', '╣', '╗', '╝'):
                right_borders.append((i, len(plain)))
                
        if len(right_borders) > 1:
            target_col = right_borders[0][1]
            for i, col in right_borders:
                if col != target_col:
                    print(f"BORDER ALIGNMENT ERROR in {file_path}: Line {i+1} right border is at col {col}, expected {target_col}.")
                    print(f"Line content: '{lines[i]}'")
                    failed = True
                
    if failed:
        sys.exit(1)
    else:
        print("✅ All golden files passed strict alignment checks.")

if __name__ == "__main__":
    check_alignments()
