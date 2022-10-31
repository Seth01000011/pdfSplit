from pikepdf import Pdf, Page
from pathlib import Path
import fitz
import os, sys

# In some parts of the documentation we skip closing Pdf objects for brevity. In
# production code, you should open them in a with block or explicitly close them.

dest_dir = "./split_pdfs/"

if not Path(dest_dir).exists():
  os.makedirs(dest_dir)


def format_filenames(string):
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

def split_by_chapter_and_section(input_pdf):
  toc = []
  filename = ""
  next_filename = ""
  last_page_written = 0
  current_page = 0

  with fitz.Document(input_pdf) as in_pdf:
    toc = in_pdf.get_toc()
    # print(toc)
  n = 0 # iterator for chapters
  y = 0 # iterator for subsections
  for section in toc:
    if section[0] == 1:
      subdir = dest_dir + f'{n:03}' + format_filenames(section[1])
      if not Path(subdir).exists():
        os.makedirs(subdir)
      n = n + 1
      current_page = section[2]
      # need to insert something here, it skips right through this and includes
      # the next few pages of the next "chapter" in the previous "chapter's" last
      # out_pdf...

    if filename == "":
      filename = subdir + "/" + "0000TABLE_OF_CONTENTS.pdf"
      current_page = 1
    if section[0] == 2:
      next_filename = subdir + "/" + f'{y:03}' + format_filenames(section[1]) + ".pdf"
      # filename = subdir + "/" + f'{y:03}' + format_filenames(section[1]) + ".pdf"
      y = y + 1
      current_page = section[2]-2
      in_pdf = fitz.open(input_pdf)
      out_pdf = fitz.open()
      out_pdf.insert_pdf(in_pdf, from_page=last_page_written, to_page=current_page, \
        start_at=0, annots=False, show_progress=1)
      out_pdf.save(filename)
      out_pdf.close()
      in_pdf.close()
      filename = next_filename
      last_page_written = current_page + 1




  # with Pdf.open(input_pdf) as in_pdf:
  #   with in_pdf.open_outline() as outline:
  #     n = 0 # iterator for formatting subdir names based on chapter.title
  #     for chapter in outline.root:
  #       subdir = dest_dir + f'{n:03}' + format_filenames(chapter.title)
  #       if not Path(subdir).exists():
  #         os.makedirs(subdir)
  #       n = n + 1
  #       for section in chapter.children:
  #         out_pdf = Pdf.new()
  #         filename = subdir + format_filenames(section.title) + ".pdf"
  #         section_dest = section.destination
  #         # Page(direct_dest[section])


  #         if not Path(filename).exists():
  #           for pages in section.obj:
  #             out_pdf.pages.append(pages)
  #           out_pdf.save(filename)



    
      

######################
# uncomment the following to allow usage in terminal

# if len(sys.argv) < 2:
#   raise ValueError("Usage: Type path/filename.pdf for the pdf you want to split")

# if sys.argv[2] == "-p":
#   split_every_page(sys.argv[1])

# if sys.argv[2] == "-c":
#   split_by_chapter_and_section(sys.argv[1])

########################

split_by_chapter_and_section("outbackManual.pdf")