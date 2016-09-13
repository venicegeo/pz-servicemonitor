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

class ServiceInterface:
    def __init__(self,**entries):
        self.__dict__.update(entries)
#
#
#
class ResourceMetaDataInterface:
    def __init__(self,**entries):
        self.__dict__.update(entries)
#
#
#
class StatsInterface:
    def __init__(self,**entries):
        self.__dict__.update(entries)
#
#
#
class ServiceStatsInterface:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        self.service_stats = ServiceStats(self._id,self.url,self.calls)
class ServiceStats:
    def __init__(self,_id,url,calls=[]):
        self._id=_id
        self.url=url
        self.calls=calls
    def add_call(self,call):
        if len(self.calls) is 10:
            self.calls.remove(self.calls[0])
        self.calls.append(call.toDict())
#
#        
#        
class CallInterface:
    def __init__(self,**entries):
        self.__dict__.update(entries)
class Call:
    class CallDict:
        def __init__(self,call):
            self.time=call.time
            if call.data is None:
                self.data=None
            else:
                self.data=call.data.status_code
    def __init__(self,time,data):
        self.time=time
        self.data=data
    def toDict(self):
        return self.CallDict(self).__dict__