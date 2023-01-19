import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
	def __init__(self):
		super().__init__(title="Asterisk Call Logger")

		self.grid = Gtk.Grid()
		self.caller_label = Gtk.Label(label="Caller ID")
		self.grid.attach(self.caller_label, 0, 0, 1, 1)
		self.caller_entry = Gtk.Entry()
		self.grid.attach(self.caller_entry, 1, 0, 1, 1)

		self.add(self.grid)
