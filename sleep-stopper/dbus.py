import asyncio
from dbus_fast.aio import MessageBus

class SleepStopperDBusClient(object):

    def __init__(self):
        self.cookie = None
        self.runner = asyncio.get_event_loop()
        self.runner.run_until_complete(self.init())

    async def init(self):
        self.bus = await MessageBus().connect()

        introspection = await self.bus.introspect('org.freedesktop.ScreenSaver', '/org/freedesktop/ScreenSaver')

        self.obj = self.bus.get_proxy_object('org.freedesktop.ScreenSaver', '/org/freedesktop/ScreenSaver', introspection)

        self.screensaver = self.obj.get_interface('org.freedesktop.ScreenSaver')

    def is_active(self):
       return self.cookie is None
    
    def inhibit(self):
        self.runner.run_until_complete(self._set_inhibit())
        return True

    def uninhibit(self):
        if not self.cookie:
            return False
        self.runner.run_until_complete(self._set_uninhibit())

    async def _set_inhibit(self):
        self.cookie = await self.screensaver.call_inhibit("Sleep Stopper", "User requested inhibit!")
        print(self.cookie)

    async def _set_uninhibit(self):
        if not self.cookie:
            print("self.cookie not set, ignoring request..")
            return False
        await self.screensaver.call_un_inhibit(self.cookie)
        self.cookie = None
        return True

#asyncio.run(SleepStopperDBusClient())

