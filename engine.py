from browser import document, alert, ajax, window
from browser.html import TEXTAREA, CENTER, DIV, PRE, FORM, INPUT, BUTTON, BR, IMG

jq = window.jQuery.noConflict(True)

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

def shortcuts(ev):
    id = document.activeElement.id
    if ev.shiftKey and ev.which == 13:
        handleShiftEnter(id)
        ev.returnValue = False
    elif ev.which == 13:
        handleInEnter(id)
    elif ev.shiftKey and ev.which == 46:
        handleShiftDelete(id)
        ev.returnValue = False
    elif ev.altKey and ev.which == 78:
        handleAltN(id)
        ev.returnValue = False
    elif ev.shiftKey and ev.which == 38:
        handleShiftUp(id)
        ev.returnValue = False
    elif ev.shiftKey and ev.which == 40:
        handleShiftDown(id)
        ev.returnValue = False
    elif ev.which == 27:
        handleEsc(id)
        ev.returnValue = False
    elif ev.altKey and ev.which == 67:
        handleInAltC(id)
        ev.returnValue = False
    elif ev.altKey and ev.which == 69:
        handleInAltE(id)
        ev.returnValue = False
    elif ev.altKey and ev.which == 49:
        handleInAlt1(id)
        ev.returnValue = False
    elif ev.altKey and ev.which == 50:
        handleInAlt2(id)
        ev.returnValue = False
    elif ev.altKey and ev.which == 51:
        handleInAlt3(id)
        ev.returnValue = False
    elif ev.altKey and ev.which == 52:
        handleInAlt4(id)
        ev.returnValue = False
    elif ev.altKey and ev.which == 53:
        handleInAlt5(id)
        ev.returnValue = False
    elif ev.altKey and ev.which == 73:
        handleInAltI(id)
        ev.returnValue = False
    elif ev.altKey and ev.which == 84:
        handleInAltT(id)
        ev.returnValue = False
    elif ev.altKey and ev.which == 66:
        handleInAltB(id)
        ev.returnValue = False

def outShortcuts(ev):
    global lastFocused
    try:
        id = document.activeElement.id
        print('Focused on: ',id)
        if ev.shiftKey and ev.which == 38:
            handleShiftUp(id)
            ev.returnValue = False
        elif ev.shiftKey and ev.which == 40:
            handleShiftDown(id)
            ev.returnValue = False
        elif ev.which == 13:
            handleOutEnter(id)
            ev.returnValue = False
        elif ev.shiftKey and ev.which == 46:
            handleShiftDelete(id)
            ev.returnValue = False
        elif ev.altKey and ev.which == 78:
            handleAltN(id)
            ev.returnValue = False
        elif ev.altKey and ev.which == 67:
            handleOutAltC(id)
            ev.returnValue = False
        elif ev.altKey and ev.which == 69:
            handleOutAltE(id)
            ev.returnValue = False
        elif ev.altKey and ev.which == 49:
            handleOutAlt1(id)
            ev.returnValue = False
        elif ev.altKey and ev.which == 50:
            handleOutAlt2(id)
            ev.returnValue = False
        elif ev.altKey and ev.which == 51:
            handleOutAlt3(id)
            ev.returnValue = False
        elif ev.altKey and ev.which == 52:
            handleOutAlt4(id)
            ev.returnValue = False
        elif ev.altKey and ev.which == 53:
            handleOutAlt5(id)
            ev.returnValue = False
        elif ev.altKey and ev.which == 73:
            handleOutAltI(id)
            ev.returnValue = False
        elif ev.altKey and ev.which == 84:
            handleOutAltT(id)
            ev.returnValue = False
        elif ev.altKey and ev.which == 66:
            handleOutAltB(id)
            ev.returnValue = False
    except Exception as e:
        print(e)

def handleShiftEnter(id):
    global page
    id = id.replace('S','')
    id = id.replace('C','')
    id = id.replace('L','')
    print('ID: ',id)
    print('last: ',page[-1])
    if id == page[-1]:
        newCell()
    else:
        idDown = str(page[page.index(id)+1])
        if not document[idDown].style.display == 'none':
            document[idDown].focus()
        else:
            document['co'+idDown].focus()
    try:
        eval(id)
    except Exception as e:
        print('Exception ShiftEnter: ',e)

def handleAltN(id):
    print('Insert after ',id)
    global jq,lastFocused,cellCounter
    id = id.replace('co','')
    newCell()
    jq("#c"+str(cellCounter-1)).insertAfter("#co"+id)
    jq("#co"+str(cellCounter-1)).insertAfter("#c"+str(cellCounter-1))
    document[str(cellCounter-1)].focus()
    document[id].style.display = 'none'
    sendNewCell(page.index(id)+1)
    page.insert(str(page.index(id)+1),page.pop())

def handleShiftDelete(id):
    if id == page[-1]:
        document[id].value = ''
    elif 'co' in id:
        del document[id] #del co
        del document[id[0]+id[2:]] #del c
        focusNextCell(id)
        sendDeleteCell(page.index(id[2:]))
        page.remove(id[2:])
    else: #soh numero
        del document['co'+id]
        del document['c'+id]
        focusNextCell(id)
        sendDeleteCell(page.index(id))
        page.remove(id)
    updateSectionNumbers()
    updateFigureNumbers()
    updateTableNumbers()
    handleReferences()
    window.math.reNumber()
    print('Cell deleted')
    print(page)

lastFocused = None
def lastFocus(ev):
    global lastFocused
    lastFocused = ev.target.id

def handleShiftUp(id):
    global page
    print('ShiftUp')
    print('Active element: ',id)
    print(page)
    id = id.replace('c','').replace('o','')
    if not id == page[0]:
        print('not first')
        upId = page.index(id)-1
        print('Focus on: o',page[upId])
        if document[page[upId]].style.display == 'none':
            print('if')
            document['co'+page[upId]].focus()
        else:
            document[page[upId]].focus()
            print('else')

def handleShiftDown(id):
    print('ShiftDown')
    print('Active element: ',id)
    id = id.replace('c','').replace('o','')
    global page
    if not id == page[-1]:
        print('not last')
        downId = page.index(id)+1
        print('Focus on: o',downId)
        if document[page[downId]].style.display == 'none':
            document['co'+page[downId]].focus()
        else:
            document[page[downId]].focus()

def handleOutEnter(id):
    id = id.replace('co','')
    document[id].style.display = 'block'
    try:
        ## No caso de imagens
        document['F'+id].style.display = 'block'
    except:
        pass
    document[id].focus()

def handleInEnter(id):
    try:
        document[id].rows += 1
    except:
        pass

def handleEsc(id):
    document[id].style.display = 'none'
    try:
        ## No caso de imagens
        document['F'+id].style.display = 'none'
    except:
        pass
    document['co'+id].focus()

def handleInAltC(id):
    if not '#code <label>\n' in document[id].value:
        document[id].value = '#code <label>\n' + document[id].value

def handleInAltE(id):
    if not '!eq <label>\n' in document[id].value:
        document[id].value = '!eq <label>\n' + document[id].value

def handleInAlt1(id):
    if not '!# ' in document[id].value:
        document[id].value = '!# ' + document[id].value

def handleInAlt2(id):
    if not '!## ' in document[id].value:
        document[id].value = '!## ' + document[id].value

def handleInAlt3(id):
    if not '!### ' in document[id].value:
        document[id].value = '!### ' + document[id].value

def handleInAlt4(id):
    if not '!#### ' in document[id].value:
        document[id].value = '!#### ' + document[id].value

def handleInAlt5(id):
    if not '!##### ' in document[id].value:
        document[id].value = '!##### ' + document[id].value

def handleInAltT(id):
    if not '!tab ' in document[id].value:
        document[id].value = '!tab <label>\n' + document[id].value

def handleInAltB(id):
    if not '!- ' in document[id].value:
        document[id].value = '!- ' + document[id].value

def slider(ev):
    previewId = ev.target.id.replace('SL','P')
    print(document[previewId].style.width)
    document[previewId].style.width = str(int(float(ev.target.value)*800.0))+'px'

def previewImg(ev):
    window.previewImg(ev,'P'+ev.target.id)

def handleInAltI(id):
    global page,cellCounter
    if id == 'c0':
        upId = 0
    else:
        upId = page[page.index(id)-1]
    handleOutAltI(upId)
    handleShiftDelete(id)
    document[str(cellCounter-1)].focus()

def handleOutAltC(id):
    handleAltN(id)
    handleInAltC(nextId(id))
    
def handleOutAltE(id):
    handleAltN(id)
    handleInAltE(nextId(id))

def handleOutAlt1(id):
    handleAltN(id)
    handleInAlt1(nextId(id))

def handleOutAlt2(id):
    handleAltN(id)
    handleInAlt2(nextId(id))

def handleOutAlt3(id):
    handleAltN(id)
    handleInAlt3(nextId(id))

def handleOutAlt4(id):
    handleAltN(id)
    handleInAlt4(nextId(id))

def handleOutAlt5(id):
    handleAltN(id)
    handleInAlt5(nextId(id))

def handleOutAltT(id):
    handleAltN(id)
    handleInAltT(nextId(id))

def handleOutAltB(id):
    handleAltN(id)
    handleInAltB(nextId(id))

def handleOutAltI(id):
    global page,cellCounter
    print('calledAltI')
    id = id.replace('co','')
    newImageCell()
    print('Ended')
    print('insert after',id)
    print('cell',cellCounter-1)
    jq("#c"+str(cellCounter-1)).insertAfter("#co"+id)
    jq("#co"+str(cellCounter-1)).insertAfter("#c"+str(cellCounter-1))
    document[str(cellCounter-1)].focus()
    document[id].style.display = 'none'
    sendNewCell(page.index(id)+1)
    page.insert(str(page.index(id)+1),page.pop())

def newImageCell():
    global page,cellCounter
    try:
        id = str(cellCounter)
        newInImg = CENTER(FORM([INPUT(type="file",name='img',id=id),BR(),'Label:',INPUT(name='label',id="L"+id),BR(),'Caption:',INPUT(name='caption',id="C"+id),BR(),'Source:',INPUT(name='source',id="S"+id),BR(),'Width: ',INPUT(id="SL"+id,type="range",max="1",min="0",step="0.01",name='width'),BR(),IMG(id="P"+id,style={'width':'400px'})],id='F'+id,enctype="multipart/form-data",method="POST",action="image"),id="c"+id)
        newOutCell = CENTER(DIV(Class="paragraph", id='o'+id),id="co"+id,tabindex="0")
        document['page'] <= newInImg
        document['page'] <= newOutCell
        document['SL'+id].bind('change',slider)
        document[id].bind('change',previewImg)
        bindShortcuts(newInImg)
        bindOutShortcuts(newOutCell)
        newInImg.bind('blur',lastFocus)
        newOutCell.bind('blur',lastFocus)
        document[id].focus()
        page.append(id)
        cellCounter += 1
    except Exception as e:
        print('Exceptio: ',e)

cellCounter = 0
def newCell():
    global page,cellCounter
    id = str(cellCounter)
    newInCell = CENTER(TEXTAREA(style={'width':800,'height':200},id=id,action="evalCell"),id="c"+id,Class="dontprint")
    newOutCell = CENTER(DIV(Class="paragraph", id='o'+id),id="co"+id,tabindex="0")
    document['page'] <= newInCell
    document['page'] <= newOutCell
    bindShortcuts(newInCell)
    bindOutShortcuts(newOutCell)
    newInCell.bind('blur',lastFocus)
    newOutCell.bind('blur',lastFocus)
    document[id].focus()
    page.append(id)
    print(page)
    cellCounter += 1

def showCode(ev):
    id = ev.currentTarget.children[0].id[1:]
    print('Show code id ',id)
    document[id].style.display = 'block'
    
# To keep track of the right output cell
outIndex = None
def eval(id):
    # Handles the cell evaluation
    global outIndex,page
    outIndex = str(id)
    print('OutIndex ',outIndex)
    if document[id].tagName == 'TEXTAREA':
        content = document[id].value
        send(content)
        document[id].style.display = 'none'
    else:
        if document[id].files.length:
            img = document[id].files[0]
        else:
            img = None
        label = document['L'+id].value
        source = document['S'+id].value
        caption = document['C'+id].value
        width = document['SL'+id].value
        sendImg(img,label,source,caption,width)
        document['F'+id].style.display = 'none'
        document[id].style.display = 'none'
    print('submitted')
    
def bindShortcuts(element):
    element.bind('keydown',shortcuts)
    print('Binded ',element.id)

def bindOutShortcuts(element):
    element.bind('dblclick',showCode)
    element.bind('keydown',outShortcuts)

def receive(req):
    # Receiving the server handler output as req.text
    global outIndex
    try:
        print('Receiving...',outIndex)
        if req.status==200 or req.status==0:
            print('Received: ',req.text)
            if req.text[:12] == '!@StartRef@!' and '!@EndRef@!' in req.text:
                ref = getInside('!@StartRef@!','!@EndRef@!',req.text)
                req.text = req.text.replace('!@StartRef@!'+ref+'!@EndRef@!','')
                refCell = getInside('cell="','"',ref)
                ref = ref.replace('cell="'+refCell+'"','')
                if refCell:
                    document['o'+refCell].innerHTML =  ref
            document['o'+outIndex].innerHTML =  req.text
            updateSectionNumbers()
            updateTableNumbers()
            handleReferences()
            window.math.reNumber()
            #window.MathJax.Hub.Queue(["Typeset",window.MathJax.Hub])
            print('o'+outIndex)
    except Exception as e:
        print('Exception: ',e)

def receiveImg(req):
    # Receiving the server handler output as req.text
    global outIndex
    print('Receiving img...')
    try:
        print('Receiving...',outIndex)
        document['o'+outIndex].innerHTML = req
        updateFigureNumbers()
        updateTableNumbers()
        handleReferences()
        print('o'+outIndex)
    except Exception as e:
        print('Exception in recvImg: ',e)

def send(content):
    # Sends the cell content to the server handlers
    req = ajax.ajax()
    req.bind('complete',receive)
    req.open('POST','http://127.0.0.1:8080/evalCell',True)
    req.set_header('content-type','application/x-www-form-urlencoded')
    req.send({'docID':window.docID,'cell':page.index(outIndex),'content':content})

def sendImg(img,label,source,caption,width):
    print('Sending img...')
    window.uploadImg(window.docID,page.index(outIndex),img,label,source,caption,width)

def openFile(ev):
    toOpen = document['toOpen'].files[0]
    window.uploadFile(window.docID,toOpen)

def sendNewCell(index):
    print('New cell pending')
    req = ajax.ajax()
    req.bind('complete',ack)
    req.open('post','http://127.0.0.1:8080/newCell',True)
    req.set_header('content-type','application/x-www-form-urlencoded')
    req.send({'docID':window.docID,'index':index})

def sendDeleteCell(index):
    print('Delete cell pending')
    req = ajax.ajax()
    req.bind('complete',ack)
    req.open('post','http://127.0.0.1:8080/deleteCell',True)
    req.set_header('content-type','application/x-www-form-urlencoded')
    req.send({'docID':window.docID,'index':index})

def ack(req):
    print('ACKasd: ',req.text)
    try:
        if '!@StartRef@!' in req.text and '!@EndRef@!' in req.text:
            ref = getInside('!@StartRef@!','!@EndRef@!',req.text)
            req.text = req.text.replace('!@StartRef@!'+ref+'!@EndRef@!','')
            refCell = getInside('cell="','"',ref)
            ref = ref.replace('cell="'+refCell+'"','')
            if refCell:
                document['o'+refCell].innerHTML =  ref
        updateSectionNumbers()
        updateFigureNumbers()
        updateTableNumbers()
        handleReferences() # this order is important. If it comes after mathjax, the \ref command gets evalluated by it first
        window.math.reNumber()
    except:
        pass

def renderFile(req):
    global page,cellCounter
    del document['page']
    document <= DIV(id="page")
    page = []
    print('Done deleting')
    print('Received: ',req)
    try:
        document['page'].innerHTML +=  req
        cellCounter = 0
        while str(cellCounter) in document:
            print('Cell :',cellCounter)
            bindShortcuts(document['c'+str(cellCounter)])
            bindOutShortcuts(document['co'+str(cellCounter)])
            page.append(str(cellCounter))
            print(page)
            cellCounter += 1
        toBind = getAllInside('id="SL','"',req)
        for imgId in toBind:
            print('Binding to ',toBind[imgId])
            sliderID = 'SL'+toBind[imgId]
            document[sliderID].bind('change',slider)
            document[toBind[imgId]].bind('change',previewImg)
        newCell()
        updateSectionNumbers()
        updateFigureNumbers()
        updateTableNumbers()
        handleReferences() # this order is important. If it comes after mathjax, the \ref command gets evalluated by it first
        window.math.reNumber()
        #window.MathJax.Hub.Queue(["Typeset",window.MathJax.Hub])
        print('Done loading file')
    except Exception as e:
        print(e)

def focusNextCell(id):
    global page
    idDown = nextId(id)
    if document[idDown].style.display == 'none':
        document['co'+idDown].focus()
    else:
        document[idDown].focus()

def nextId(id):
    global page
    id = id.replace('c','').replace('o','')
    if page.index(id)+1 < len(page):
        return page[page.index(id)+1]
    else:
        return page[-1]

def updateSectionNumbers():
    global references
    def replaceNumber(content,tag,numbering):
        if '<span>' in content:
            heading = content[content.index('</span>'):]
            print('If: ',heading)
            return tag+'<span>'+numbering+heading
        else:
            heading = content.replace(tag,'')
            print('Else: ',heading)
            return tag+'<span>'+numbering+'</span>'+heading

    def clearHeading(html,endTag):
        '''Remove all after the endTag'''
        return html[:html.index(endTag)+len(endTag)]

    S,SS,SSS,SSSS,SSSSS = 0,0,0,0,0
    document['pannel'].html = ''
    for id in page:
        html = document['o'+id].html
        if html:
            if '<h1' in html:
                S+=1
                SS,SSS,SSSS,SSSSS = 0,0,0,0
                if 'id="' in html:
                    tag = '<h1'+getInside('<h1','>',html)+'>'
                    label = getInside('id="','"',html)
                    references['\\sec{'+label+'}'] = '<a href="#'+label+'">'+str(S)+'</a>'
                else:
                    tag = '<h1>'
                document['o'+id].html = replaceNumber(html,tag,str(S)+'. ')
                document['pannel'].html += '<a class="pannelItem" href="#o'+id+'">'+clearHeading(replaceNumber(html,tag,str(S)+'. '),'</h1>').replace(tag,'')+'</a><br>'
            elif '<h2' in html:
                SS+=1
                SSS,SSSS,SSSSS = 0,0,0
                if 'id="' in html:
                    tag = '<h2'+getInside('<h2','>',html)+'>'
                    label = getInside('id="','"',html)
                    references['\\sec{'+label+'}'] = '<a href="#'+label+'">'+str(S)+'.'+str(SS)+'</a>'
                else:
                    tag = '<h2>'
                document['o'+id].html = replaceNumber(html,tag,str(S)+'.'+str(SS)+'. ')
                document['pannel'].html += '<a class="pannelItem" href="#o'+id+'">'+clearHeading(replaceNumber(html,tag,str(S)+'. '+str(SS)+'. '),'</h2>').replace(tag,'')+'</a><br>'
            elif '<h3' in html:
                SSS+=1
                SSSS,SSSSS = 0,0
                if 'id="' in html:
                    tag = '<h3'+getInside('<h3','>',html)+'>'
                    label = getInside('id="','"',html)
                    references['\\sec{'+label+'}'] = '<a href="#'+label+'">'+str(S)+'.'+str(SS)+'.'+str(SSS)+'</a>'
                else:
                    tag = '<h3>'
                document['o'+id].html = replaceNumber(html,tag,str(S)+'.'+str(SS)+'.'+str(SSS)+'. ')
                document['pannel'].html += '<a class="pannelItem" href="#o'+id+'">'+clearHeading(replaceNumber(html,tag,str(S)+'. '+str(SS)+'. '+str(SSS)+'. '),'</h3>').replace(tag,'')+'</a><br>'
            elif '<h4' in html:
                SSSS+=1
                SSSSS = 0
                if 'id="' in html:
                    tag = '<h4'+getInside('<h4','>',html)+'>'
                    label = getInside('id="','"',html)
                    references['\\sec{'+label+'}'] = '<a href="#'+label+'">'+str(S)+'.'+str(SS)+'.'+str(SSS)+'.'+str(SSSS)+'</a>'
                else:
                    tag = '<h4>'
                document['o'+id].html = replaceNumber(html,tag,str(S)+'.'+str(SS)+'.'+str(SSS)+'.'+str(SSSS)+'. ')
                document['pannel'].html += '<a class="pannelItem" href="#o'+id+'">'+clearHeading(replaceNumber(html,tag,str(S)+'. '+str(SS)+'. '+str(SSS)+'. '+str(SSSS)+'. '),'</h4>').replace(tag,'')+'</a><br>'
            elif '<h5' in html:
                SSSSS+=1
                if 'id="' in html:
                    tag = '<h5'+getInside('<h5','>',html)+'>'
                    label = getInside('id="','"',html)
                    references['\\sec{'+label+'}'] = '<a href="#'+label+'">'+str(S)+'.'+str(SS)+'.'+str(SSS)+'.'+str(SSSS)+'.'+str(SSSSS)+'</a>'
                else:
                    tag = '<h5>'
                document['o'+id].html = replaceNumber(html,tag,str(S)+'.'+str(SS)+'.'+str(SSS)+'.'+str(SSSS)+'.'+str(SSSSS)+'. ')
                document['pannel'].html += '<a class="pannelItem" href="#o'+id+'">'+clearHeading(replaceNumber(html,tag,str(S)+'. '+str(SS)+'. '+str(SSS)+'. '+str(SSSS)+'. '+str(SSSSS)+'. '),'</h5>').replace(tag,'')+'</a><br>'
                
def updateFigureNumbers():
    global references
    def replaceNumber(content,tag,numbering):
        print('Content: ',content)
        if '<span>' in content:
            caption = content[content.index('</span>'):]
            print('If: ',caption)
            return '<br><center>'+tag+'<span>'+numbering+caption
        else:
            caption = content[content.index(tag)+len(tag):]
            print('Else: ','<center>'+tag+'<span>'+numbering+'</span>'+caption)
            return '<br><center>'+tag+'<span>'+numbering+'</span>'+caption

    N = 0
    for id in page:
        html = document['o'+id].html
        if html:
            if '<figcaption' in html:
                N+=1
                if 'id="' in html:
                    label = getInside('id="','"',html)
                    references['\\fig{'+label+'}'] = '<a href="#'+label+'">'+str(N)+'</a>'
                    tag = '<figcaption id="'+label+'">'
                    print('tem id')
                else:
                    tag = '<figcaption>'
                document['o'+id].html = replaceNumber(html,tag,'<b>Fig. '+str(N)+':</b> ')

def updateTableNumbers():
    global references
    def replaceNumber(content,tag,numbering):
        print('Content: ',content)
        if '<span>' in content:
            caption = content[content.index('</span>'):]
            print('If: ',caption)
            return '<br><center>'+tag+'<span>'+numbering+caption
        else:
            caption = content[content.index(tag)+len(tag):]
            print('Else: ','<center>'+tag+'<span>'+numbering+'</span>'+caption)
            return '<br><center>'+tag+'<span>'+numbering+'</span>'+caption

    N = 0
    for id in page:
        html = document['o'+id].html
        if html:
            if 'class="tableCaption"' in html:
                N+=1
                if 'id="' in html:
                    label = getInside('id="','"',html)
                    references['\\tab{'+label+'}'] = '<a href="#'+label+'">'+str(N)+'</a>'
                    tag = '<div class="tableCaption" id="'+label+'">'
                    print('tem id')
                else:
                    tag = '<div class="tableCaption">'
                document['o'+id].html = replaceNumber(html,tag,'<b>Table '+str(N)+':</b> ')

references = {}
def handleReferences():
    global references
    def updateRef(html):
        # First update the old ones
        for ref in references:
            print('No ref: ',ref)
            if '\\eq{' in ref:
                command = '\\eq{'
            elif '\\sec{' in ref:
                command = '\\sec{'
            elif '\\fig{' in ref:
                command = '\\fig{'
            elif '\\tab{' in ref:
                command = '\\tab{'
            else:
                print('something went wrong with ref')
                continue
            label = getInside(command,'}',ref)
            reference = '<a href="#'+label+'">'
            if reference in html:
                number = getInside(reference,'</a>',html)
                html = html.replace(reference+number+'</a>', references[command+label+'}'])
                document['o'+id].html = html

    def interpreteRef(command,html):
        # Now generate the new ones
        toRef = getAllInside(command,'}', html)
        for expr in toRef:
            if expr in references:
                html = html.replace(expr,references[expr])
            else:
                label = getInside(command,'}',expr)
                ref = '<a href="#'+label+'">???</a>'
                references[expr] = ref
                html = html.replace(expr, ref)
        document['o'+id].html = html

    for id in page:
        html = document['o'+id].html
        if '<a href="#' in html:
            updateRef(html)
        if '\\fig{' in html:
            interpreteRef('\\fig{',html)
        if '\\eq{' in html:
            document['o'+id].html = html.replace('\\eq{','\\ref{')
            print('replaced eq')
        if '\\sec{' in html:
            interpreteRef('\\sec{',html)
        if '\\tab{' in html:
            interpreteRef('\\tab{',html)
            
            

# Initialize the first cell
page = []
newCell()
document['openButton'].bind('click',openFile)
window.receiveImg = receiveImg
window.renderFile = renderFile
