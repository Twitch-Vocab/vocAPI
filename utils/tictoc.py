

import datetime

class TicToc:

    def __init__(self):
        
        self.start = datetime.datetime.now()


    def end(self):

        elapsed = datetime.datetime.now() - self.start

        return elapsed.total_seconds() * 1000

