from docx import Document
from docx.shared import Inches
import os

def getAllInside(first,last,content):
    # returns a dict of keys first+value+last and the values
    valuesDict = {}
    for i in range(content.count(first)):
        try:
            f = content.index(first)
            l = content[f+len(first):].index(last)
            key = content[f:f+len(first)+l+len(last)]
            value = key.replace(first,'').replace(last,'')
        except ValueError:
            print('Error')
            continue
        valuesDict[key] = value
        content = content.replace(key,'')
    return valuesDict

class DocxExporter():
    def __init__(self,filename,docType):
        self.filename = filename
        self.document = Document()
        self.docType = docType

    def formatText(self,text):
        '''handle bold, italic, etc '''
        '''content = text
        if '<b>' in text:
            toBold = getAllInside('<b>','</b>',text)
            for bold in toBold:
                text = text.replace(bold,'\\textbf{'+toBold[bold]+'}')
            content = text
        if '<i>' in text:
            toItalicize = getAllInside('<i>','</i>',text)
            for italic in toItalicize:
                text = text.replace(italic,'\\textit{'+toItalicize[italic]+'}')
            content = text
        if '<code><pre>' in text: #multiline code
            codes = getAllInside('<code><pre>','</pre></code>',text)
            for code in codes:
                text = text.replace(code,'\\begin{lstlisting}\n'+codes[code]+'\n\end{lstlisting}')
            content = text
        if '<code>' in text: #inline code
            codes = getAllInside('<code>','</code>',text)
            for code in codes:
                text = text.replace(code,'\lstinline{'+codes[code]+'}')
            content = text
        return content'''
        if text:
            p = self.document.add_paragraph()
            textBuffer = ''
            italic = False
            bold = False
            for letter in text:
                textBuffer += letter
                if '<i>' in textBuffer:
                    runText = textBuffer.replace('<i>','')
                    r = p.add_run(runText)
                    r.italic = italic
                    r.bold = bold
                    textBuffer = ''
                    italic = True
                elif '</i>' in textBuffer:
                    runText = textBuffer.replace('</i>','')
                    r = p.add_run(runText)
                    r.italic = italic
                    r.bold = bold
                    textBuffer = ''
                    italic = False
                elif '<b>' in textBuffer:
                    runText = textBuffer.replace('<b>','')
                    r = p.add_run(runText)
                    r.italic = italic
                    r.bold = bold
                    textBuffer = ''
                    bold = True
                elif '</b>' in textBuffer:
                    runText = textBuffer.replace('</b>','')
                    r = p.add_run(runText)
                    r.italic = italic
                    r.bold = bold
                    textBuffer = ''
                    bold = False
            if textBuffer:
                p.add_run(textBuffer)

    def addText(self,text):
        self.formatText(text)

    def addHeading(self,title,level):
        formatedTitle = self.formatText(title)
        self.document.add_heading(formatedTitle,level=level)

    def addFigure(self,img,caption,source=None,label=None):
        pass

    def close(self):
        self.document.save(os.getcwd()+'/Archieves/'+self.filename+'.docx')


