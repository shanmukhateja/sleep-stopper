from dbus import SleepStopperDBusClient

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class SleepStopperApplication(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, title="Sleep Stopper")
        self.set_size_request(300, 150)

        self.vbox = Gtk.Box()
        self.set_child(self.vbox)

        self.dbus = SleepStopperDBusClient()

        self.block_button = Gtk.Button.new_with_label("Block sleep")
        self.unblock_button = Gtk.Button.new_with_label("Unblock Sleep")

        self.block_button.set_hexpand(True)
        self.unblock_button.set_hexpand(True)

        self.vbox.append(self.block_button)
        self.vbox.append(self.unblock_button)

        self.block_button.connect("clicked", self.on_block_clicked)
        self.unblock_button.connect("clicked", self.on_unblock_clicked)

        self.update_ui_state()

    def on_block_clicked(self, _btn):
        result = self.dbus.inhibit()
        if result:
            # show toast 
            pass
        else:
            # show error toast
            pass
        self.update_ui_state()

    def on_unblock_clicked(self, _btn):
        result = self.dbus.uninhibit()
        if result:
            # show toast 
            pass
        else:
            # show error toast
            pass
        self.update_ui_state()

    def update_ui_state(self):
        is_active = self.dbus.is_active()

        if is_active:
            # Inhibit not on?
            self.block_button.set_visible(True)
            self.unblock_button.set_visible(False)
        else:
            # Inhibit IS SET!!
            self.block_button.set_visible(False)
            self.unblock_button.set_visible(True)

def on_activate(app):
    win = SleepStopperApplication(application=app)
    win.present()

app = Gtk.Application(application_id="in.suryatejak.sleepstopper")
app.connect("activate", on_activate)
app.run(None)
