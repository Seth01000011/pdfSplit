# pdfSplit

Splits PDF's according to top-level and secondary-level-based outlines, eg:
chapters and sections

# Initial setup

- set up virtual environment in current working directory with $ python3 -m venv ./
  - execute virtual environment with $ source ./bin/activate
    - when done splitting pdfs, exit venv with $ deactivate
  - pip install pymupdf

# Usage

- Set up environment per "Initial setup"
- run command $ python3 pdfSplitChapter.py [pdfname.pdf]
- pdf will be split and placed into "/split-pdf/" subdirectory
  in current working directory
