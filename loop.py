# -*- coding: utf-8 -*-

import threading
from time import sleep

class LoopingThread:
    def __init__(self, interval=1, live=False):
        self.interval=interval
        self.live=live        
        self.thread = threading.Thread(target=self.run,args=())
        self.thread.daemon=True
        if live:
            self.start()
    def start(self):
        self.live=True
        self.thread.start()
    def run(self):
        count = 0
        while self.live:
            print("Loop: " + str(count))
            count+=1
            sleep(self.interval)
        else:
            print("Ending loop, closing resources...")
    def stop(self):
        self.live=False