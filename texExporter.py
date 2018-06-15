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
    def __init__(self,filename,docID,docType):
        self.docID = docID
        self.filename = filename
        self.document = open(os.getcwd()+'/Archieves/'+docID+'/'+filename+'.tex','w', encoding='utf8')
        self.docType = docType
        if docType == 'abntepusp':
            from shutil import copyfile
            copyfile(os.getcwd()+'/Modelos/abntepusp.cls',os.getcwd()+'/Archieves/'+docID+'/abntepusp.cls')
            self.options = 'a4paper,capchap,espacoduplo,normaltoc'
            self.addPackages = ['\\usepackage[alf,abnt-etal-list=0,abnt-repeated-author-omit=no]{abntex2cite}',]
        else:
            self.options = ''
            self.addPackages = []
        self.inBullet = False
        self.writePreamble()

    def writePreamble(self):
        self.document.write('''\\documentclass['''+self.options+''']{'''+self.docType+'''}
\\usepackage[T1]{fontenc} %font encoding setup
\\usepackage[utf8]{inputenc} %input encoding setup
\\usepackage{graphicx} %for displaying figures
\\usepackage{mathtools} %for displaying math
\\usepackage{listings} %for displaying code
\\usepackage[font=small]{caption}
''')

        for package in self.addPackages:
            self.document.write(package+'\n')

        self.document.write('''

\\setcounter{secnumdepth}{5} %for displaying numbers up to 5 levels
\\setcounter{tocdepth}{5} %for displaying numbers up to 5 levels in TOC

\\begin{document}

''')

    def formatText(self,text):
        '''handle bold, italic, etc '''
        content = text.replace('\\sec{','\\ref{').replace('\\fig{','\\ref{').replace('\\eq{','\\ref{').replace('\\tab{','\\ref{')
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

    def addText(self,text,output):
        if '!eq' in text:
            text = output
        formatedText = self.formatText(text)
        self.document.write(formatedText+'\n\n')

    def addHeading(self,title,level,label):
        section = {1:'\chapter{',2:'\section{',3:'\subsection{',4:'\subsubsection{',5:'\paragraph{',6:'\subparagraph'}
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
        citations = getAllInside('\cite{','}',source)
        for cite in citations:
            source = source.replace(cite,'\\protect'+cite)
        figure = '''\\begin{figure}[!h]
\centering
\caption{'''+caption+'''}
\includegraphics[width='''+width+'''\\textwidth]{Images/'''+img+'''}
\label{'''+label+'''}
\caption*{Source: '''+source+'''}
\end{figure}'''
        self.document.write(figure+'\n\n')

    def addTable(self,table,caption,label='',source=''):
        cols = 0
        for row in table.split('\n'):
            rowCols = 0
            if '||' in row:
                rowCols = len(row.split('||'))
            elif '|' in row:
                rowCols = len(row.split('|'))
            if rowCols > cols:
                cols = rowCols

        tableCode = '''\\begin{table}
\caption{'''+caption+'''}
\label{'''+label+'''}
\centering
\\begin{tabular}{'''+' c |'*(cols-1)+''' c }
'''

        for row in table.split('\n'):
            if '||' in row:
                headings = row.split('||')
                for heading in headings:
                    tableCode += heading + ' & '
                tableCode = tableCode[:-3]
                tableCode += '\\\\\n\hline\n'
            elif '|' in row:
                colText = row.split('|')
                for text in colText:
                    tableCode += text + ' & '
                tableCode = tableCode[:-3]
                tableCode += '\\\\\n'
        tableCode += '''\hline
\end{tabular}'''
        if source:
            tableCode += '''
\caption*{Source: '''+source+'''}
'''
        tableCode += '\end{table}'
        self.document.write(tableCode+'\n\n')

    def addTitle(self,title):
        if self.docType == 'abntepusp':
            titleCode = '\\titulo{'+title+'}\n'
        else:
            titleCode = '\\title{'+title+'}\n\\maketitle\n\n'
        self.document.write(titleCode)

    def addAuthor(self,author):
        if self.docType == 'abntepusp':
            names = author.split(' ')
            firstNames = ' '.join(names[:-1])
            lastName = names[-1]
            self.document.write('\\autorPoli{'+firstNames+'}{}{}{}{'+lastName+'}\n')

    def addAdvisor(self,advisor):
        if self.docType == 'abntepusp':
            self.document.write('\\orientador{'+advisor+'}\n')

    def addConcentrationArea(self,area):
        if self.docType == 'abntepusp':
            self.document.write('\\areaConcentracao{'+area+'}\n')

    def addDepartment(self,department):
        if self.docType == 'abntepusp':
            self.document.write('\\departamento{'+department+'}\n')

    def addModelType(self,modelType,area):
        if self.docType == 'abntepusp':
            self.document.write('\\'+modelType+'{'+area+'}\n')

    def addLocal(self,local):
        if self.docType == 'abntepusp':
            self.document.write('\\local{'+local+'}\n')

    def addDate(self,date):
        if self.docType == 'abntepusp':
            self.document.write('\\data{'+date+'}\n')

    def makeCover(self):
        if self.docType == 'abntepusp':
            self.document.write('\\capa{}\n\\folhaderosto{}\n\n')
            self.document.write('\\tableofcontents\n')
            self.document.write('\\listoffigures\n')
            self.document.write('\\listoftables\n\n')

    def addBullet(self,topic):
        topic = self.formatText(topic)
        self.document.close()
        self.document = open(os.getcwd()+'/Archieves/'+self.docID+'/'+self.filename+'.tex','r', encoding='utf8')
        backUp = self.document.readlines()
        self.document.close()
        self.document = open(os.getcwd()+'/Archieves/'+self.docID+'/'+self.filename+'.tex','w', encoding='utf8')
        if '\\end{itemize}' in backUp[-2]:
            del backUp[-1]
            backUp[-1] = '\\item '+topic+'\n'
            self.document.write(''.join(backUp))
            self.document.write('\\end{itemize}\n\n')
        else:
            self.document.write(''.join(backUp))
            self.document.write('\\begin{itemize}\n')
            self.document.write('\\item '+topic+'\n')
            self.document.write('\\end{itemize}\n\n')

    def addReferences(self,refs):
        self.document.write('\\newpage\n')
        self.document.write('\\bibliography{database}\n\n')

    def addAbstracts(self,title,content):
        content = content.replace('<br>','\n')
        content = content.replace('<h1 class="abstract">'+title+'</h1>','')
        title = title.lower()
        self.document.write('\\begin{'+title+'}\n\n')
        self.document.write(self.formatText(content.replace('!'+title,'')))
        self.document.write('\\end{'+title+'}\n\n')

    def close(self):
        self.document.write('\\end{document}')
        self.document.close()
