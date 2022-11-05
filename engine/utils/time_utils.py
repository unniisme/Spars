#Class to hold all functions of time
class Time:
    """
    Class holds functions related to time
    A tick is the unit of time in which any action or updation can occur
    """
    globalTime = 0
    timers = []
    dt = 1 #Actual time in milliseconds per tick

    def __init__(self, label = None, startValue = 0, millisPerTick = 1):
        self.time = startValue
        self.label = label
        Time.timers.append(self)
        self.dt = millisPerTick

    def __str__(self):
        return self.ToClockString()

    def SetGlobalClock(startValue = 0):
        Time.globalTime = startValue

    def Tick(self=None):
        if self == None:
            Time.globalTime += 1
        else:
            self.time += 1

    def Reset(self=None):
        if self == None:
            value = Time.globalTime
            Time.globalTime = 0
            return value
        value = self.time
        self.time = 0
        return value

    def TickAll():
        Time.Tick()
        for timer in Time.timers:
            timer.Tick()

    def ToClockString(self = None):
        if self == None:
            time = Time.globalTime*Time.dt
        else:
            time = self.time*Time.dt
        
        milli = str(time%100)
        time = time//100
        seconds = f"{time%60:02d}"
        minutes = f"{(time//60)%60:02d}"
        hours = f"{(time//3600)%24:02d}"
        days = f"{(time//(3600*24))}"

        return (days + ":" + hours + ":" + minutes + ":" + seconds + ":" + milli)