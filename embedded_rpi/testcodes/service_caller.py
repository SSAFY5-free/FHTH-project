#!/usr/bin/python
"""Invoke remote methods."""
import dbus

FOOD_SERVICE_PATH = '/fhth/food/Test'
FOOD_SERVICE_IFACE = 'food.fhth.TestInterface'
FOOD_SERVICE_DOMAIN = 'food.fhth'

"""Proxy object from the Test object in receiver."""
sbus = dbus.SessionBus()
proxy = sbus.get_object(SERVICE_DOMAIN, SERVICE_PATH)
iface = dbus.Interface(proxy, dbus_interface=SERVICE_IFACE)
# props = iface.foo()

print(sbus)
print(proxy)
print(iface)
# print(props)

"""Call a method that simply retruns a string."""
# print(proxy.foo(dbus_interface=SERVICE_IFACE))
# print(proxy.action_activate(dbus_interface=SERVICE_IFACE))

iface.activate_action()
iface.set_amount("300")

# """Invoke a method that throws an exception and catch it."""
# try:
#     obj.fail(dbus_interface='tld.domain.sub.TestInterface')
# except Exception as e:
#     print(str(e))
#
# """
# Call the stop method of the proxxied object which will stop the receivers
# main loop.
# """
# print(obj.stop(dbus_interface='tld.domain.sub.TestInterface'))
