from objc_util import c_void_p, c_int, c, c_bool, NSString, ObjCBlock, c_char_p, ObjCClass, c_long, c_ulong, nsdata_to_bytes
from objc_tools.c.objc_handler import chandle
from objc_tools.backports.enum_backport import IntEnum
from objc_tools.c import dispatch
from sys import modules
from time import time
from plistlib import loads
from datetime import datetime
from io import BytesIO
import Image

global nowplaying
nowplaying = None

class Commands (IntEnum):
    kMRPlay = 0
    kMRPause = 1
    kMRTogglePlayPause = 2
    kMRStop = 3
    kMRNextTrack = 4
    kMRPreviousTrack = 5
    kMRToggleShuffle = 6
    kMRToggleRepeat = 7
    kMRStartForwardSeek = 8
    kMREndForwardSeek = 9
    kMRStartBackwardSeek = 10
    kMREndBackwardSeek = 11
    kMRGoBackFifteenSeconds = 12
    kMRSkipFifteenSeconds = 13
    

MRMediaRemoteGetNowPlayingInfo = c.MRMediaRemoteGetNowPlayingInfo
MRMediaRemoteGetNowPlayingInfo.argtypes = [c_void_p, ObjCBlock]

MRMediaRemoteGetNowPlayingApplicationIsPlaying = c.MRMediaRemoteGetNowPlayingApplicationIsPlaying
MRMediaRemoteGetNowPlayingApplicationIsPlaying.argtypes = [c_void_p, ObjCBlock]

MRMediaRemoteSendCommand = c.MRMediaRemoteSendCommand
MRMediaRemoteSendCommand.argtypes = [c_int, c_void_p]
MRMediaRemoteSendCommand.restype = c_bool

MRMediaRemoteUnregisterForNowPlayingNotifications = c.MRMediaRemoteUnregisterForNowPlayingNotifications
MRMediaRemoteUnregisterForNowPlayingNotifications.argtypes = []
MRMediaRemoteUnregisterForNowPlayingNotifications.restype = None

MRMediaRemoteRegisterForNowPlayingNotifications = c.MRMediaRemoteRegisterForNowPlayingNotifications
MRMediaRemoteRegisterForNowPlayingNotifications.argtypes = []

MRMediaRemoteCopyPickableRoutes = c.MRMediaRemoteCopyPickableRoutes
MRMediaRemoteCopyPickableRoutes.restype = c_void_p

q=dispatch.dispatch_get_global_queue(0, 0)

def routes():
    MRMediaRemoteCopyPickableRoutes = c.MRMediaRemoteCopyPickableRoutes
    MRMediaRemoteCopyPickableRoutes.argtypes = []
    MRMediaRemoteCopyPickableRoutes.restype = c_void_p
    MRMediaRemoteCopyPickableRoutes.errcheck = chandle
    return MRMediaRemoteCopyPickableRoutes()

def route_has_volume_control():
    MRMediaRemotePickedRouteHasVolumeControl = c.MRMediaRemotePickedRouteHasVolumeControl
    MRMediaRemotePickedRouteHasVolumeControl.argtypes = []
    MRMediaRemotePickedRouteHasVolumeControl.restype = c_bool
    return MRMediaRemotePickedRouteHasVolumeControl()
    

class Nowplaying (object):
    def __init__(self):
        self._nowplaying = None
        self.timestamp = None
    
    def get(self, block = True, timeout=1):
        #handler = ObjCBlock(handle, argtypes=[c_void_p, c_void_p])
        MRMediaRemoteGetNowPlayingInfo(queue, handler)
        this = modules[__name__]
        
        if block:
            ctime = time()
            while (self._nowplaying == None or self._nowplaying == this.nowplaying) and (time() - ctime < timeout):
                self._nowplaying = this.nowplaying
            self.timestamp = datetime.now()
        else:
            self._nowplaying = this.nowplaying
            self.timestamp = datetime.now()
    
    @property
    def nowplaying(self):
        if self._nowplaying.ptr:
            b = nsdata_to_bytes(self._nowplaying.plistData())
            data = loads(b)
            # striping the prefix from items
            for i in data:
                data[i.replace('kMRMediaRemoteNowPlayingInfo','')] = data.pop(i)
            return data
        else:
            return None
            
    @property
    def image(self):
        if 'ArtworkData' in self.nowplaying.keys():
            f = BytesIO(self.nowplaying['ArtworkData'])
            return Image.open(f)
        else:
            return None
            

def bhandle(_cmd, d):
        global  nowplaying
        nowplaying = chandle(d, None, None)
        
        
queue = dispatch.dispatch_get_global_queue(0, 0)
MRMediaRemoteGetNowPlayingInfo = c.MRMediaRemoteGetNowPlayingInfo
MRMediaRemoteGetNowPlayingInfo.argtypes = [c_void_p, ObjCBlock]
handler = ObjCBlock(bhandle, argtypes=[c_void_p, c_void_p])


def update_global():
    MRMediaRemoteGetNowPlayingInfo(queue, handler)


def set_route(route, pw):
    MRMediaRemoteSetPickedRouteWithPassword = c.MRMediaRemoteSetPickedRouteWithPassword
    MRMediaRemoteSetPickedRouteWithPassword.argtypes=[c_void_p, c_void_p]
    MRMediaRemoteSetPickedRouteWithPassword(ns(route).ptr, ns(pw).ptr)
    

if __name__ == '__main__':    
    n=Nowplaying()
    n.get(True)

