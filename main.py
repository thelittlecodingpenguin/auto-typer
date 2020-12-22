import time
import highlight

def main():
  for file_name in ("main.py", "highlight.py", "lexer.py"): # opens the files and prints them
    with open(file_name, 'r') as f:
      code = f.read(); print("File: " + file_name)
      skip_pos, highlights = highlight.highlight(highlight.parse(code))

      i = 0

      while i < len(highlights):
        c = highlights[i]
        print(c, end='', flush=True); time.sleep(0.05)
        i += 1

main()
