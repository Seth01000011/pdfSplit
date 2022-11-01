from pathlib import Path
import fitz
import os, sys

# In some parts of the documentation we skip closing Pdf objects for brevity. In
# production code, you should open them in a with block or explicitly close them.

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
    # with fitz.Document(self.input_pdf_path) as in_pdf:
    n = 0 # iterator for chapters
    y = 0 # iterator for subsections
    for section in self.toc:
      ###########################
      # need to find a way to make everything written the "current"?
      # everything in the last iteration is skipped since it hits the 'end'
      # and solving that will probably solve the issue of the beginning of the
      # next 'chapter' being put in the end of the last chapter...
      ###########################
      if section[0] == 1:
        subdir = self.dest_dir + f'{n:03}' + self.format_filenames(section[1])
        if not Path(subdir).exists():
          os.makedirs(subdir) 
        y = 0
        self.filename = subdir + "/" + f'{y:03}' + self.format_filenames(section[1]) + ".pdf"
        n = n + 1
        # self.current_page = section[2]
        # if self.next_filename == "":
        #   self.next_filename = subdir + "/" + "0000TABLE_OF_CONTENTS.pdf"
        #   self.current_page = section[2]
        self.chapter_found = True
        ####################################
        # need to insert something here, it skips right through this and includes
        # the next few pages of the next "chapter" in the previous "chapter's" last
        # out_pdf...
        
        # gotta fix self.next_filename being ""..
        # really want to force the next if statement to run!?
        # somehow need to make next_filename make sense... 


        ####################################

      if section[0] == 2:
        # self.filename = self.next_filename
        # self.next_filename = subdir + "/" + f'{y:03}' + self.format_filenames(section[1]) + ".pdf"
        
        # filename = subdir + "/" + f'{y:03}' + format_filenames(section[1]) + ".pdf"
        y = y + 1
        self.current_page = section[2] - 2
        self.write_out_pdf()
        self.filename = subdir + "/" + f'{y:03}' + self.format_filenames(section[1]) + ".pdf"
        self.last_page_written = self.current_page + 1
        self.last_section = True
    self.current_page = self.length
    self.write_out_pdf()


  def write_out_pdf(self):
    # reference_pdf = fitz.open(self.input_pdf_path)
    in_pdf = fitz.open(self.input_pdf_path)
    out_pdf = fitz.open()
    out_pdf = fitz.open()
    out_pdf.insert_pdf(in_pdf, from_page=self.last_page_written, to_page=self.current_page, \
      start_at=0, annots=False, show_progress=1)
    out_pdf.save(self.filename)
    out_pdf.close()
    in_pdf.close()
    # self.filename = self.next_filename



  def format_filenames(self, string):
    string = string.replace("/","_")
    string = string.replace(" ", "_")
    return string

# splits pdf into individual pages
def split_every_page(input_pdf):
  with Pdf.open(input_pdf) as in_pdf:
    for n, page in enumerate(in_pdf.pages):
      out_pdf = Pdf.new()
      out_pdf.pages.append(page)
      out_pdf.save(f'./split_pdfs/page{n:02d}.pdf')

pdf = PdfSplit()
pdf.split_by_chapter_and_section()

######################
# uncomment the following to allow usage in terminal
# this is old... but I should reimplement it when I get this working

# if len(sys.argv) < 2:
#   raise ValueError("Usage: Type path/filename.pdf for the pdf you want to split")

# if sys.argv[2] == "-p":
#   split_every_page(sys.argv[1])

# if sys.argv[2] == "-c":
#   split_by_chapter_and_section(sys.argv[1])

########################

