from appJar import gui
from MXDRV import MXDRV
app = MXDRV()
gui = gui(title="X68000 MDX Manager")

def search(self):
    q = gui.getEntry("Query")
    if not q or q=="":
        return
    res = app.search(q)
    if not res:
        gui.errorBox("No results", "Couldn't find anything for '{}'. Try rescanning...".format(q))
    else:
        gui.deleteAllTableRows("Songs")
        gui.replaceAllTableRows("Songs",[[v.filename,v.name,v.path] for v in res])
    return    

def rescan(self):
    c = app.scan_library()
    gui.showinfo("Scan complete","Indexed {} songs in {}".format(c['count'],str(c['time']).split('.')[0]))
    return

gui.addButton("Rescan Library",rescan,row=0,column=0)
gui.addLabelEntry("Query",row=0,column=3)
gui.addButton("Search",search,row=0,column=4)
gui.addTable("Songs",[["Filename","Name","Path"]],row=1,colspan=5)

gui.setSize(720,320)
gui.go()
