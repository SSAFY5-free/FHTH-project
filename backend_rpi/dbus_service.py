#!/usr/bin/python
"""Receiver related functionality."""
import dbus
import dbus.service
import dbus.glib

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GObject

# SERVICE_PATH = '/tld/domain/sub/Test'
SERVICE_PATH = '/fhth/food/Test'
# SERVICE_IFACE = 'tld.domain.sub.TestInterface'
SERVICE_IFACE = 'food.fhth.TestInterface'
# SERVICE_DOMAIN = 'sub.domain.tld'
SERVICE_DOMAIN = 'food.fhth'

def amount_changed_cb(iface, changed_props, invalidated_props):
    print(changed_props)

def action_activated_cb():
    print("action callback")

class Test(dbus.service.Object):
    """Reciever test class."""

    loop = None

    def __init__(self, bus_name, object_path, loop):
        """Initialize the DBUS service object."""
        dbus.service.Object.__init__(self, bus_name, object_path)
        self.loop = loop

    # @dbus.service.method(SERVICE_IFACE)
    # def foo(self):
    #     """Return a string."""
    #     print("foo method activated")
    #     return 'Foo'

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

"""
First we get the bus to attach to. This may be either the session bus, of the
system bus. For system bus root permission is required.

We claim a bus name on the chosen bus. The name should be in form of a
domain name.
"""
bus = dbus.SessionBus()
# bus = dbus.SystemBus()
bus_name = dbus.service.BusName(SERVICE_DOMAIN, bus=bus)

"""
We initialize our service object with our name and object path. Object
path should be in form of a reverse domain dame, delimited by / instead of .
and the Class name as last part.

The object path we set here is of importance for our invoker, since it will to
call it exactly as defined here.
"""
obj = Test(bus_name, SERVICE_PATH, loop)


"""
Attach signal handler.

Signal handlers may be attached in different ways, either by interface keyword
or DBUS interface and a signal name or member keyword.

You can easily gather all information by running the DBUS monitor.
"""
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
