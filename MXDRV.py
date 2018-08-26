import sqlite3
import json
from Song import Song
import subprocess
from scanner import scan

class MXDRV:
	offset = 0
	playing = None
	def __init__(self):
		cfg = json.loads(open("config.json","r").read())
		self.player_path = cfg['player_path']
		self.folders = cfg['library_folders']
		try:
			dbfile = cfg['database']
		except:
			dbfile = "mxdrv.db"
		try:
			self.folders = cfg['library_folders']
		except:
			print('No mdx folders specified')
			exit()
		if len(self.folders)<1:
			print('No mdx folders specified')
			exit()
		self.dbfile = dbfile
		self.cfg = cfg
		self.conn = sqlite3.connect(dbfile)
		self.db = self.conn.cursor()
		self.db.execute("""
		CREATE TABLE IF NOT EXISTS `songs`(
		`filename`	TEXT DEFAULT NULL,
		`name`	TEXT DEFAULT NULL,
		`path`	TEXT DEFAULT NULL);
		""")
	
	def get_songs(self,limit=50):
		self.offset+=limit
		self.db.execute("SELECT name,filename,path FROM songs LIMIT ? OFFSET ?",(limit,self.offset,))
		rs = self.db.fetchall()
		if rs:
			ret=[]
			for i in rs:
				ret.append(Song(rs[i][0],rs[i][1],rs[i][2]))
			return ret

	def search(self,q):
		self.db.execute("SELECT name,filename,path FROM songs WHERE name LIKE '%{q}%' OR filename LIKE '%{q}%'".format(**{'q':q}))
		rs = self.db.fetchall()
		if rs:
			print('Found {} song(s) for term {}'.format(len(rs),q))
			ret=[]
			for i in rs:
				ret.append(Song(i[0],i[1],i[2]))
			return ret			
	
	def song_count(self):
		self.db.execute("SELECT count(*) FROM songs")
		return self.db.fetchone()[0]

	def play(self,song):
		if self.playing:
			self.playing.terminate()
			self.playing = None
		self.playing = subprocess.Popen("{} {}".format(self.player_path,song.path))
		print('Now playing {}'.format(song.name))
		return 1

	def stop(self):
		if self.playing:
			self.playing.terminate()
			self.playing = None
			print('Stopped playing')
			return 1
		print('Nothing playing')
		return

	def scan_library(self):
		c = scan(self)
		print('Indexed {} songs in {}'.format(c['count'],str(c['time']).split('.')[0]))
		return c
