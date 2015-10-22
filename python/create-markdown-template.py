
import os
import sys
import stat

class MarkdownTemplate:

  def __init__(self):
    self.output_dir = os.getcwd()
    self.bibtex_name = "bib.bibtex"
    self.make_name = "make.sh"
    self.metadata_name = "metadata.yaml"

  def create(self, filename):
    markdown_name = filename + ".md"
    pdf_name = filename + ".pdf"

    self.create_markdown(markdown_name)
    self.create_bibtex()
    self.create_metadata()
    self.create_makefile(markdown_name, pdf_name)

  def create_markdown(self, markdown_name):
    open(self.output_dir + "/" + markdown_name, 'a').close()

  def create_bibtex(self):
    open(self.output_dir + "/" + self.bibtex_name, 'a').close()

  def create_metadata(self):
    meta_file = open(self.output_dir + "/" + self.metadata_name, "w")
    meta_file.write("---\n")
    meta_file.write("bibliography: {0}\n".format(self.bibtex_name))
    meta_file.write("---")
    meta_file.close()

  def create_makefile(self, markdown_name, pdf_name):
    make_file_location = self.output_dir + "/" + self.make_name
    # create make file
    make_file_output = \
      "pandoc " + \
      "--filter pandoc-citeproc " + \
      "--listings " + \
      "-V geometry:margin=1in " + \
      "-V documentclass:article " + \
      "-V secnumdepth:1 " + \
      "-o \"{0}\" {1} {2}".format(pdf_name, markdown_name, self.metadata_name)
    make_file = open(make_file_location, 'w')
    make_file.write(make_file_output)
    make_file.close()

    # finally, make it exectuable
    st = os.stat(make_file_location)
    os.chmod(make_file_location, st.st_mode | stat.S_IEXEC)

if __name__ == '__main__':
  try:
    filename = sys.argv[1]
    template = MarkdownTemplate()
    template.create(filename)
  except IndexError:
    print "Please provide a name for the Markdown template"
  