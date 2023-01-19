"""Brief example of using the channel API with a state machine.
This app will answer any channel sent to Stasis(hello), and play "Hello,
world" to the channel. For any DTMF events received, the number is played back
to the channel. Press # to hang up, and * for a special message.
"""

#
# Copyright (c) 2013, Digium, Inc.
# Copyright (c) 2018, Matthias Urlichs
#

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import GUI

import asyncari
import asyncio, gbulb

from datetime import datetime

import os

ast_host = os.getenv("AST_HOST", 'localhost')
ast_port = int(os.getenv("AST_ARI_PORT", 8088))
ast_url = os.getenv("AST_URL", 'http://%s:%d/' % (ast_host, ast_port))
ast_username = os.getenv("AST_USER", 'asterisk')
ast_password = os.getenv("AST_PASS", 'asterisk')
ast_app = os.getenv("AST_APP", 'hello')


#def channel_state_change_cb(channel, ev):
#	"""Handler for changes in a channel's state"""

#	print("Channel %s is now: %s" % (channel.json.get('name'), channel.json.get('state')))


async def ari_thread():
	async with asyncari.connect(ast_url, ast_app, ast_username, ast_password) as client:
		# Run the WebSocket
#		client.on_channel_event('ChannelStateChange', channel_state_change_cb)
		print("------1-----")
		async for m in client:
			print("------2-----")
			print("** EVENT **", m)
			print(m._orig_msg)
			print("Caller: %s" % m['channel']['caller']['number'])
			print("Target: %s" % m['channel']['dialplan']['app_data'].split(',')[1])
			print("Creation Time: %s" % m['channel']['creationtime'])
			print(datetime.strptime(m['channel']['creationtime'][0:18], "%Y-%m-%dT%H:%M:%S"))
			print("timestamp: %s" % m['timestamp'])
			print("------3-----")
		print("------4-----")


def main():
	print("Entering main")
	asyncio.set_event_loop_policy(gbulb.GLibEventLoopPolicy())
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	GUI.MainWindow.Window.connect("destroy", Gtk.main_quit)
	GUI.MainWindow.Window.show_all()
	print("main: create_task")
	loop.run_until_complete(ari_thread())
	print("main:task created")
		#await task
	loop.run_forever()
	print("main:end")


if __name__ == "__main__":
	#logging.basicConfig(level=logging.DEBUG)
	try:
		main()
	except KeyboardInterrupt:
		pass
