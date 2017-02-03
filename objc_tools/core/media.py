from ctypes import Structure, c_int32, c_int64, c_uint32, c_double
from objc_util import c
from enum import Enum

class CMTimeFlags (Enum):
    Valid = 1<<0
    HasBeenRounded = 1<<1
    PositiveInfinity = 1<<2
    NegativeInfinity = 1<<3
    Indefinite = 1<<4
    ImpliedValueFlagsMask = PositiveInfinity | NegativeInfinity | Indefinite

class CMTime (Structure):
    '''A Handler for CMTime Structures
    DO NOT CALL DIRECTLY use CMTimeMake
    '''
    
    _fields_ = [('CMTimeValue', c_int64),
                ('CMTimeScale', c_int32),
                ('CMTimeFlags', c_uint32),
                ('CMTimeEpoch', c_int64)]
    
    @property
    def seconds(self):
        '''Return the object as seconds'''
        return self.CMTimeValue / self.CMTimeScale
        
    @seconds.setter
    def seconds(self, time):
        self.CMTimeValue = time * self.CMTimeScale
    
    @property
    def flags(self):
        returns = []
        for i in CMTimeFlags:
            if self.CMTimeFlags & i.value:
                returns += [i]
        return returns
    
    @flags.setter
    def flags(self, nil):
        pass
        
    def __repr__(self):
        return '<CMTime value: {tvalue}, Scale: {tscale}>'.format(tvalue=self.CMTimeValue, tscale=self.CMTimeScale)
        
    def __add__(self, other):
        return CMTimeAdd(self, other)
        
    def __sub__(self, other):
        return CMTimeSubtract(self, other)
        
    def __mul__(self, other):
        return CMTimeMultiplyByFloat64(self, other)
        
    def __truediv__(self, other):
        return self * (1/other)
        
    def __eq__(self, other):
        if CMTimeCompare(self, other) == 0:
            return True
        else:
            return False
            
    def __lt__(self, other):
        if CMTimeCompare(self, other) == -1:
            return True
        else:
            return False
        
    def __le__(self, other):
        if CMTimeCompare(self, other) <= 0:
            return True
        else:
            return False
    
    def __gt__(self, other):
        if CMTimeCompare(self, other) == 1:
            return True
        else:
            return False
            
    def __ge__(self, other):
        if CMTimeCompare(self, other) >= 0:
            return True
        else:
            return False
    
    def __bool__(self):
        '''Return True if the CMTime is valid'''
        if CMTimeFlags.Valid in self.flags:
            return True
        else:
            return False
                
def CMTimeMake(value, scale = 90000):
    '''Make a CMTime
       :param value: The numerator of the resulting CMTime.
       :param scale: The denomenator of the resulting CMTime.
       :rtype: 
       '''
    CMTimeMake = c.CMTimeMake
    CMTimeMake.argtypes = [c_int64, c_int32]
    CMTimeMake.restype = CMTime
    return CMTimeMake(value, scale)

CMTimeMakeWithSeconds = c.CMTimeMakeWithSeconds
CMTimeMakeWithSeconds.argtypes = [c_double, c_int32]
CMTimeMakeWithSeconds.restype = CMTime

CMTimeMultiplyByFloat64 = c.CMTimeMultiplyByFloat64
CMTimeMultiplyByFloat64.argtypes = [CMTime, c_double]
CMTimeMultiplyByFloat64.restype = CMTime

CMTimeAdd = c.CMTimeAdd
CMTimeAdd.argtypes = [CMTime, CMTime]
CMTimeAdd.restype = CMTime

CMTimeSubtract = c.CMTimeSubtract
CMTimeSubtract.argtypes = [CMTime, CMTime]
CMTimeSubtract.restype = CMTime

CMTimeConvertScale = c.CMTimeConvertScale
CMTimeConvertScale.argtypes = [CMTime, c_int32]
CMTimeConvertScale.restype = CMTime

CMTimeMultiplyByRatio = c.CMTimeMultiplyByRatio
CMTimeMultiplyByRatio.argtypes = [CMTime, c_int32, c_int32]
CMTimeMultiplyByRatio.restype = CMTime

CMTimeCompare = c.CMTimeCompare
CMTimeCompare.argtypes = [CMTime, CMTime]
CMTimeCompare.restype = c_int32

def objc_CMTime(struct):
    '''Converts the AnonymousStructure fromn the returns of some objc functions'''
    return CMTime(struct.a, struct.b, struct.c, struct.d)
