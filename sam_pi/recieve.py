#!/usr/bin/env python
# -*- coding: utf8 -*-

#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Osnovnoy
#
# Created:     30/01/2018
# Copyright:   (c) Osnovnoy 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import requests
import json
import urllib2

class Recieve:

    def __init__(self,uid):
        content = uid
        response = requests.get('http://abdn-sam.herokuapp.com/')
        data = json.load(response.content)
