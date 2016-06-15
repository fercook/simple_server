import tornado.ioloop
import tornado.web
import os.path
import logging
import datetime
import uuid
import base64

__UPLOADS__ = "marenostrum/uploads/"
__SCORES__ = "marenostrum/scores/"
__MIDIS__ = "marenostrum/midi/"
class HitAndShitHandler(tornado.web.RequestHandler): # From Hit/Shit main page
    def get(self):
        self.render("client/ikerealm/hitAndShit.html");

class ComposerHitOrShitHandler(tornado.web.RequestHandler):
    def get(self):
	   self.render("client/musiccomposer/index_HorS.html")

class DrawingMusic(tornado.web.RequestHandler):
    def get(self):
        self.render("client/ikerealm/drawingmusic.html");

class MIDISupply(tornado.web.RequestHandler):
    def get(self):
        self.render("client/midisupply.html");

class MusicComposer(tornado.web.RequestHandler):
    def get(self):
	   self.render("client/musiccomposer/index.html");

class ScoreSongHandler(tornado.web.RequestHandler): # From Hit/Shit main page
    def get(self):
        #self.write("ScoreSongHandler")
        cname = str(uuid.uuid4()) + '.score'
        fh = open(__SCORES__ + cname, 'w')
        songID = self.get_argument("id")
        songScore = self.get_argument("score","0")
        songSource = self.get_argument("source")
        fh.write(songID+" "+songScore+" "+songSource+" "+str(datetime.datetime.now()))
        #self.finish(cname + " was uploaded!!")
        #self.write("song id: "+songID+" score: "+songScore)
        if (songSource=="composer"):
                self.render("client/musiccomposer/index.html");
        else:
                self.render("client/ikerealm/drawingmusic.html");

class GetSongsHandler(tornado.web.RequestHandler): # From Hit/Shit main page
    def get(self):
        fileName= os.path.dirname(__file__)+__MIDIS__+'latest_midi_set.zip'
        if not os.path.isfile(fileName):
            raise HTTPError(404)
        self.set_header('Content-Type', 'application/force-download')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % fileName) 
        with open(fileName, 'rb') as f:
            try:
                data = f.read()
                if (data):
                    self.write(data)
                f.close()
                self.finish()
                return
            except:
                raise HTTPError(404)
        raise HTTPError(500)
            #audio/rtp-midi #application/octet-stream
        print('GetSongs: ',datetime.datetime.now())
        self.set_header('Content-Type','application/octet-stream')
        self.set_header('files','latest_midi_set.zip')
        self.write(data)
        self.finish()
        #print(data)

class SaveSongHandler(tornado.web.RequestHandler): # From drawing or composer apps
    def post(self):
        self.write("SaveSongHandler")
        #fileinfo = self.request.files['filearg'][0]
        #fname = fileinfo['filename']
        data = self.request.body
        cname = str(uuid.uuid4()) + '.mid'
        fh = open(__UPLOADS__ + cname, 'wb')
        fh.write(base64.b64decode(data.replace("data:image/png;base64,", "")))
        self.finish(cname + " is uploaded!! Check %s folder" %__UPLOADS__)
        #filedata = fileinfo['body']
        #print(fname+'  '+filedata[:100])

        #print('REQ: ',self.request.body)


settings = {
    "debug": True,
    "static_path": os.path.join(os.path.dirname(__file__), "client")
}

def make_app():
    return tornado.web.Application(handlers=[
        (r"/hitorshit", HitAndShitHandler),
        (r"/composerhitorshit", ComposerHitOrShitHandler),
	    (r"/drawingmusic", DrawingMusic),
        (r"/score-song", ScoreSongHandler),
        (r"/get-songs", GetSongsHandler),
        (r"/save-song", SaveSongHandler),
        (r"/midisupply", MIDISupply),
	    (r"/musiccomposer", MusicComposer),
        ],**settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
