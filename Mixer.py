from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume



def getDevices():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    sessions = AudioUtilities.GetAllSessions()

    # for session in sessions:
    #     volume = session._ctl.QueryInterface(ISimpleAudioVolume)
    #     if session.Process:
    #         print(session.Process.name())
    return sessions

if __name__ == "__main__":
    getDevices()
