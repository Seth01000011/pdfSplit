from pathlib import Path
import fitz
import os, sys

class PdfSplit:

  def __init__(self, input_pdf_path=sys.argv[1], dest_dir = "./split_pdfs/"):
    self.input_pdf_path = input_pdf_path
    with fitz.Document(input_pdf_path) as in_pdf:
      self.toc = in_pdf.get_toc()
      self.length = in_pdf.page_count
    self.current_page = 0
    self.last_page_written = 0
    self.dest_dir = dest_dir
    if not Path(self.dest_dir).exists():
      os.makedirs(self.dest_dir)

  def split_by_chapter_and_section(self):
    n = 0 # iterator for chapters
    y = 0 # iterator for subsections
    for section in self.toc:
      if section[0] == 1:
        subdir = self.dest_dir + f'{n:03}' + self.format_filenames(section[1])
        if not Path(subdir).exists():
          os.makedirs(subdir) 
        y = 0
        self.filename = subdir + "/" + f'{y:03}' + self.format_filenames(section[1]) + ".pdf"
        n = n + 1
        self.chapter_found = True
      if section[0] == 2:
        y = y + 1
        self.current_page = section[2] - 2
        self.write_out_pdf()
        self.filename = subdir + "/" + f'{y:03}' + self.format_filenames(section[1]) + ".pdf"
        self.last_page_written = self.current_page + 1
        self.last_section = True
    self.current_page = self.length
    self.write_out_pdf()


  def write_out_pdf(self):
    in_pdf = fitz.open(self.input_pdf_path)
    out_pdf = fitz.open()
    out_pdf = fitz.open()
    out_pdf.insert_pdf(in_pdf, from_page=self.last_page_written, to_page=self.current_page, \
      start_at=0, annots=False, show_progress=1)
    out_pdf.save(self.filename)
    out_pdf.close()
    in_pdf.close()



  def format_filenames(self, string):
    string = string.replace("/","_")
    string = string.replace(" ", "_")
    return string

pdf = PdfSplit()
pdf.split_by_chapter_and_section()

