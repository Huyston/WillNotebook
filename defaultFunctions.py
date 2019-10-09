import os

def section(text):
    '''This is a test notebook python function'''
    print("<h1>"+text+"</h1>")

def msg(msg):
    return '<font class="msg dontprint">'+msg+'</font>'

def error(msg):
    return '<font class="error dontprint">'+msg+'</font>'

def plot(xlines,ylines,labels=None,colors=None,styles=None,widths=None,xlabel=None,ylabel=None,caption='',name='',plotWidth=800,source=''):
    global docID
    if name == '':
        print(msg("Please give this plot a name."))
        return
    try:
        import matplotlib.pyplot as p
    except:
        print(msg("You dont have matplotlib installed. Please install it and try again."))
    if type(xlines[0]) == list:
        plots = len(xlines)
        if labels == None:
            labels = [None]*plots
        if colors == None:
            colors = [None]*plots
        if styles == None:
            styles = [None]*plots
        if widths == None:
            widths = [None]*plots
        for xline,yline,label,color,style,width in zip(xlines,ylines,labels,colors,styles,widths):
            p.plot(xline,yline,label=label,linewidth=width,color=color,linestyle=style)
        if any(labels):
            p.legend(loc='best')
        p.grid()
        path = 'Archieves/'+docID+'/Images/'+name+'.png'
        try:
            os.mkdir(os.getcwd()+'/Archieves/'+docID)
        except FileExistsError:
            pass
        try:
            os.mkdir(os.getcwd()+'/Archieves/'+docID+'/Images')
        except FileExistsError:
            pass
        p.savefig(path)
        print('<br><center><figcaption>'+caption+'</figcaption>'+'<img style="width:'+str(plotWidth)+'" src="'+path+'"><br>Source: '+source+'</center><br>')
