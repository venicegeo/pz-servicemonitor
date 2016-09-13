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
import json
import signal
import sys
import time
import mongo
import loop
import common

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

class AdminStats:
    def __init__(self, createdAt=time.time(),online=0,degraded=0,failed=0,unknown=0):        
        self.createdAt = createdAt
        self.online=online
        self.degraded=degraded
        self.failed=failed
        self.unknown=unknown
    def update(self,mong):
        if not common.mongoFound:
            return
        self.online,self.degraded,self.failed,self.unknown = 0,0,0,0
        services = mong.get_services()
        for service in services:
            meta = mongo.ResourceMetaDataInterface(**service.resourceMetadata)
            av = None
            try:
                av = meta.availability
            except:
                pass
            if av == None:
                self.unknown+=1
            elif av == mongo.ONLINE:
                self.online+=1
            elif av == mongo.DEGRADED:
                self.degraded+=1
            elif av == mongo.FAILED:
                self.failed+=1
            else:
                self.unknown+=1
    def getJSON(self):
        if not common.mongoFound:
            return HttpMessage(200,"MongoDB could not be found.").getJSON()
        return json.dumps(self.__dict__, indent=2)


app = Flask(__name__)
mong = mongo.Mongo()
mongExists=mong.env_found()
loopThread = loop.LoopingThread(interval=20,mong=mong)

adminStats = AdminStats()

@app.route("/",methods=['GET'])
def helloWorld():
    return HttpMessage().getJSON()
    
@app.route("/admin/stats", methods=['GET'])
def adminStat():
    adminStats.update(mong)
    return adminStats.getJSON()

@app.route("/hello")
def hello():
    return "<html>Hello world</html>"
    
@app.route('/test', methods=['GET','POST'])
def test():
    if request.method == 'GET':
        return HttpMessage(200,"GET").getJSON()
    elif request.method == 'POST':
        if not request.is_json:
            return HttpMessage(400,"Payload is not of type json").getJSON()
        jsn = request.get_json()
        if jsn is None:
            return HttpMessage(400,"Bad payload").getJSON()
        return HttpMessage(200,jsn).getJSON()
    else:
        return HttpMessage(400,"Bad request").getJSON()

def signal_handler(signal, frame):
        print('Shutting down...')
        loopThread.stop()
        sys.exit(0)

if __name__ =="__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')
    loopThread.start()
    app.run()

