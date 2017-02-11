import cherrypy
import random
from cherrypy.lib.static import serve_file
import os
from io import StringIO
from subprocess import call
import sys
import dill as pickle
#import pickle

try:
    from sympy import latex
except:
    print('No sympy installed')

def section(text):
    '''This is a test notebook python function'''
    print("<h1>"+text+"</h1>")

def genRandomStr(length):
    chars = 'qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
    randomStr = ''.join(random.choice(chars) for i in range(length))
    return randomStr

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

def startWith(text,content):
    return content.replace('\n','').replace(' ','')[:len(text)] == text

def emptyLine(content):
    if content.replace('\n','').replace(' ','') == '':
        return True
    else:
        return False

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        print(self)
        sys.stdout = self._stdout
	  
class WillNotebook(object):
    emptyLineSymbol = '.'
    archive = {}
    references = {}
    @cherrypy.expose
    def index(self):
        docID= genRandomStr(8)
        while docID in self.archive:
            docID = genRandomStr(8)
        notebook = open('notebook.html','r')
        notebook = notebook.read().replace('!@docID@!',docID)
        #The globals can be used to perform Python default functions for WillNotebook
        #It is ignored in the save state, so only locals is saved in the document
        self.archive[docID] = {'Globals':{'section':section},'Locals':{},'page':[],'references':None}
        self.references[docID] = {'keys':{},'counts':{},'References':'','refCell':''}
        return notebook

    @cherrypy.expose
    def newCell(self,docID,index):
        print('New cell called')
        self.archive[docID]['page'].insert(int(index),{'content':'','output':'.'})
        return 'Cell inserted'

    @cherrypy.expose
    def deleteCell(self,docID,index):
        index = int(index)
        print('Delete cell called')
        print('Index: ',index)
        content = self.archive[docID]['page'][index]['content']
        if 'type' in content:
            if content['type'] == 'image':
                filename = content['img']
                os.remove(os.getcwd()+'/Archieves/Images/'+filename)
        if startWith('!ref',content):
            print('Deleting the refCell')
            self.references[docID]['refCell'] = ''
        changedRefs = False
        if '\cite{' in content:
            citations = getAllInside('\cite{','}',content)
            for citation in citations:
                print('Citation deletion: ', citation)
                self.references[docID]['counts'][citation] -= content.count(citation)
                print(self.references[docID]['counts'][citation])
                if self.references[docID]['counts'][citation] == 0:
                    del self.references[docID]['counts'][citation]
                    del self.references[docID]['keys'][citation]
                    changedRefs = True
                    print('Citation removed')
        refUpdate = ''
        if changedRefs:
            self.makeReferences(docID)
            if self.references[docID]['refCell']:
                refUpdate = '!@StartRef@!cell="'+str(self.references[docID]['refCell'])+'"'+self.handleReferences(docID)+'!@EndRef@!'
        self.archive[docID]['page'].pop(int(index))
        print('This is the update: ',refUpdate)
        return refUpdate+'Cell deleted'

    @cherrypy.expose
    def evalCell(self,docID,cell,content):
        cell = int(cell)
        print(cell)
        changedCitations = False
        if cell == len(self.archive[docID]['page']):
            self.archive[docID]['page'].append({'content':content,'output':'.'})
        else:
            ### Existing cell ###
            ### Check if there was any citation and if it changed ###
            citations = getAllInside('\cite{','}',content)
            print('citations: ',citations)
            if not citations:
                if 'citations' in self.archive[docID]['page'][cell]:
                    changedCitations = True
                    for citation in self.archive[docID]['page'][cell]['citations']:
                        n = self.archive[docID]['page'][cell]['citations'][citation]
                        self.references[docID]['counts'][citation] -= n
                        print('Citation '+citation+' was removed from content')
                        if self.references[docID]['counts'][citation] == 0:
                            del self.references[docID]['counts'][citation]
                            del self.references[docID]['keys'][citation]
                            print('No more citation '+citation+' in document. Deleting...')
                    del self.archive[docID]['page'][cell]['citations']
            else:
                if 'citations' in self.archive[docID]['page'][cell]:
                    cellCitations = [i for i in self.archive[docID]['page'][cell]['citations'].keys()]
                    for citation in cellCitations:
                        if not citation in citations:
                            print('Removing citation from counters')
                            self.references[docID]['counts'][citation] -= self.archive[docID]['page'][cell]['citations'][citation]
                            if self.references[docID]['counts'][citation] == 0:
                                changedCitations = True
                                del self.archive[docID]['page'][cell]['citations'][citation]
                                del self.references[docID]['counts'][citation]
                                del self.references[docID]['keys'][citation]
                        else:
                            print('Updating citation counters')
                            oldN = self.archive[docID]['page'][cell]['citations'][citation]
                            self.references[docID]['counts'][citation] -= oldN
        refUpdate = ''
        if changedCitations:
            if self.references[docID]['refCell']:
                self.makeReferences(docID)
                refUpdate = '!@StartRef@!cell="'+str(self.references[docID]['refCell'])+'"'+self.handleReferences(docID)+'!@EndRef@!'
        self.archive[docID]['page'][cell]['content'] = content
        if startWith('#code',content):
            output = self.handlePythonCode(docID,content)
            ## {{}} soh nao sera avaliado em #code
        else:
            if '{{' in content and '}}' in content:
                content = self.handleValues(docID,content)
            ## Order is important here, first the ***
            if '***' in content:
                print('BoldItalic parts')
                content = self.handleBoldItalics(content)
            if '**' in content:
                print('Bold parts')
                content = self.handleBold(content)
            if '*' in content:
                print('Italic parts')
                content = self.handleItalics(content)
            if '\cite{' in content and '}' in content:
                content = self.handleCitations(docID,cell,content)
            if startWith('!#',content):
                output = self.handleSections(content)
            elif startWith('!eq',content):
                output = self.handleEquations(content)
            elif startWith('!title',content):
                output = self.handleTitle(content)
            elif startWith('!ref',content):
                output = self.handleReferences(docID,cell=cell)
            else:
                output = content
        if emptyLine(output):
            output = self.emptyLineSymbol
        if not '!@StartRef@!' in content[:12]:
            print('Modified citations and there is no citations in content')
            output = refUpdate+output
        ## Store output without the ref updater tags ##
        if '!@StartRef@!' in output:
            print('output with ref: ',output)
            refContent = getInside('!@StartRef@!','!@EndRef@!',output)
            storeOutput = output.replace(refContent,'')
            storeOutput = storeOutput.replace('!@StartRef@!','')
            storeOutput = storeOutput.replace('!@EndRef@!','')
            self.archive[docID]['page'][cell]['output'] = storeOutput
        else:
            self.archive[docID]['page'][cell]['output'] = output
        print('References now: ',self.references[docID]['References'])
        ## Update refcell content ##
        if self.references[docID]['refCell']:
            for n in range(len(self.archive[docID]['page'])):
                if self.archive[docID]['page'][n]['content'] == '!ref':
                    refCell = n
            self.references[docID]['serverRefCell'] = refCell
            self.archive[docID]['page'][refCell]['output'] = '<h1>References</h1>\n'+self.references[docID]['References']
        return output

    def handlePythonCode(self,docID,content):
        with Capturing() as output:
            try:
                exec(content,self.archive[docID]['Globals'],self.archive[docID]['Locals'])
            except Exception as e:
                print('Exception: ', e)
        if output == []:
            label = ''
            for line in content.split('\n'):
                if '#code' in line:
                    label = line.replace('#code','')
                    break
            return '<font class="dontprint" color="green">[code]'+label+'</font>'
        else:
            # Retorna o primeiro indice da lista (str)
            return output[0]

    def handleValues(self,docID,content):
        toEvaluate = getAllInside('{{','}}',content)
        for expr in toEvaluate:
            try:
                out = eval(toEvaluate[expr],self.archive[docID]['Globals'],self.archive[docID]['Locals'])
                objType = str(type(out))
                if 'sympy' in objType or 'list' in objType and 'sympy' in str(type(out[0])):
                    print('Is a sympy object!')
                    try:
                        out = str(latex(out))
                        if not '!eq' in content:
                            out = '$'+out+'$'
                    except:
                        print('Latex error')
                        out = str(out)
                else: 
                    print('Not a sympy object! It it: ',objType)
                    out = str(out)
                content = content.replace(expr,out)
            except Exception as e:
                print('excep: ',e)
                content = 'Exception: '+str(e)
        return content

    def handleItalics(self,content):
        toItalicize = getAllInside('*','*', content)
        for expr in toItalicize:
            print('Italics :',expr)
            italic = '<i>'+toItalicize[expr]+'</i>'
            content = content.replace(expr,italic)
        return content

    def handleBold(self,content):
        toBold = getAllInside('**','**', content)
        for expr in toBold:
            print('Bold :',expr)
            bold = '<b>'+toBold[expr]+'</b>'
            content = content.replace(expr,bold)
        return content

    def handleBoldItalics(self,content):
        toBoldItalicize = getAllInside('***','***', content)
        for expr in toBoldItalicize:
            print('BoldItalics :',expr)
            boldItalic = '<i><b>'+toBoldItalicize[expr]+'</b></i>'
            content = content.replace(expr,boldItalic)
        return content

    def makeReferences(self,docID):
        def getRef(line):
            print('Getting from: ',line)
            keyword = 'indent" >'
            i = line.index(keyword)
            reference = line[i+len(keyword):]
            print('The ref is: ',reference)
            while ' ' in reference[0]:
                reference = reference[1:]
            return reference.replace('\n','')

        '''Updates the references'''
        self.references[docID]['References'] = ''
        ### Make the tex file and compile it ###
        citations = open(os.getcwd()+'/Archieves/cit.tex','w')
        citations.write('''\\documentclass{article}
\\usepackage[T1]{fontenc}
\\usepackage[utf8]{inputenc}
\\usepackage[alf,abnt-etal-list=0,abnt-repeated-author-omit=no]{abntex2cite}
\\usepackage{url}

\\begin{document}
''')
        refs = []
        for ref in self.references[docID]['keys']:
            citations.write(ref+'\n\n')
            refs.append(ref)
        citations.write('''\\bibliography{database}
\end{document}''')
        citations.close()
        call(['htlatex','cit.tex'],cwd=os.getcwd()+'/Archieves/')
        call(['bibtex','cit.aux'],cwd=os.getcwd()+'/Archieves/')
        call(['htlatex','cit.tex'],cwd=os.getcwd()+'/Archieves/')
        ### END: Make the tex file and compile it ###
        ### Parse the compiled HTML file ###
        html = open(os.getcwd()+'/Archieves/cit.html','r',errors='replace',encoding='latin1')
        n = 0
        beginReference = False
        for line in html:
            ### Get citation ###
            if n < len(refs):
                if 'class="noindent"' in line or 'class="indent"' in line:
                    self.references[docID]['keys'][refs[n]] = getRef(line)
                    n+=1
            ### Get reference ###
            else:
                ### Order of the if's is important
                if '</div>' in line:
                    beginReference = False
                if beginReference:
                    self.references[docID]['References']+= line
                if 'thebibliography' in line:
                    beginReference = True

        ### END: Parse the compiled HTML file ###

    def handleCitations(self,docID,cell,content):
        print('Citations working')
        toCitate = getAllInside('\cite{','}',content)
        print('Citation list: ',toCitate)
        ## Check if there is a new citation
        changed = False
        for citation in toCitate:
            if not citation in self.references[docID]['keys']:
                if not 'citations' in self.archive[docID]['page'][cell]:
                    self.archive[docID]['page'][cell]['citations'] = {}
                self.references[docID]['keys'][citation] = ''
                self.archive[docID]['page'][cell]['citations'][citation] = content.count(citation)
                self.references[docID]['counts'][citation] = content.count(citation)
                changed = True
                print('NEW REF ADDED')
            else:
                print('Adding')
                self.references[docID]['counts'][citation] += content.count(citation)
        refUpdate = ''
        if changed:
            self.makeReferences(docID)
            if self.references[docID]['refCell']:
                refUpdate = '!@StartRef@!cell="'+str(self.references[docID]['refCell'])+'"'+self.handleReferences(docID)+'!@EndRef@!'
        for citation in toCitate:
            content = content.replace(citation,self.references[docID]['keys'][citation])    
        print('Content in citation is: ',content)
        return refUpdate+content

    def handleReferences(self,docID,cell=None):
        if cell:
            self.references[docID]['refCell'] = cell
        output = '<h1>References</h1>\n'
        output += self.references[docID]['References']
        return output

    def handleSections(self,content):
        n = 1 #number of #'s in the section mark
        pos = content.index('!#')+2
        for char in content[pos:]:
            if char == '#':
                n+=1
            else:
                break
        heading = ''
        for line in content.split('\n'):
            if '!#' in line:
                label = line.replace('!'+'#'*n,'')
                if label:
                    if label[0] == ' ':
                        label = label[1:]
            else:
                heading += line
        if label:
            return '<h'+str(n)+' id="'+label+'">'+heading+'</h'+str(n)+'>'
        else:
            return '<h'+str(n)+'>'+heading+'</h'+str(n)+'>'

    def handleEquations(self,content):
        eqContent = ''
        for line in content.split('\n'):
            if '!eq' in line:
                label = line.replace('!eq ','')
            else:
                eqContent += line
        eq = '\\begin{equation}'
        if label.replace('<label>',''):
            eq += '\label{'+label+'}\n'
        eq += eqContent+'\end{equation}'
        return eq

    def handleTitle(self,content):
        title = content.replace('!title ','')
        return '<center><b><font size="7">'+title+'</font></b></center><br><br>'
    
    @cherrypy.expose
    def image(self,docID,cell,img,label,source,caption,width):
        cell = int(cell)
        filename = img.filename
        imgWidth = str(int(float(width)*800.0))+'px'
        if cell == len(self.archive[docID]['page']):
            self.archive[docID]['page'].append({'content':{'type':'image','img':filename,'label':label,'source':source,'caption':caption,'width':imgWidth},'output':'.'})
        i = open(os.getcwd()+'/Archieves/Images/'+filename,'wb')
        while True:
            data = img.file.read(4096)
            if not data:
                break
            else:
                i.write(data)
            print('Loading...')
        i.close()
        if label:
            output = '<br><center><figcaption id="'+label+'">'+caption+'</figcaption>'+'<img style="width:'+imgWidth+'" src="Archieves/Images/'+filename+'"><br>Source: '+source+'</center><br>'
        else:
            output = '<br><center><figcaption>'+caption+'</figcaption>'+'<img style="width:'+imgWidth+'" src="Archieves/Images/'+filename+'"><br>Source: '+source+'</center><br>'
        self.archive[docID]['page'][cell]['output'] = output
        return output

    @cherrypy.expose
    def saveFile(self,docID,filename,extension):
        if extension == 'will':
            self.saveAsWill(docID,filename)
        elif extension == 'tex':
            self.saveAs(docID,filename,extension)
        elif extension == 'docx':
            self.saveAs(docID,filename,extension)
        elif extension == 'pdflatex':
            self.saveAs(docID,filename,extension)
            extension = 'pdf'
        return serve_file(os.getcwd()+'/Archieves/'+filename+'.'+extension,"application/x-download","attachment")

    def saveAsWill(self,docID,filename):
        archive = open(os.getcwd()+'/Archieves/'+filename+'.will','wb')
        self.archive[docID]['references'] = self.references[docID]
        try:
            pickle.dump(self.archive[docID],archive)
        except Exception as e:
            print('Could not save state! ',e)
            self.archive[docID]['Locals'] = {}
            pickle.dump(self.archive[docID],archive)
        archive.close()

    def saveAs(self,docID,filename,docFormat,article=True):
        if article:
            texClass = 'article'
        else:
            texClass = 'report'
        if docFormat == 'tex':
            from texExporter import TexExporter
            exporter = TexExporter(filename,texClass)
        elif docFormat == 'pdflatex':
            from pdfLatexExporter import PdfLatexExporter
            exporter = PdfLatexExporter(filename,texClass)
        elif docFormat == 'docx':
            from docxExporter import DocxExporter
            exporter = DocxExporter(filename,texClass)

        for cell in self.archive[docID]['page']:
            content = cell['content']
            show = True
            if '<h' in cell['output']:
                for level in range(1,6):
                    n = str(level)
                    if '<h'+n in cell['output']:
                        label = ''
                        endTag = '>'
                        if '<h'+n+' id="' in cell['output']:
                            label = getInside('id="','"',cell['output'])
                            endTag = ' id="'+label+'">'
                        title = getInside('<h'+n+endTag,'</h'+n+'>',cell['output'])
                        exporter.addHeading(title,level,label)
                        ### cells that have more than only a title. E.g. References
                        remaining = cell['output'].replace('<h'+n+endTag,'').replace('</h'+n+'>','').replace(title,'')
                        if remaining:
                            exporter.addText(remaining)
                        else:
                            break
            elif 'class="dontprint"' in cell['output']:
                show = False
            ### special cells ###
            elif 'type' in content and not type(content) == str:
                if content['type'] == 'image':
                    img = content['img']
                    caption = content['caption']
                    source = content['source']
                    label = content['label']
                    width = str(int(content['width'].replace('px',''))/800.0)
                    exporter.addFigure(img,caption,source=source,label=label,width=width)
                else:
                    raise NotImplemented
            else:
                if show:
                    exporter.addText(cell['output'])

        print('ta no close')
        exporter.close()
        print('Acabou')

    @cherrypy.expose
    def open(self,docID,toOpen):
        filename = toOpen.filename
        d = open(os.getcwd()+'/Archieves/'+filename,'wb')
        while True:
            data = toOpen.file.read(4096)
            if not data:
                break
            else:
                d.write(data)
            print('Loading...')
        d.close()
        req = self.openFile(docID,filename)
        return req

    @cherrypy.expose
    def openFile(self,docID,filename):
        self.archive[docID] = {}
        print('Openning file ',filename)
        try:
            archive = open(os.getcwd()+'/Archieves/'+filename,'rb')
        except:
            content = 'Error loading file. File not found.'
            output = content
            print('Error opening file. File does not exist!')
            return '<center id="c1"><textarea id="1" action="evalCell" style="width: 800px; display: none;">'+content+'</textarea></center><center id="co1"><div id="o1" class="paragraph">'+output+'</div></center>'
        self.archive[docID] = pickle.load(archive)
        self.references[docID] = self.archive[docID]['references']
        if 'serverRefCell' in self.references[docID]:
            self.references[docID]['refCell'] = self.references[docID]['serverRefCell']
        else:
            self.references[docID]['refCell'] = None
        self.archive[docID]['Globals'] = {'section':section}
        archive.close()
        notebook = ''
        for cell,stuff in enumerate(self.archive[docID]['page']):
            # toDo check if cell is 'image'. If so, construct the image, not
            # the textArea
            print(cell)
            if 'type' in stuff['content'] and not type(stuff['content']) == str:
                if stuff['content']['type'] == 'image':
                    img = stuff['content']['img']
                    label = stuff['content']['label']
                    source = stuff['content']['source']
                    caption = stuff['content']['caption']

                    notebook += '<center id="c'+str(cell)+'"><form id="F'+str(cell)+'" enctype="multipart/form-data" method="POST" action="image" style="display: none;"><input type="file" name="img" value="Archieves/Images/'+img+'" id="'+str(cell)+'" style="display: none;"><br>Label:<input name="label" value="'+label+'" id="L'+str(cell)+'"><br>Caption:<input name="caption" value="'+caption+'" id="C'+str(cell)+'"><br>Source:<input name="source" value="'+source+'" id="S'+str(cell)+'"><br>Width:<input id="SL'+str(cell)+'"name="width" type="range" min="0" max="1" step="0.01"><br><img id="P'+str(cell)+'" src="Archieves/Images/'+img+'"></form></center>'
                    output = stuff['output']
                    notebook += '<center tabindex="0" id="co'+str(cell)+'"><div id="o'+str(cell)+'" class="paragraph">'+output+'</div></center>'
            else:
                content = stuff['content']
                output = stuff['output']
                notebook += '<center id="c'+str(cell)+'"><textarea id="'+str(cell)+'" action="evalCell" style="width: 800px; display: none;">'+content+'</textarea></center>'
                notebook += '<center tabindex="0" id="co'+str(cell)+'"><div id="o'+str(cell)+'" class="paragraph">'+output+'</div></center>'
        return notebook


if __name__ == '__main__':
    conf = {'/':{'tools.sessions.on':True,'tools.staticdir.on':True,'tools.staticdir.dir':os.getcwd()}}
    cherrypy.quickstart(WillNotebook(),'/',config=conf)
