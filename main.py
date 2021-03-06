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

def msg(msg):
    return '<font class="msg dontprint">'+msg+'</font>'

def error(msg):
    return '<font class="error dontprint">'+msg+'</font>'

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
        self.archive[docID] = {'Globals':{'docID':docID},'Locals':{},'page':[],'references':None}
        self.references[docID] = {'keys':{},'counts':{},'References':'','refCell':''}
        self.loadDefaultFuncs()
        return notebook

    def loadDefaultFuncs(self):
        with open('defaultFunctions.py','r') as funcs:
            self.defaultFuncs = funcs.read()

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
        if type(content) is dict:
            if content['type'] == 'image':
                filename = content['img']
                os.remove(os.getcwd()+'/Archieves/'+docID+'/Images/'+filename)
                content = content['caption']+content['source']
        elif startWith('!ref',content):
            print('Deleting the refCell')
            self.references[docID]['refCell'] = ''
            self.references[docID]['serverRefCell'] = ''
        changedRefs = False
        if '\cite{' in content or '\citeonline{' in content:
            print('Counts: ',self.references[docID]['counts'])
            citations = getAllInside('\cite{','}',content)
            citations.update(getAllInside('\citeonline{','}',content))
            for citation in citations:
                print('Citation deletion: ', citation)
                if '\cite{' in citation:
                    citationList = getInside('\cite{','}',citation).split(',')
                elif '\citeonline{' in citation:
                    citationList = getInside('\citeonline{','}',citation).split(',')
                for individual in citationList:
                    self.references[docID]['counts'][individual] -= content.count(citation)
                    if self.references[docID]['counts'][individual] == 0:
                        del self.references[docID]['counts'][individual]
                        print('Deleting ',individual)
                        if citation in self.references[docID]['keys']:
                            del self.references[docID]['keys'][citation]
                        changedRefs = True
                        print('Citation removed')
        else:
            print('No citation in this cell')
        self.updateRefCell(docID)
        refUpdate = ''
        if changedRefs:
            self.makeReferences(docID)
            if self.references[docID]['refCell']:
                refUpdate = '!@StartRef@!cell="'+str(self.references[docID]['refCell'])+'"'+self.handleReferences(docID)+'!@EndRef@!'
        self.archive[docID]['page'].pop(int(index))
        print('This is the update: ',refUpdate)
        return refUpdate+'Cell deleted'

    @cherrypy.expose
    def evalCell(self,docID,cell,outIndex,content):
        cell = int(cell)
        print(cell)
        if cell == len(self.archive[docID]['page']):
            self.archive[docID]['page'].append({'content':content,'output':'.'})
        self.archive[docID]['page'][cell]['content'] = content
        refUpdate,content = self.handleText(docID,cell,content)
        if startWith('!#',content):
            output = self.handleSections(content)
        elif startWith('!eq',content):
            output = self.handleEquations(content)
        elif startWith('!title',content):
            output = self.handleTitle(content)
        elif content == '!ref':
            output = self.handleReferences(docID,cell=outIndex)
        elif startWith('!tab',content):
            output = self.handleTables(content)
        elif startWith('!-',content):
            output = self.handleBullets(content)
        elif startWith('!keyfor',content):
            output = self.handleBibKeySearch(docID,content)
        elif startWith('!addref',content):
            output = self.handleInsertBibEntry(docID,content)
        elif startWith('!delref',content):
            output = self.handleDeleteBibEntry(docID,content)
        elif startWith('!infofor',content):
            output = self.handleInfoForBibEntry(docID,content)
        elif startWith('!todo',content):
            output = self.handleTODO(content)
        elif startWith('!resumo',content):
            output = self.handleAbstracts(docID,'Resumo',content)
        elif startWith('!abstract',content):
            output = self.handleAbstracts(docID,'Abstract',content)
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
        self.updateRefCell(docID)
        return output

    def updateRefCell(self,docID):
        if self.references[docID]['refCell']:
            for n in range(len(self.archive[docID]['page'])):
                if self.archive[docID]['page'][n]['content'] == '!ref':
                    refCell = n
            self.references[docID]['serverRefCell'] = refCell
            self.archive[docID]['page'][refCell]['output'] = '<h1>References</h1>\n'+self.references[docID]['References']

    def handleText(self,docID,cell,content):
        ### Existing cell ###
        ### Check if there was any citation and if it changed ###
        changedCitations = False
        citations = getAllInside('\cite{','}',content)
        citations.update(getAllInside('\citeonline{','}',content))
        if not citations:
            if 'citations' in self.archive[docID]['page'][cell]:
                changedCitations = True
                for citation in self.archive[docID]['page'][cell]['citations']:
                    n = self.archive[docID]['page'][cell]['citations'][citation]
                    if '\cite{' in citation:
                        citationList = getInside('\cite{','}',citation).split(',')
                    elif '\citeonline{' in citation:
                        citationList = getInside('\citeonline{','}',citation).split(',')
                    for individual in citationList:
                        self.references[docID]['counts'][individual] -= n
                        print('Citation '+individual+' was removed from content')
                        if self.references[docID]['counts'][individual] == 0:
                            del self.references[docID]['counts'][individual]
                            print('No more citation '+citation+' in document. Deleting...')
                            if citation in self.references[docID]['keys']:
                                del self.references[docID]['keys'][citation]
                del self.archive[docID]['page'][cell]['citations']
        else:
            if 'citations' in self.archive[docID]['page'][cell]:
                cellCitations = [i for i in self.archive[docID]['page'][cell]['citations'].keys()]
                for citation in cellCitations:
                    if not citation in citations:
                        print('Removing citation from counters')
                        n = self.archive[docID]['page'][cell]['citations'][citation]
                        if '\cite{' in citation:
                            citationList = getInside('\cite{','}',citation).split(',')
                        elif '\citeonline{' in citation:
                            citationList = getInside('\citeonline{','}',citation).split(',')
                        for individual in citationList:
                            self.references[docID]['counts'][individual] -= n
                            if self.references[docID]['counts'][individual] == 0:
                                changedCitations = True
                                del self.references[docID]['counts'][individual]
                                if citation in self.archive[docID]['page'][cell]['citations']:
                                    del self.archive[docID]['page'][cell]['citations'][citation]
                                if citation in self.references[docID]['keys']:
                                    del self.references[docID]['keys'][citation]
                    else:
                        print('Updating citation counters')
                        oldN = self.archive[docID]['page'][cell]['citations'][citation]
                        if '\cite{' in citation:
                            citationList = getInside('\cite{','}',citation).split(',')
                        elif '\citeonline{' in citation:
                            citationList = getInside('\citeonline{','}',citation).split(',')
                        for individual in citationList:
                            self.references[docID]['counts'][individual] -= oldN
        refUpdate = ''
        if changedCitations:
            if self.references[docID]['refCell']:
                self.makeReferences(docID)
                refUpdate = '!@StartRef@!cell="'+str(self.references[docID]['refCell'])+'"'+self.handleReferences(docID)+'!@EndRef@!'
        if startWith('#code',content):
            content = self.handlePythonCode(docID,cell,content)
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
            if ('\cite{' in content or '\citeonline{' in content) and '}' in content:
                content = self.handleCitations(docID,cell,content)
        self.updateRefCell(docID)
        return refUpdate, content

    def renderText(self,docID,content):
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
                toCitate = getAllInside('\cite{','}',content)
                for citation in toCitate:
                    content = content.replace(citation,self.references[docID]['keys'][citation])    
            return content

    def handlePythonCode(self,docID,cell,content):
        with Capturing() as output:
            try:
                if 'matplotlib' in content and 'savefig' in content:
                    #Its a plot! Parse the imagename and treat it like an image
                    return self.handlePlot(docID, cell, content)
                exec(self.defaultFuncs+content,self.archive[docID]['Globals'])#,self.archive[docID]['Locals'])
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
            return '<br>'.join(output)

    def handlePlot(self,docID,cell,content):
        plotArgs = getInside('savefig(',')',content)
        f = 'def getName(*args,**kwargs):\n    return args[0]\n_internalPlotName = getName('+plotArgs+')'
        g = {}
        exec(f,g)
        filename = eval('_internalPlotName',g)
        label = ''
        source = ''
        caption = 'Testing plot'
        imgWidth = '800px'
        code = ''
        try:
            os.mkdir(os.getcwd()+'/Archieves/'+docID)
        except FileExistsError:
            pass
        try:
            os.mkdir(os.getcwd()+'/Archieves/'+docID+'/Images')
        except FileExistsError:
            pass
        for line in content.split('\n'):
            if '#code' in line:
                label = line.replace('#code ','')
            elif 'savefig' in line:
                line = line.replace('savefig(',f'savefig(os.getcwd()+"/Archieves/{docID}/Images/{filename}",discard=')
                code += line+'\n'
            else:
                code += line+'\n'
        print(code)

        exec(self.defaultFuncs+code,self.archive[docID]['Globals'])#,self.archive[docID]['Locals'])

        _,handledCaption = self.handleText(docID,cell,caption) # handle caption, will mess refUpdate
        _,handledSource = self.handleText(docID,cell,source) # handle source, will mess refUpdate
        refUpdate,_ = self.handleText(docID,cell,caption+source) # handle refUpdate
        caption = handledCaption # restoring caption
        source = handledSource # restoring source
        if source:
            source = 'Source: '+ source
        if label:
            output = '<br><center><figcaption id="'+label+'">'+caption+'</figcaption>'+'<img style="width:'+imgWidth+'" src="Archieves/@$docID$@/Images/'+filename+'"><br>'+source+'</center><br>'
        else:
            output = '<br><center><figcaption>'+caption+'</figcaption>'+'<img style="width:'+imgWidth+'" src="Archieves/@$docID$@/Images/'+filename+'"><br>'+source+'</center><br>'
        self.archive[docID]['page'][cell] = {'content':{'type':'image','img':filename,'label':label,'source':source,'caption':caption,'width':imgWidth},'output':'.'}
        self.archive[docID]['page'][cell]['output'] = output
        return refUpdate+output.replace('@$docID$@',docID)
        
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
            #print('Bold :',expr)
            bold = '<b>'+toBold[expr]+'</b>'
            content = content.replace(expr,bold)
        return content

    def handleBoldItalics(self,content):
        toBoldItalicize = getAllInside('***','***', content)
        for expr in toBoldItalicize:
            #print('BoldItalics :',expr)
            boldItalic = '<i><b>'+toBoldItalicize[expr]+'</b></i>'
            content = content.replace(expr,boldItalic)
        return content

    def makeReferences(self,docID):
        def getRef(line):
            #print('Getting from: ',line)
            keyword = 'indent" >'
            i = line.index(keyword)
            reference = line[i+len(keyword):]
            #print('The ref is: ',reference)
            while ' ' in reference[0]:
                reference = reference[1:]
            return reference.replace('\n','')

        '''Updates the references'''
        self.references[docID]['References'] = ''
        ### Make the tex file and compile it ###
        citations = open(os.getcwd()+'/Archieves/'+docID+'/cit.tex','w')
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
        call(['htlatex','cit.tex'],cwd=os.getcwd()+'/Archieves/'+docID)
        call(['bibtex','cit.aux'],cwd=os.getcwd()+'/Archieves/'+docID)
        call(['htlatex','cit.tex'],cwd=os.getcwd()+'/Archieves/'+docID)
        ### END: Make the tex file and compile it ###
        ### Parse the compiled HTML file ###
        html = open(os.getcwd()+'/Archieves/'+docID+'/cit.html','r',errors='replace',encoding='latin1')
        n = 0
        beginReference = False
        buffedLine = ''
        buffering = False
        for line in html:
            ### Get citation ###
            if n < len(refs):
                print(buffering)
                if 'class="noindent"' in line or 'class="indent"' in line or buffering:
                    print('entrou')
                    buffedLine += line # This is because if some references are too long and there is a new line, citation gets cut.
                    #print(buffedLine)
                    if ')' in line:
                        self.references[docID]['keys'][refs[n]] = getRef(buffedLine)
                        buffedLine = ''
                        buffering = False
                        n+=1
                    else:
                        buffering = True
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
        toCitate.update(getAllInside('\citeonline{','}',content))
        print('Citation list: ',toCitate)
        ## Check if there is a new citation
        changed = False
        for citation in toCitate:
            if not citation in self.references[docID]['keys']:
                if not 'citations' in self.archive[docID]['page'][cell]:
                    self.archive[docID]['page'][cell]['citations'] = {}
                self.references[docID]['keys'][citation] = ''
                self.archive[docID]['page'][cell]['citations'][citation] = content.count(citation)
                if '\cite{' in citation:
                    citationList = getInside('\cite{','}',citation).split(',')
                elif '\citeonline{' in citation:
                    citationList = getInside('\citeonline{','}',citation).split(',')
                for individual in citationList:
                    if not individual in self.references[docID]['counts']:
                        self.references[docID]['counts'][individual] = 0
                    self.references[docID]['counts'][individual] += content.count(citation)
                changed = True
                print('NEW REF ADDED')
            else:
                print('Adding')
                if '\cite{' in citation:
                    citationList = getInside('\cite{','}',citation).split(',')
                elif '\citeonline{' in citation:
                    citationList = getInside('\citeonline{','}',citation).split(',')
                for individual in citationList:
                    if not individual in self.references[docID]['counts']:
                        self.references[docID]['counts'][individual] = 0
                    self.references[docID]['counts'][individual] += content.count(citation)
        refUpdate = ''
        if changed:
            self.makeReferences(docID)
            if self.references[docID]['refCell']:
                refUpdate = '!@StartRef@!cell="'+str(self.references[docID]['refCell'])+'"'+self.handleReferences(docID)+'!@EndRef@!'
        for citation in toCitate:
            content = content.replace(citation,self.references[docID]['keys'][citation])    
        #print('Content in citation is: ',content.encode('utf8'))
        return refUpdate+content

    def handleReferences(self,docID,cell=None):
        if cell:
            print('RefCell is ',cell)
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
        nonNumbered = False
        for line in content.split('\n'):
            if '!eq*' in line:
                label = line.replace('!eq*','').strip()
                nonNumbered = True
            elif '!eq' in line:
                label = line.replace('!eq','').strip()
            else:
                eqContent += line
        if nonNumbered:
            eq = '\\begin{equation*}'
        else:
            eq = '\\begin{equation}'
        if label.replace('<label>',''):
            eq += '\label{'+label+'}\n'
        if nonNumbered:
            eq += eqContent+'\end{equation*}'
        else:
            eq += eqContent+'\end{equation}'
        return eq

    def handleTitle(self,content):
        title = content.replace('!title ','')
        return '<div class="title">'+title+'</div>'

    def handleBibKeySearch(self,docID,content):
        terms = content.replace('!keyfor ','').strip()
        begin = '<font class="bibKeys dontprint">'
        matchingKeys = ''
        bibData = self.getBibKeys(docID,getInfo=True)
        for key in bibData:
            for term in terms:
                if term in bibData[key]:
                    matchingKeys += key+'\n'
                    break
        end = '</font>'
        if matchingKeys:
            return begin+matchingKeys+end
        else:
            return begin+'No matching result'+end

    def getBibKeys(self,docID,bibText=None,getInfo=False):
        if not docID in os.listdir(os.getcwd()+'/Archieves'):
            os.mkdir(os.getcwd()+'/Archieves/'+docID)
        if not 'database.bib' in os.listdir(os.getcwd()+'/Archieves/'+docID):
            with open(os.getcwd()+'/Archieves/'+docID+'/database.bib','w',encoding='utf8') as bib:
                pass
        if bibText:
            bibData = bibText
        else:
            with open(os.getcwd()+'/Archieves/'+docID+'/database.bib','r',encoding='utf8') as bib:
                bibData = bib.read()
        comma = 0
        if getInfo:
            keys = {}
        else:
            keys = []
        while True:
            try:
                cursor = bibData.index('@',comma)
                openBrace = bibData.index('{',cursor)
                comma = bibData.index(',',openBrace)
                key = bibData[openBrace+1:comma]
                try:
                    nextEntry = bibData.index('@',comma)
                except ValueError:
                    nextEntry = -1
                if getInfo:
                    keys[key] = bibData[cursor:nextEntry]
                else:
                    keys.append(key)
            except ValueError:
                break
        return keys

    def handleInsertBibEntry(self,docID,bibText):
        bibText = bibText.replace('!addref','').strip()
        key = self.getBibKeys(docID,bibText=bibText)
        if key:
            key = key[0]
            if key in self.getBibKeys(docID):
                return error('Holy! Entry already exists in the database.')
            else:
                with open(os.getcwd()+'/Archieves/'+docID+'/database.bib','a',encoding='utf8') as bib:
                    bib.write(bibText+'\n\n')
                return msg('Inserted bib entry')
        else:
            return error('Woops! This is not a valid bibtex entry.')

    def handleDeleteBibEntry(self,docID,bibKey):
        bibKey = bibKey.replace('!delref','').strip()
        if bibKey in self.getBibKeys(docID):
            entry = self.getBibKeys(docID,getInfo=True)[bibKey].strip()+'\n\n'
            with open(os.getcwd()+'/Archieves/'+docID+'/database.bib','r',encoding='utf8') as bib:
                bibData = bib.read()
            bibData = bibData.replace(entry,'')
            with open(os.getcwd()+'/Archieves/'+docID+'/database.bib','w',encoding='utf8') as bib:
                bib.write(bibData)
            return msg('Deleted '+bibKey+' bib entry')
        else:
            return error('Woops! This key is not in the database.')
    
    def handleInfoForBibEntry(self,docID,bibKey):
        bibKey = bibKey.replace('!infofor','').strip()
        if bibKey in self.getBibKeys(docID):
            entry = self.getBibKeys(docID,getInfo=True)[bibKey].strip()+'\n\n'
            return msg(entry)
        else:
            return error('Woops! This key is not in the database.')

    def handleTODO(self,content):
        content = content.replace('!todo ','')
        return '<font class="todo dontprint">TODO: '+content+'</font>'

    @cherrypy.expose
    def image(self,docID,cell,img,label,source,caption,width):
        def loadImg(filename):
            try:
                os.mkdir(os.getcwd()+'/Archieves/'+docID)
            except FileExistsError:
                pass
            try:
                os.mkdir(os.getcwd()+'/Archieves/'+docID+'/Images')
            except FileExistsError:
                pass
            i = open(os.getcwd()+'/Archieves/'+docID+'/Images/'+filename,'wb')
            try:
                while True:
                    data = img.file.read(4096)
                    if not data:
                        break
                    else:
                        i.write(data)
                    print('Loading...')
                i.close()
            except AttributeError:
                print('Using cached image')
        cell = int(cell)
        imgWidth = str(int(float(width)*800.0))+'px'
        if not type(img) == str:
            filename = img.filename
        else:
            filename = None
            print('No filename. Checking if it is just an update')
            try:
                filename = self.archive[docID]['page'][cell]['content']['img']
            except:
                print('Its not update. User forgot to enter img')
                output = '<font class="dontprint" color="red">Warning, no image was inserted. Please try again.</font>'
                if cell == len(self.archive[docID]['page']):
                    self.archive[docID]['page'].append({'content':{'type':'image','img':filename,'label':label,'source':source,'caption':caption,'width':imgWidth},'output':output})
                return output
            print('Its update. Using filename: ',filename)
        if cell == len(self.archive[docID]['page']):
            self.archive[docID]['page'].append({'content':{'type':'image','img':filename,'label':label,'source':source,'caption':caption,'width':imgWidth},'output':'.'})
            loadImg(filename)
        else:
            # existing cell
            if 'type' in self.archive[docID]['page'][cell]['content']:
                if self.archive[docID]['page'][cell]['content']['type'] == 'image':
                    # Updating image cell
                    print('Updating image!')
                    if not filename == self.archive[docID]['page'][cell]['content']['img']:
                        print('There should be an filename: ',filename)
                        loadImg(filename)
                    elif self.archive[docID]['page'][cell]['content']['img'] == None:
                        return '<font class="dontprint" color="red">Warning, no image was inserted. Please try again.</font>'
                    self.archive[docID]['page'][cell]['content']['img'] = filename
                    self.archive[docID]['page'][cell]['content']['label'] = label
                    self.archive[docID]['page'][cell]['content']['source'] = source
                    self.archive[docID]['page'][cell]['content']['caption'] = caption
                    self.archive[docID]['page'][cell]['content']['width'] = imgWidth
            else:
                if filename:
                    loadImg(filename)
                else:
                    return '<font class="dontprint" color="red">Warning, no image was inserted. Please try again.</font>'
                    
                self.archive[docID]['page'][cell] = {'content':{'type':'image','img':filename,'label':label,'source':source,'caption':caption,'width':imgWidth},'output':'.'}
        _,handledCaption = self.handleText(docID,cell,caption) # handle caption, will mess refUpdate
        _,handledSource = self.handleText(docID,cell,source) # handle source, will mess refUpdate
        refUpdate,_ = self.handleText(docID,cell,caption+source) # handle refUpdate
        caption = handledCaption # restoring caption
        source = handledSource # restoring source
        if source:
            source = 'Source: '+source
        if label:
            output = '<br><center><figcaption id="'+label+'">'+caption+'</figcaption>'+'<img style="width:'+imgWidth+'" src="Archieves/@$docID$@/Images/'+filename+'"><br>'+source+'</center><br>'
        else:
            output = '<br><center><figcaption>'+caption+'</figcaption>'+'<img style="width:'+imgWidth+'" src="Archieves/@$docID$@/Images/'+filename+'"><br>'+source+'</center><br>'
        self.archive[docID]['page'][cell]['output'] = output
        return refUpdate+output.replace('@$docID$@',docID)

    def handleTables(self,content):
        table = '<center><table>'
        caption = ''
        source = ''
        label = ''
        for row in content.split('\n'):
            if '!tab' in row:
                label = row.replace('!tab ','')
            elif not '|' in row:
                if row:
                    if not caption:
                        caption = '<div class="tableCaption" id="'+label+'">'+row+'</div>'
                    else:
                        source = row
            elif '||' in row:
                headings = row.split('||')
                table += '<tr>\n'
                for heading in headings:
                    table += '<th>'+heading+'</th>'
                table += '</tr>'
            elif '|' in row:
                cols = row.split('|')
                table += '<tr>\n'
                for col in cols:
                    table += '<td>'+col+'</td>'
                table += '</tr>'
            table += '\n'
        if not source:
            table += '</table></center>\n'
        else:
            table += '</table><br>Source: '+source+'</center>\n'
        return caption+table

    def handleBullets(self,content):
        return '<li>'+content.replace('!- ','').replace('!-','')+'</li>'

    def handleAbstracts(self,docID,title,content):
        ''' Doesn't count citations '''
        abstract = '<h1 class="abstract">'+title+'</h1>'
        blankLine = False
        content = content.replace('!'+title.lower(),'')
        for line in content.split('\n'):
            if line:
                abstract += '<br>'+self.renderText(docID,line)
                blankLine = False
            else:
                if not blankLine:
                    abstract += '<br>'
                    blankLine = True
        return abstract

    @cherrypy.expose
    def saveFile(self,docID,filename,extension,model):
        if extension == 'will':
            self.saveAsWill(docID,filename)
        elif extension == 'tex':
            self.saveAs(docID,filename,extension,model)
        elif extension == 'docx':
            self.saveAs(docID,filename,extension,model)
        elif extension == 'pdflatex':
            self.saveAs(docID,filename,extension,model)
            extension = 'pdf'
        return serve_file(os.getcwd()+'/Archieves/'+docID+'/'+filename+'.'+extension,"application/x-download","attachment")

    def saveAsWill(self,docID,filename):
        import tarfile
        try:
            os.mkdir(os.getcwd()+'/Archieves/'+docID)
        except FileExistsError:
            pass
        archive = open(os.getcwd()+'/Archieves/'+docID+'/'+filename+'.wnb','wb')
        self.archive[docID]['references'] = self.references[docID]
        try:
            pickle.dump(self.archive[docID],archive)
        except Exception as e:
            print('Could not save state! ',e)
            self.archive[docID]['Locals'] = {}
            pickle.dump(self.archive[docID],archive)
        archive.close()
        try:
            os.mkdir(os.getcwd()+'/Archieves/'+docID+'/Images')
        except FileExistsError:
            pass
        if not 'database.bib' in os.listdir(os.getcwd()+'/Archieves/'+docID):
            db = open(os.getcwd()+'/Archieves/'+docID+'/database.bib','w')
            db.close()
        with tarfile.open(os.getcwd()+'/Archieves/'+docID+'/'+filename+'.will','w:xz') as will:
            will.add(os.getcwd()+'/Archieves/'+docID+'/'+filename+'.wnb',arcname=filename+'.wnb')
            will.add(os.getcwd()+'/Archieves/'+docID+'/database.bib',arcname='database.bib')
            will.add(os.getcwd()+'/Archieves/'+docID+'/Images',arcname='Images')

    def saveAs(self,docID,filename,docFormat,model):
        try:
            os.mkdir(os.getcwd()+'/Archieves/'+docID)
        except FileExistsError:
            pass
        try:
            os.mkdir(os.getcwd()+'/Archieves/'+docID+'/Images')
        except FileExistsError:
            pass
        if not 'database.bib' in os.listdir(os.getcwd()+'/Archieves/'+docID):
            db = open(os.getcwd()+'/Archieves/'+docID+'/database.bib','w')
            db.close()
        if model == 'article':
            texClass = 'article'
        elif model == 'usp':
            texClass = 'abntepusp'
        else:
            texClass = 'report'
        if docFormat == 'tex':
            from texExporter import TexExporter
            exporter = TexExporter(filename,docID,texClass)
        elif docFormat == 'pdflatex':
            from pdfLatexExporter import PdfLatexExporter
            exporter = PdfLatexExporter(filename,docID,texClass)
        elif docFormat == 'docx':
            from docxExporter import DocxExporter
            exporter = DocxExporter(filename,docID,texClass)

        for cell in self.archive[docID]['page']:
            content = cell['content']
            show = True
            if '<h' in cell['output'] and not '!ref' in content and not 'class="abstract"' in cell['output']:
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
            elif 'dontprint' in cell['output']:
                show = False
            ### special cells ###
            elif 'type' in content and not type(content) == str:
                if content['type'] == 'image':
                    img = content['img']
                    caption = content['caption']
                    source = content['source']
                    label = content['label']
                    source = self.renderText(docID,source)
                    caption = self.renderText(docID,caption)
                    width = str(float(content['width'].replace('px',''))/800)
                    print('On main.py image width is ',width)
                    exporter.addFigure(img,caption,source=source,label=label,width=width)
                else:
                    raise NotImplemented
            elif '!tab' in content:
                caption = ''
                label = ''
                table = ''
                source = ''
                for row in content.split('\n'):
                    if '!tab' in row:
                        label = row.replace('!tab ','')
                    elif not '|' in row:
                        if row:
                            if not caption:
                                caption = row
                            else:
                                source = row
                    else:
                        table += row+'\n'
                exporter.addTable(table,caption,label,source)
            elif '!title' in content:
                title = content.replace('!title ','')
                exporter.addTitle(title)
            elif '!author' in content:
                author = content.replace('!author ','')
                exporter.addAuthor(author)
            elif '!advisor' in content:
                advisor = content.replace('!advisor ','')
                exporter.addAdvisor(advisor)
            elif '!concentration' in content:
                area = content.replace('!concentration ','')
                exporter.addConcentrationArea(area)
            elif '!modeltype' in content:
                params = content.replace('!modeltype ','').split(' ')
                model = params[0]
                del params[0]
                area = ' '.join(params)
                exporter.addModelType(model,area)
            elif '!local' in content:
                local = content.replace('!local ','')
                exporter.addLocal(local)
            elif '!department' in content:
                department = content.replace('!department ','')
                exporter.addDepartment(department)
            elif '!date' in content:
                date = content.replace('!date ','')
                exporter.addDate(date)
            elif '!makecover' in content.lower():
                exporter.makeCover()
            elif '!- ' in content.lower():
                topic = cell['output'].replace('<li>','').replace('</li>','').strip()
                exporter.addBullet(topic)
            elif '!ref' in content:
                exporter.addReferences(cell['output'])
            elif '!resumo' in content:
                exporter.addAbstracts('Resumo',cell['output'])
            elif '!abstract' in content:
                exporter.addAbstracts('Abstract',cell['output'])
            else:
                if show:
                    exporter.addText(content,cell['output'])

        print('ta no close')
        exporter.close()
        print('Acabou')

    @cherrypy.expose
    def open(self,docID,toOpen):
        import tarfile
        filename = toOpen.filename
        try:
            print('Trying to create a folder for the document')
            os.mkdir(os.getcwd()+'/Archieves/'+docID)
            print('Done')
        except FileExistsError:
            print('Document was open before. Overwriting')
            import shutil
            shutil.rmtree(os.getcwd()+'/Archieves/'+docID)
            os.mkdir(os.getcwd()+'/Archieves/'+docID)
            print('Done rewriting')
        if '.will' in filename:
            d = open(os.getcwd()+'/Archieves/'+docID+'/'+filename,'wb')
            while True:
                data = toOpen.file.read(4096)
                if not data:
                    break
                else:
                    d.write(data)
                print('Loading...')
            d.close()
            with tarfile.open(os.getcwd()+'/Archieves/'+docID+'/'+filename,mode='r:xz') as will:
                will.extractall(path=os.getcwd()+'/Archieves/'+docID+'/')
            req = self.openFile(docID,filename)
            return req
        else:
            return 'Filetype not suported for opening'

    @cherrypy.expose
    def openFile(self,docID,filename):
        self.archive[docID] = {}
        print('Openning file ',filename)
        for f in os.listdir(os.getcwd()+'/Archieves/'+docID):
            if '.wnb' in f:
                filename = f
        try:
            archive = open(os.getcwd()+'/Archieves/'+docID+'/'+filename,'rb')
        except:
            content = 'Error loading file. File not found.'
            output = content
            print('Error opening file. File does not exist!')
            return '<center id="c1"><textarea id="1" action="evalCell" style="width: 800px; display: none;">'+content+'</textarea></center><center id="co1"><div id="o1" class="paragraph">'+output+'</div></center>'
        self.archive[docID] = pickle.load(archive)
        if 'references' in self.archive[docID]:
            self.references[docID] = self.archive[docID]['references']
        else:
            self.references[docID] = {'keys':{},'counts':{},'References':'','refCell':''}
        if 'serverRefCell' in self.references[docID]:
            self.references[docID]['refCell'] = self.references[docID]['serverRefCell']
        else:
            self.references[docID]['refCell'] = None
        self.archive[docID]['Globals'] = {'docID':docID}
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
                    width = stuff['content']['width']
                    widthValue = str(float(width.replace('px',''))/800)

                    notebook += '<center id="c'+str(cell)+'"><form id="F'+str(cell)+'" enctype="multipart/form-data" method="POST" action="image" style="display: none;"><input type="file" name="img" value="Archieves/'+docID+'/Images/'+img+'" id="'+str(cell)+'" style="display: none;"><br>Label:<input name="label" value="'+label+'" id="L'+str(cell)+'"><br>Caption:<input name="caption" value="'+caption+'" id="C'+str(cell)+'"><br>Source:<input name="source" value="'+source+'" id="S'+str(cell)+'"><br>Width:<input id="SL'+str(cell)+'"name="width" type="range" min="0" max="1" step="0.01" value="'+widthValue+'"><br><img id="P'+str(cell)+'" src="Archieves/'+docID+'/Images/'+img+'" style="width:'+width+'"></form></center>'
                    output = stuff['output'].replace('@$docID$@',docID)
                    notebook += '<center tabindex="0" id="co'+str(cell)+'"><div id="o'+str(cell)+'" class="paragraph">'+output+'</div></center>'
            else:
                content = stuff['content']
                output = stuff['output'].replace('@$docID$@',docID)
                notebook += '<center id="c'+str(cell)+'"><textarea id="'+str(cell)+'" action="evalCell" style="width: 800px; display: none;">'+content+'</textarea></center>'
                notebook += '<center tabindex="0" id="co'+str(cell)+'"><div id="o'+str(cell)+'" class="paragraph">'+output+'</div></center>'
        return notebook


if __name__ == '__main__':
    conf = {'/':{'tools.sessions.on':True,'tools.staticdir.on':True,'tools.staticdir.dir':os.getcwd()}}
    cherrypy.quickstart(WillNotebook(),'/',config=conf)
