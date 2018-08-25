import os
from Song import Song
from datetime import datetime

def scan(MXDRV):
    MXDRV.db.execute("DELETE FROM songs")
    t1 = datetime.now()
    count=0
    for p in MXDRV.folders:
        for path, dirs, files in os.walk(p):
            for file in files:
                p = os.path.join(path,file)
                s = parse(p,file)
                if s:
                    MXDRV.db.execute("INSERT INTO songs(filename,name,path) values(?,?,?)",(s.filename,s.name,s.path,))
                    count+=1
    MXDRV.conn.commit()
    t2 = datetime.now()
    return {'count':count,'time':t2-t1}

def parse(path,f):
    if path.endswith("MDX") or path.endswith("mdx"):
        name = getname(open(path,"rb").read())
        return Song(name,f,path)
        
def getname(p):
    return p.split(b'\x0d\x0a\x1a')[0].decode('shift-jis',errors='ignore')

