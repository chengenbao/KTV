#!/usr/python3

from urllib import request, error, parse
import shutil, json, os, logging
from yinyuetai import yyt_api_class as yyt_api

class stv_request_class(object):
    def __init__(self, uri, machine):
        self.uri = uri
        self.machine = machine
        self.online = False
        self.seq = '0000000000'
        self.api = yyt_api()
        # Must be changed by self.sequence_init() before the others requests.

    def network_check(func):
        def wrapper(*args, **kw):
            req = args[0]
            try:
                retval = func(*args, **kw)
                req.online = True
                return retval
            except error.HTTPError as e1:
                logging.warning(e1)
                req.online = False
            except error.URLError as e2:
                logging.warning(e2)
                req.online = False
        return wrapper

    @network_check
    def open_url(self, url):
        with request.urlopen(url) as f:
            return json.loads(f.read().decode('utf-8'))

    def sequence_init(self, seq):
        self.seq = seq
        url = self.uri + '/sequence/init/%s/%s' % (self.machine, seq)
        return self.open_url(url)

    def instruction_fetch(self):
        url = self.uri + '/playcontrol/fetch/%s/%s' % (self.seq, self.machine)
        return self.open_url(url)

    def praise_fetch(self, song_id):
        url = self.uri + '/praise/fetch/%s/%s/%s' % (self.seq, self.machine, song_id)
        return self.open_url(url)

    def play_list_fetch(self):
        url = self.uri + '/playlist/fetch/%s/%s' % (self.seq, self.machine)
        return self.open_url(url)

    def his_list_fetch(self):
        url = self.uri + '/history/fetch/%s/%s' % (self.seq, self.machine)
        return self.open_url(url)

    def play_list_move(self, song_id):
        url = self.uri + '/playlist/resort/%s/%s/%s/2' % (self.seq, self.machine, song_id)
        return self.open_url(url)

    def play_list_add(self, song_id):
        url = self.uri + '/playlist/add/%s/%s/%s' % (self.seq, self.machine, song_id)
        return self.open_url(url)

    def play_list_remove(self, song_id):
        url = self.uri + '/playlist/delete/%s/%s/%s' % (self.seq, self.machine, song_id)
        return self.open_url(url)

    def top_fetch(self, top_type):
        if 'guess' == top_type:
            url = self.uri + '/recommendation/%s/%s' % (self.seq, self.machine)
        else:
            url = self.uri + '/top/%s' % (top_type)
        return self.open_url(url)

    def comment_fetch(self, song_id):
        url = self.uri + '/comment/fetch/%s' % (song_id)
        return self.open_url(url)

    def search_singer_by_fullname(self, key):
        key = parse.quote(key.encode('utf-8')) # Solved Unicode URL
        url = self.uri + '/search/fullname/singer/%s' % (key)
        return self.open_url(url)

    def search_singer_by_abridge(self, key):
        key = parse.quote(key.encode('utf-8'))
        url = self.uri + '/search/abbreviation/singer/%s' % (key)
        return self.open_url(url)

    def search_song_by_fullname(self, key):
        key = parse.quote(key.encode('utf-8'))
        url = self.uri + '/search/fullname/song/%s' % (key)
        return self.open_url(url)

    def search_song_by_abridge(self, key):
        key = parse.quote(key.encode('utf-8'))
        url = self.uri + '/search/abbreviation/song/%s' % (key)
        return self.open_url(url)

    def singer_song_fetch(self, singer_id):
        url = self.uri + '/singer/fetch/%s' % (singer_id)
        return self.open_url(url)

    @network_check
    def download(self, song_id, directory = '/tmp/stv/mv'):
        retval = os.path.isdir(directory)
        if not retval:
            os.mkdir(directory)

        url = self.uri + '/download/mv/%s' % (song_id)
        path = os.path.join(directory, song_id)
        with request.urlopen(url) as f:
            header = dict(f.getheaders())
            length = int(header['Content-Length'])
            if 4 == length:
                return None

            with open(path, 'wb') as out_file:
                shutil.copyfileobj(f, out_file)

        return path

    @network_check
    def album_fetch(self, star_id, directory = '/tmp/stv/album'):
        retval = os.path.isdir(directory)
        if not retval:
            os.mkdir(directory)

        url = self.uri + '/download/album/%s' % (star_id)
        path = os.path.join(directory, star_id)
        with request.urlopen(url) as f:
            header = dict(f.getheaders())
            length = int(header['Content-Length'])
            if 4 == length:
                return None

            with open(path, 'wb') as out_file:
                shutil.copyfileobj(f, out_file)

        return path

if __name__ == '__main__':
    req = stv_request_class('http://localhost:5000', '2')
    req.album_fetch('2')
