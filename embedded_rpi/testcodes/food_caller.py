#!/usr/bin/python
import dbus

SERVICE_PATH = '/fhth/food/Test'
SERVICE_IFACE = 'food.fhth.TestInterface'
SERVICE_DOMAIN = 'food.fhth'

sbus = dbus.SessionBus()
proxy = sbus.get_object(SERVICE_DOMAIN, SERVICE_PATH)
iface = dbus.Interface(proxy, dbus_interface=SERVICE_IFACE)
# props = iface.activate_action()

print(sbus)
print(proxy)
print(iface)
# print(props)

iface.activate_action()
iface.set_amount("300")
