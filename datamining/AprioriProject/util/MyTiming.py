import datetime

class MyTiming:

    def __init__(self):
        self.start = None
        self.end = None

    def start_counting(self):
        self.start = datetime.datetime.now()

    def stop_counting(self):
        self.end = datetime.datetime.now()

    def countElapsed(self):
        if(self.start != None and self.end != None):
            scnds = (self.end - self.start).total_seconds()



            return '{} s'.format(str(datetime.timedelta(seconds=scnds)))

    def resetTimer(self):
        self.start = None
        self.end = None