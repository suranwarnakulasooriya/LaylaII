import time

class Stopwatch:
    def __init__(self):
        self.start = 0
        self.suspend = 0
        self.downtime = 0
        self.paused = False
    def Start(self):
        if not self.paused: self.start = time.time()
    def Pause(self):
        if not self.paused: self.suspend = time.time(); self.paused = True
    def Resume(self):
        if self.paused:
            self.downtime += time.time()-self.suspend
            self.suspend = 0; self.paused = False
    def GetTime(self):
        return int(time.time()-self.downtime-self.start)
    def Reset(self):
        self.start = 0
        self.suspend = 0
        self.downtime = 0
        self.paused = False

stopwatch = Stopwatch()
print(type(stopwatch))
input('press enter to start')
stopwatch.Start()
input('press enter to pause')
stopwatch.Pause()
input('press enter to resume')
stopwatch.Resume()
input('press enter to stop')
print(stopwatch.GetTime())
print(type(stopwatch.GetTime()))
stopwatch.Reset()
