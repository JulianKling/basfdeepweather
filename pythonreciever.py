#!/usr/bin/python3

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import geoplotlib
import _thread
from geoplotlib.colors import colorbrewer
from geoplotlib.utils import epoch_to_str, BoundingBox, read_csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

hostName = "10.0.45.5"
hostPort = 5000

def start_server():
	try:
		myServer.serve_forever()
	except KeyboardInterrupt:
		pass

class MyServer(BaseHTTPRequestHandler):

	#	GET is for clients geting the predi
	def do_GET(self):
		self.send_response(200)
		self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))

	#	POST is for submitting data.
	def do_POST(self):

		print( "incomming http: ", self.path )

		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		print(post_data.decode('utf8'))
		self.send_response(200)

		#client.close()

		#import pdb; pdb.set_trace()


myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

data = read_csv('./metro.csv')
# start the server in a background thread
_thread.start_new_thread(start_server,())

geoplotlib.dot(data, 'r')
geoplotlib.labels(data, 'name', color=[0,0,255,255], font_size=10, anchor_x='center')
geoplotlib.show()

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))