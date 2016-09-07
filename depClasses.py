# -*- coding: utf-8 -*-
# Copyright 2016, RadsiantBlue Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import threading
from time import sleep
import mongo

class LoopingThread:
    def __init__(self, interval=1, live=False, mong=None):
        self.interval=interval
        self.live=live        
        self.thread = threading.Thread(target=self.run,args=())
        self.thread.daemon=True
        if mong is None:
            self.mong=mongo.Mongo()
        else:
            self.mong=mong
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
            self.mong.execute()
            sleep(self.interval)
        else:
            print("Ending loop, closing resources...")
    def stop(self):
        self.live=False