import appJar
import json
from MXDRV import MXDRV
app = MXDRV()
gui = appJar.gui(title="X68000 MDX Manager")
dirs=[]

def search():
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

def rescan():
    c = app.scan_library()
    gui.infoBox("Scan complete","Indexed {} songs in {}".format(c['count'],str(c['time']).split('.')[0]))
    return

def add_dir():
    d = gui.directoryBox(title="Add folder", parent="set")
    dirs.append(d)
    gui.addTableRow("dirs",d)

def save(dirs):
    d = dirs+app.folders
    app.cfg['library_folders']=d
    if not gui.getEntry("Database")=="":
        app.cfg['database']=gui.getEntry("Database")
    with open("config.json","w") as f:
        f.seek(0)
        f.write(json.dumps(app.cfg))
        f.truncate()
        dirs=[]
        gui.infoBox("Done","Config updated")
    gui.hideSubWindow("set")


gui.addButton("Rescan Library",rescan,row=0,column=0)
gui.addButton("Settings",lambda settings:[gui.replaceAllTableRows("dirs",app.folders),gui.showSubWindow("set")],row=0,column=1)
gui.addLabelEntry("Query",row=0,column=3)
gui.addButton("Search",search,row=0,column=4)
gui.addTable("Songs",[["Filename","Name","Path"]],row=1,colspan=5)

gui.startSubWindow("set", modal=True)
gui.addLabelEntry("Database",row=0,column=0)
gui.setEntryDefault("Database",app.dbfile)
gui.addButton("Add folder",add_dir)
gui.addTable("dirs",[["Path"],[app.folders]])
gui.addButtons(["OK","Cancel"],[lambda s: save(dirs),lambda exit: gui.hideSubWindow("set")])
gui.stopSubWindow()

gui.setSize(720,320)
gui.go()
