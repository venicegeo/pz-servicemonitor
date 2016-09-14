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

from pymongo import MongoClient
import requests
import time
import mc
import json
import os
import common

ONLINE='ONLINE'
DEGRADED='DEGRADED'
FAILED='FAILED'
OFFLINE='OFFLINE'

env = os.environ['p-mongodb']

def mongo_health_check(url):
    try:
        requests.get("http://%s"%url)
    except:
        print("Health check to: %s failed."%url)
        return False
        #sys.exit()
    return True
def split_url(url):
    parts = url.split("/")
    return parts[0]+"//"+parts[2]
def format_update(update):
    return json.loads(("{'$set':{'resourceMetadata.availability': '"+update+"'}}").replace("'","\""))
class Mongo:
    def __init__(self):
        self.envFound = mongo_health_check(env)
        if self.envFound:
            print("Found mongo")
            self.mongoClient = MongoClient(env)
            self.piazzaDB = self.mongoClient['Piazza']
            self.servicesCO = self.piazzaDB['Services']
            self.statsCO = self.piazzaDB['ServiceMonitor']
            self.update_stats_coll()
    def env_found(self):
        return self.envFound
    def update_stats_coll(self):
        services = self.get_services()
        for service in services:
            exists = self.statsCO.find_one({"_id":service._id})
            if exists is None:
                self.statsCO.insert_one(mc.ServiceStats(service._id,service.url,[]).__dict__)
    def get_services(self):
        cursor=self.servicesCO.find()
        services = []
        for doc in cursor:
            service = mc.ServiceInterface(**doc)
            meta = mc.ResourceMetaDataInterface(**service.resourceMetadata)
            av = None
            try:
                av = meta.availability
            except:
                pass
            if av!=OFFLINE:
               services.append(service)
        return services
    def get_stats(self):
        cursor=self.statsCO.find()
        stats = []
        for doc in cursor:
            stats.append(mc.StatsInterface(**doc))
        return stats
    def test_service(self, url):
        url=split_url(url)
        print("Testing: "+url,end=" ")
        r = None;        
        try:
            r = requests.get(url,timeout=300)
        except:
            pass
        return r
    def update_service_stats(self,_id,result):
        exists = self.statsCO.find_one({"_id":_id})
        if exists is None:
            return
        stats = mc.ServiceStatsInterface(**exists)
        stats.service_stats.add_call(mc.Call(time.time(),result))
        self.statsCO.replace_one({"_id":_id},stats.service_stats.__dict__)
    def perform_calc(self,_id):
        exists = self.statsCO.find_one({"_id":_id})
        if exists is None:
            return FAILED
        statsInt = mc.ServiceStatsInterface(**exists)
        stats = statsInt.service_stats
        maxi = len(stats.calls)-1
        print(mc.CallInterface(**stats.calls[maxi]).data,end=" ")
        if mc.CallInterface(**stats.calls[maxi]).data is not 200:
            if maxi>2:           
                if mc.CallInterface(**stats.calls[maxi-1]).data is not 200 and mc.CallInterface(**stats.calls[maxi-2]).data is not 200:
                    return FAILED
                else:
                    return DEGRADED
            else:
                return DEGRADED
        else:
            if maxi>2:
                if mc.CallInterface(**stats.calls[maxi-1]).data is 200 and mc.CallInterface(**stats.calls[maxi-2]).data is 200:
                    return ONLINE
                else:
                    return DEGRADED      
            else:
                return ONLINE
    def execute(self):
        common.mongoFound = mongo_health_check(env)
        if not common.mongoFound:
            return
        self.update_stats_coll()
        now = time.time()
        print("Starting run at %f"%now)
        services = self.get_services()
        print("Found %d services"%len(services))
        for service in services:
            result = self.test_service(service.url)            
            #print(result)
            self.update_service_stats(service._id,result)
            update = self.perform_calc(service._id)
            print(update)
            #self.servicesCO.update_one({"_id":service._id},format_update(update))    
        print("Finished run")

