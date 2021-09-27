#!/usr/bin/python
import dbus
import dbus.service
import dbus.glib
import rpi_motor

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GObject

SERVICE_PATH = '/fhth/motor/Test'
SERVICE_IFACE = 'motor.fhth.TestInterface'
SERVICE_DOMAIN = 'motor.fhth'

motor = None

class MotorService(dbus.service.Object):
    def __init__(self, bus_name, object_path):
        """Initialize the DBUS service object."""
        dbus.service.Object.__init__(self, bus_name, object_path)

    @dbus.service.method(SERVICE_IFACE, in_signature='s')
    def activate_motor(self, cmd):
        print("motor command input")
        print(cmd)
        self.MotorCommand(SERVICE_IFACE, {'cmd': cmd}, [])
        return 'motor'

    @dbus.service.signal(SERVICE_IFACE,signature='sa{sv}as')
    def MotorCommand(self, interface, changed, invalidated):
        print(changed)
        print(changed['cmd'])


def catchall_handler(*args, **kwargs):
    """Catch all handler.

    Catch and print information about all singals.
    """
    print('---- Caught signal ----')
    print('%s:%s\n' % (kwargs['dbus_interface'], kwargs['member']))

    print('Arguments:')
    for arg in args:
        print('* %s' % str(arg))

    print("\n")

def cmd_handler(iface, changed_props, invalidated_props):
    print("cmd handler")
    print(changed_props['cmd'])
    if changed_props['cmd'] == 'go':
        motor.go()
    elif changed_props['cmd'] == 'stop':
        motor.stop()
    elif changed_props['cmd'] == 'left':
        motor.left()
    elif changed_props['cmd'] == 'right':
        motor.right()

motor = rpi_motor.MotorControl(2)

loop = GObject.MainLoop()
bus = dbus.SessionBus()
bus_name = dbus.service.BusName(SERVICE_DOMAIN, bus=bus)

obj = MotorService(bus_name, SERVICE_PATH)

bus.add_signal_receiver(catchall_handler,
                        interface_keyword='dbus_interface',
                        member_keyword='member')

bus.add_signal_receiver(cmd_handler,
                        dbus_interface=SERVICE_IFACE,
                        signal_name='MotorCommand')

loop.run()
