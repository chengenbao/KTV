#!/usr/bin/python3

from os import path
import time

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gst, Gtk
# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo




class stv_video_player_class(object):
    def __init__(self, obj, obj_hook):
        GObject.threads_init()
        Gst.init(None)

        self.pipeline = Gst.Pipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::error', self.on_error)

        # This is needed to make the video output in our DrawingArea:
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)

        self.playbin = Gst.ElementFactory.make('playbin', None)
        self.pipeline.add(self.playbin)

        self.state = Gst.State.NULL

        self.obj = obj
        self.obj_hook = obj_hook

    # def change_area(self, area):
    #     self.pipeline.set_state(Gst.State.PAUSED)
    #     # self.bus.remove_watch()
    #     self.bus.disable_sync_message_emission()
    #     self.xid = area.get_window().get_xid()
    #     self.bus.enable_sync_message_emission()
    #     self.cur_pos = self.pipeline.query_position(Gst.Format.TIME)[1]
    #     # self.pipeline.set_state(Gst.State.NULL)
    #     print('Pause: ', self.cur_pos)
    #     # seek_ns = self.cur_pos - 10 * 1000000000
    #     # if seek_ns < 0:
    #     #     seek_ns = 0
    #     # print('Seek_ns: ', seek_ns)
    #     # self.pipeline.set_state(Gst.State.READY)
    #     # self.pipeline.seek_simple(Gst.Format.TIME, Gst.SeekFlags.SNAP_BEFORE, seek_ns)
    #     # time.sleep(1)
    #     print('Sleep OK')
    #     self.pipeline.set_state(Gst.State.PLAYING)
    #     self.pipeline.seek_simple(Gst.Format.TIME, Gst.SeekFlags.SNAP_BEFORE, self.cur_pos)
    #     self.pipeline.set_state(Gst.State.PAUSED)
    #     self.cur_pos = self.pipeline.query_position(Gst.Format.TIME)[1]
    #     print('Seeked: ', self.cur_pos)
    #     # self.pipeline.set_state(Gst.State.READY)
    #     # self.pipeline.seek_simple(Gst.Format.TIME, Gst.SeekFlags.SNAP_BEFORE, self.cur_pos)
    #     # self.cur_pos = self.pipeline.query_position(Gst.Format.TIME)[1]
    #     # print(self.cur_pos)
    #     # print(self.xid)

    def pause(self):
        srt, st, stp = self.pipeline.get_state(Gst.CLOCK_TIME_NONE)
        if Gst.State.PLAYING == st:
            self.pipeline.set_state(Gst.State.PAUSED)
            self.state = Gst.State.PAUSED
        else:
            return None

    def play(self):
        srt, st, stp = self.pipeline.get_state(Gst.CLOCK_TIME_NONE)
        if Gst.State.PLAYING == st:
            return None
        else:
            self.pipeline.set_state(Gst.State.PLAYING)
            self.state = Gst.State.PLAYING

    def ready(self, filepath):
        self.pipeline.set_state(Gst.State.NULL)
        self.xid = self.area.get_window().get_xid()
        self.uri = 'file://' + filepath
        self.playbin.set_property('uri', self.uri)
        self.state = Gst.State.PAUSED

    def set_xid(self, area):
        '''
        # self.window.show_all()
        # You need to get the XID after window.show_all().  You shouldn't get it
        # in the on_sync_message() handler because threading issues will cause
        # segfaults there.
        # self.xid = self.disp_area.get_property('window').get_xid()
        '''
        self.area = area
        self.xid = area.get_window().get_xid()

    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)

    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            # print('prepare-window-handle')
            msg.src.set_window_handle(self.xid)

    def on_eos(self, bus, msg):
        self.obj_hook(self.obj)
        # self.stop()
        # print('on_eos(): seeking to start of video')
        # self.pipeline.seek_simple(
        #     Gst.Format.TIME,
        #     Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
        #     0
        # )

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())

if __name__ == '__main__':
    pass
