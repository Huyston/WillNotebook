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

class TexExporter():
    def __init__(self,filename,docType):
        self.document = open(os.getcwd()+'/Archieves/'+filename+'.tex','w')
        self.docType = docType
        self.writePreamble()

    def writePreamble(self):
        self.document.write('''\\documentclass{'''+self.docType+'''}
\\usepackage[T1]{fontenc} %font encoding setup
\\usepackage[utf8]{inputenc} %input encoding setup
\\usepackage{graphicx} %for displaying figures
\\usepackage{mathtools} %for displaying math
\\usepackage{listings} %for displaying code

\\setcounter{secnumdepth}{5} %for displaying numbers up to 5 levels
\\setcounter{tocdepth}{5} %for displaying numbers up to 5 levels in TOC

\\begin{document}

''')

    def formatText(self,text):
        '''handle bold, italic, etc '''
        content = text.replace('\\sec{','\\ref{').replace('\\fig{','\\ref{').replace('\\eq{','\\ref{')
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
        return content

    def addText(self,text):
        formatedText = self.formatText(text)
        self.document.write(formatedText+'\n')

    def addHeading(self,title,level,label):
        section = {1:'\chapter{',2:'\section{',3:'\subsection{',4:'\subsubsection{',5:'\paragraph{'}
        formatedTitle = self.formatText(title)
        if self.docType == 'article':
            level += 1
        if label:
            end = '}\label{'+label+'}'
        else:
            end = '}'
        tex = section[level]+formatedTitle+end
        self.document.write(tex+'\n\n')

    def addFigure(self,img,caption,source='',label='',width='0.5'):
        figure = '''\\begin{figure}[!h]
\centering
\includegraphics[width='''+width+'''\\textwidth]{Images/'''+img+'''}
\label{'''+label+'''}
\caption{'''+caption+'''}
Source: '''+source+'''
\end{figure}'''
        self.document.write(figure+'\n\n')

    def close(self):
        self.document.write('\\end{document}')
        self.document.close()
        print('Ta aqu')

