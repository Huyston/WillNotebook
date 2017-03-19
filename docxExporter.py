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

def getInside(first,last,content):
    f = content.index(first)
    l = content[f+len(first):].index(last)
    key = content[f:f+len(first)+l+len(last)]
    value = key.replace(first,'').replace(last,'')
    return value

class DocxExporter():
    def __init__(self,filename,docType):
        self.filename = filename
        self.document = Document()
        self.docType = docType
        self.figNumber = 1

    def formatText(self,text,p):
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
            textBuffer = ''
            italic = False
            bold = False
            for letter in text:
                textBuffer += letter
                textBuffer = textBuffer.replace('\n',' ')
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
                elif '</p>' in textBuffer:
                    print('entrou no ref')
                    ### This happens when a reference is written
                    ### Normally the reference is between </a> and </p>
                    reference = getInside('</a>','</p>',textBuffer).replace('&#x00A0;',' ').replace('&#8211;','-')
                    print(reference)
                    refBuffer = ''
                    p = self.document.add_paragraph()
                    for letter in reference:
                        refBuffer += letter
                        if 'class="ecti-1000">' in refBuffer:
                            initEmphasis = '<span'+getInside('<span','class="ecti-1000">',refBuffer)+'class="ecti-1000">'
                            runText = refBuffer.replace(initEmphasis,'')
                            r = p.add_run(runText)
                            r.italic = italic
                            r.bold = bold
                            refBuffer = ''
                            bold = True
                            print('Adding non bold')
                        elif '</span>' in refBuffer:
                            runText = refBuffer.replace('</span>','')
                            r = p.add_run(runText)
                            r.italic = italic
                            r.bold = bold
                            refBuffer = ''
                            bold = False
                            print('Adding bold')
                    if refBuffer:
                        p.add_run(refBuffer)
                    textBuffer = ''

            if textBuffer:
                p.add_run(textBuffer)

    def addText(self,text):
        p = self.document.add_paragraph()
        self.formatText(text,p)

    def addHeading(self,title,level,label):
        p = self.document.add_heading(level=level)
        self.formatText(title,p)

    def addFigure(self,img,caption,source='',label='',width='0.5'):

        cap = self.document.add_paragraph('Fig. '+str(self.figNumber)+': '+caption,'Caption')
        cap.alignment = 1
        para = self.document.add_paragraph()
        run = para.add_run()
        run.add_picture(os.getcwd()+'/Archieves/Images/'+img,width=int(float(width)*Inches(5.75)))
        para.alignment = 1
        sou = self.document.add_paragraph('Source: '+source,'Caption')
        sou.alignment = 1
        self.figNumber += 1
        self.document.add_paragraph() #pula linha

    def addTable(self,table,caption,label):
        cols = 0
        for row in table.split('\n'):
            rowCols = 0
            if '||' in row:
                rowCols = len(row.split('||'))
            elif '|' in row:
                rowCols = len(row.split('|'))
            if rowCols > cols:
                cols = rowCols

        docxTable = self.document.add_table(rows=1,cols=cols)
        for row in table.split('\n'):
            if '||' in row:
                headings = row.split('||')
                hCells = docxTable.add_row().cells
                for n,heading in enumerate(headings):
                    hCells[n].text = heading
            elif '|' in row:
                colText = row.split('|')
                hCells = docxTable.add_row().cells
                for n,text in enumerate(colText):
                    hCells[n].text = text

    def close(self):
        self.document.save(os.getcwd()+'/Archieves/'+self.filename+'.docx')


