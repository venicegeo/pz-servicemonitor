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

from flask import Flask
from flask import request
from pymongo import MongoClient
from time import sleep
import json
import threading
import signal
import sys

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
class HttpMessage:
    statusCode = 0
    data = ""
    def __init__(self,statusCode=None,message=None):
        if statusCode is not None:
            self.statusCode=statusCode
        else:
            self.statusCode=200
        if message is not None:
            self.data = message
        else:
            self.data = "Hi! I'm a monitor lizard!"
    def setMessage(self,message):
        self.data = message
    def setStatusCode(self,statusCode):
        self.statusCode=statusCode
    def getJSON(self):
        return json.dumps(self.__dict__, indent=2)
    def getHTML(self):
        return '<pre style="word-wrap: break-word; white-space: pre-wrap;">'+self.getJSON()+'</pre>'

app = Flask(__name__)

@app.route("/")
def helloWorld():
    return HttpMessage().getJSON()

@app.route('/test', methods=['GET','POST'])
def test():
    if not request.is_json:
        return HttpMessage(400,"Payload is not of type json")
    jsn = request.get_json()
    if jsn is None:
        return HttpMessage(400,"Bad payload")
    return HttpMessage(200,jsn).getJSON()

#Create mongo client
mongoClient = MongoClient("jobdb.dev:27017")
#Create primer database
primerDB = mongoClient['primer']
#Create dataset collection
datasetCOLL = primerDB['dataset']
#Add a document
result = datasetCOLL.insert_one({"foo":"bar"})
print(result.inserted_id)

cursor = datasetCOLL.find({"_id":result.inserted_id})
for doc in cursor:
    print(doc)

loopThread = LoopingThread()

def signal_handler(signal, frame):
        print('Shutting down...')
        loopThread.stop()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')

loopThread.start()
app.run()

