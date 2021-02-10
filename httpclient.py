#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.socket.settimeout(2)
        return None

    def get_code(self, data):
        code = data[0].split(' ')[1]
        print("code333")
        print(code)
        return int(code)


    def get_headers(self,data):
        return data.split("\r\n")

    def get_body(self, data):
        return data.split('\r\n')[-1]

    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        return self.recvall(self.socket)
        
        
    def close(self):
        self.socket.close()

    def getHost(self,  url):
        data = urllib.parse.urlparse(url)
        return data.hostname

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        try:
            while not done:
                part = sock.recv(1024)
                if (part):
                    buffer.extend(part)
                else:
                    done = not part
        except socket.timeout:
            print("TimeOut")
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        urlLine = urllib.parse.urlparse(url)
        if urlLine.port:
            urlPort = urlLine.port
        else:
            # if the urlLine.port is none we make it 80 as default
            urlPort = 80
        #now we get the port we can connect the host by the port 
        self.connect(self.getHost(url),urlPort)

        if urlLine.path:
            urlPath = urlLine.path
        else:
            # if it is none then we use '/' as default 
            urlPath = '/'

        send_message = """GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n""".format(path=urlPath,  host=self.getHost(url))
       
        print("header6")
        print(send_message)
        urlData = self.sendall(send_message)

        urlHeader = self.get_headers(urlData)
        code = self.get_code(urlHeader)
        self.close()
        return HTTPResponse(code,urlData)

        

        
    def POST(self, url, args=None):
        urlBody = " "
        #parse the url into 6 component 
        # kind of decode the url in specific form
        urlLine = urllib.parse.urlparse(url)
        # if urlLine.port is not none we using the port
        if urlLine.port:
            urlPort = urlLine.port
        else:
            # if the urlLine.port is none we make it 80 as default
            urlPort = 80
        #now we get the port we can connect the host by the port 
        self.connect(socket.gethostbyname(urlLine.hostname),urlPort)

        if args != None:
            urlBody = urllib.parse.urlencode(args)
        else:
            urlBody = ""

        # try to get the path for url, if the one from urlparse is not none we use it
        if urlLine.path:
            urlPath = urlLine.path
        else:
            # if it is none then we use '/' as default 
            urlPath = '/'
        # the message we are giubg 
        print("tester2")
        urlLen = len(urlBody)

        send_message = """POST {path} HTTP/1.1\r\nHost: {host}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {length}\r\n\r\n{data}""".format(path=urlPath,  data=urlBody,  length=urlLen,  host=self.getHost(url))
        self.connect(self.getHost(url), urlPort)
        print("header99")
        print(send_message)
        urlData = self.sendall(send_message)
        urlHeaders = self.get_headers(urlData)
        body = urlHeaders[-1]
        print("data999")
        print(urlData)
        code = self.get_code(urlHeaders)
        self.close()
        return HTTPResponse(code,body)

        


    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
