#!/usr/bin/python
import dbus
import dbus.service
import dbus.glib

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GObject

SERVICE_PATH = '/fhth/food/Test'
SERVICE_IFACE = 'food.fhth.TestInterface'
SERVICE_DOMAIN = 'food.fhth'

def amount_changed_cb(iface, changed_props, invalidated_props):
    print(changed_props)

def action_activated_cb():
    print("action callback")

class Test(dbus.service.Object):
    loop = None

    def __init__(self, bus_name, object_path, loop):
        """Initialize the DBUS service object."""
        dbus.service.Object.__init__(self, bus_name, object_path)
        self.loop = loop

    @dbus.service.method(SERVICE_IFACE)
    def activate_action(self):
        print("action method activated")
        self.ActionActivated()
        return 'action'

    @dbus.service.method(SERVICE_IFACE, in_signature='s')
    def set_amount(self, amount):
        print("amount method activated")
        print(amount)
        self.AmountChanged(SERVICE_IFACE, {'amount': amount}, [])
        return 'amount'

    @dbus.service.signal(SERVICE_IFACE,signature='sa{sv}as')
    def AmountChanged(self, interface, changed, invalidated):
        print(changed)
        print(changed['amount'])

    @dbus.service.signal(SERVICE_IFACE)
    def ActionActivated(self):
        print("action signal")


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


def quit_handler():
    """Signal handler for quitting the receiver."""
    print('Quitting....')
    loop.quit()

def test_handler(iface, changed_props, invalidated_props):
    print("test function")
    print(changed_props)

loop = GObject.MainLoop()
bus = dbus.SessionBus()
bus_name = dbus.service.BusName(SERVICE_DOMAIN, bus=bus)

obj = Test(bus_name, SERVICE_PATH, loop)


bus.add_signal_receiver(catchall_handler,
                        interface_keyword='dbus_interface',
                        member_keyword='member')
bus.add_signal_receiver(amount_changed_cb,
                        dbus_interface=SERVICE_IFACE,
                        signal_name='AmountChanged')
bus.add_signal_receiver(action_activated_cb,
                        dbus_interface=SERVICE_IFACE,
                        signal_name='ActionActivated')

loop.run()
