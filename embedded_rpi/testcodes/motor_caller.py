#!/usr/bin/python
import dbus

SERVICE_PATH = '/fhth/motor/Test'
SERVICE_IFACE = 'motor.fhth.TestInterface'
SERVICE_DOMAIN = 'motor.fhth'

sbus = dbus.SessionBus()
proxy = sbus.get_object(SERVICE_DOMAIN, SERVICE_PATH)
iface = dbus.Interface(proxy, dbus_interface=SERVICE_IFACE)

print(sbus)
print(proxy)
print(iface)

try:
    while 1:
        print("motor loop start")
        cmd = input("input: ")
        iface.activate_motor(cmd)
except KeyboardInterrupt:
    print("keyboard")
