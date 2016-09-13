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

class ResourceMetadata:
    def __init__(self,name,description,formatRM,qos,statusType,availability,tags,classType,expiresOn,clientCertRequired,credentialsRequired,preAuthRequired,networkAvailable,contacts,reason,version,createdBy,createdOn,createdByJobId,metadata,numericKeyValueList,textKeyValueList):
        self.name=name
        self.description=description
        self.formatRM=formatRM
        self.qos=qos
        self.statusType=statusType
        self.availability=availability
        self.tags=tags
        self.classType=classType
        self.expiresOn=expiresOn
        self.clientCertRequired=clientCertRequired
        self.credentialsRequired=credentialsRequired
        self.preAuthRequired=preAuthRequired
        self.networkAvailable=networkAvailable
        self.contacts=contacts
        self.reason=reason
        self.version=version
        self.createdBy=createdBy
        self.createdOn=createdOn
        self.createdByJobId=createdByJobId
        self.metadata=metadata
        self.numericKeyValueList=numericKeyValueList
        self.textKeyValueList=textKeyValueList
class Service:
    def __init__(self,serviceId,url,contractUrl,method,timeout,heartbeat,resourceMetadata):
        self.serviceId=serviceId
        self.url=url
        self.contractUrl=contractUrl
        self.method=method
        self.timeout=timeout
        self.heartbeat=heartbeat
        self.resourceMetadata=resourceMetadata
