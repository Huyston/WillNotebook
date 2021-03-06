from texExporter import TexExporter
from subprocess import call
import os

class PdfLatexExporter(TexExporter):
    def close(self):
        self.document.write('\\end{document}')
        self.document.close()
        print('It is here')
        filename = os.path.basename(self.document.name).replace('.tex','')
        print('The filename is: ',filename)
        call(['pdflatex','-interaction=nonstopmode',filename+'.tex'], cwd=os.getcwd()+'/Archieves/'+self.docID)
        call(['bibtex',filename+'.aux'], cwd=os.getcwd()+'/Archieves/'+self.docID)
        call(['bibtex',filename+'.aux'], cwd=os.getcwd()+'/Archieves/'+self.docID)
        call(['pdflatex','-interaction=nonstopmode',filename+'.tex'], cwd=os.getcwd()+'/Archieves/'+self.docID)
        call(['pdflatex','-interaction=nonstopmode',filename+'.tex'], cwd=os.getcwd()+'/Archieves/'+self.docID)
