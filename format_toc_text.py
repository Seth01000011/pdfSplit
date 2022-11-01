from readline import insert_text
import sys
from pathlib import Path

with open(Path("./table_of_contents.txt"), "r") as inp:
  text = inp.read()
  # print(text)
  text = text.replace("], ","],\n")
  text = text.replace("\n\n","\n")
  print(text)
  with open("./toc_formatted.txt", "w") as fixed:
    fixed.write(text)
  with open("./toc_formatted.txt", "r") as toc_formatted:
    lines = toc_formatted.readlines()
    for each in lines:
      if ("[1") in each or ("[2") in each:
        with open("./removed_non_chapter_and_sections.txt", "a") as simplified:
          simplified.write(each)
