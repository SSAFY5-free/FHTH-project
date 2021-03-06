#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-2.1-or-later

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
try:
  from gi.repository import GLib
except ImportError:
  import gobject as GObject
import sys
import threading
import requests
from datetime import datetime
import rpi_motor

bus = None
mainloop = None
motor = None

BLUEZ_SERVICE_NAME = 'org.bluez'
DBUS_OM_IFACE =      'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE =    'org.freedesktop.DBus.Properties'

GATT_SERVICE_IFACE = 'org.bluez.GattService1'
GATT_CHRC_IFACE =    'org.bluez.GattCharacteristic1'
DEVICE_IFACE = 'org.bluez.Device1'

FOOD_SVC_UUID = '00002220-0000-1000-8000-00805f9b34fb'
FOOD_CHR_LEFT_UUID = '00002221-0000-1000-8000-00805f9b34fb'
FOOD_CHR_EATEN_UUID = '00002222-0000-1000-8000-00805f9b34fb'
FOOD_CHR_AMOUNT_UUID = '00002223-0000-1000-8000-00805f9b34fb'
FOOD_CHR_ACTION_UUID = '00002224-0000-1000-8000-00805f9b34fb'

DRINK_SVC_UUID = '00002230-0000-1000-8000-00805f9b34fb'
DRINK_CHR_DRINK_UUID = '00002231-0000-1000-8000-00805f9b34fb'
DRINK_CHR_WATER_UUID = '00002232-0000-1000-8000-00805f9b34fb'

food_device = None
food_service = None
food_left_chrc = None
food_eaten_chrc = None
food_amount_chrc = None
food_action_chrc = None

drink_device = None
drink_service = None
drink_drink_chrc = None
drink_water_chrc = None

EATEN_CHANGED_TRG = False
FOOD_EATEN = True
FOOD_LEFT = 0
WATER_LACK = False

# index: SVC number
uuid_list = [FOOD_SVC_UUID, DRINK_SVC_UUID]
service_list = [food_service, drink_service]
device_list = [food_device, drink_device]
dev_name_list = ["FHTH_FOOD","FHTH_DRINK"]

def get_timestamp():
    timestamp = datetime.now()
    time = [timestamp.year,
            timestamp.month,
            timestamp.day,
            timestamp.hour,
            timestamp.minute,
            timestamp.second]
    for i,v in enumerate(time):
        if v < 10:
            time[i] = '{0:02d}'.format(v)

    return f"{time[0]}{time[1]}{time[2]} {time[3]}:{time[4]}:{time[5]}"

# ===================================================
FOOD_SERVICE_PATH = '/fhth/food/Test'
FOOD_SERVICE_IFACE = 'food.fhth.TestInterface'
FOOD_SERVICE_DOMAIN = 'food.fhth'

MOTOR_SERVICE_PATH = '/fhth/motor/Test'
MOTOR_SERVICE_IFACE = 'motor.fhth.TestInterface'
MOTOR_SERVICE_DOMAIN = 'motor.fhth'

def dbus_test(amount):
    print(type(amount), "amount: ", amount)

def amount_changed_cb(iface, changed_props, invalidated_props):
    print(changed_props)
    dbus_test(changed_props['amount'])
    write_food_amount(changed_props['amount'])

def action_activated_cb():
    print("action callback")
    if food_action_chrc is not None:
        write_food_action()

def cmd_handler(iface, changed_props, invalidated_props):
    print("cmd handler")
    print(changed_props['cmd'])
    try:
        if changed_props['cmd'] == 'go':
            motor.go()
        elif changed_props['cmd'] == 'stop':
            motor.stop()
        elif changed_props['cmd'] == 'back':
            motor.back()
        elif changed_props['cmd'] == 'left':
            motor.left()
        elif changed_props['cmd'] == 'right':
            motor.right()
        elif changed_props['cmd'] == 'middle':
            motor.middle()
    except Exception as e:
        print(e)


class WebCommService(dbus.service.Object):
    def __init__(self, bus_name, object_path):
        dbus.service.Object.__init__(self, bus_name, object_path)

    @dbus.service.method(FOOD_SERVICE_IFACE)
    def activate_action(self):
        print("action method activated")
        self.ActionActivated()
        return 'action'

    @dbus.service.method(FOOD_SERVICE_IFACE, in_signature='s')
    def set_amount(self, amount):
        print("amount method activated")
        print(amount)
        self.AmountChanged(FOOD_SERVICE_IFACE, {'amount': amount}, [])
        return 'amount'

    @dbus.service.signal(FOOD_SERVICE_IFACE,signature='sa{sv}as')
    def AmountChanged(self, interface, changed, invalidated):
        print(changed)
        print(changed['amount'])

    @dbus.service.signal(FOOD_SERVICE_IFACE)
    def ActionActivated(self):
        print("action signal")

class MotorService(dbus.service.Object):
    def __init__(self, bus_name, object_path):
        """Initialize the DBUS service object."""
        dbus.service.Object.__init__(self, bus_name, object_path)

    @dbus.service.method(MOTOR_SERVICE_IFACE, in_signature='s')
    def activate_motor(self, cmd):
        print("motor command input")
        print(cmd)
        self.MotorCommand(MOTOR_SERVICE_IFACE, {'cmd': cmd}, [])
        return 'motor'

    @dbus.service.signal(MOTOR_SERVICE_IFACE,signature='sa{sv}as')
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


# ===================================================

def post_data(data, api):
    PORT = 3000
    url = 'http://localhost:{PORT}/{API}'.format(PORT=PORT, API=api)
    try:
        res = requests.post(url, json=data, headers={})
        print("Server status: ", res.status_code)
    except Exception as e:
        print("Server errors: ", e)

def xor(condition1, condition2):
    if condition1:
        return (not condition2)
    else:
        return condition2

# callbacks
def generic_error_cb(error):
    print('D-Bus call failed: ' + str(error))
    mainloop.quit()

# ?????? ????????? ??? remove callback
def interfaces_removed_cb(object_path, interfaces):
    print("interfaces removed callback")
    print(object_path)
    print(interfaces)

# registration callbacks
def food_left_start_notify_cb():
    print('FOOD-LEFT notifications enabled')

def food_eaten_start_notify_cb():
    print('FOOD-EATEN notifications enabled')

def food_amount_start_notify_cb():
    print('FOOD-AMOUNT notifications enabled')

def food_action_start_notify_cb():
    print('FOOD-ACTION notifications enabled')

def drink_drink_start_notify_cb():
    print('DRINK-DRINK notifications enabled')

def drink_water_start_notify_cb():
    print('DRINK-WATER notifications enabled')

# write callback (????????? write ????????? ?????????)
def write_cb():
    print("Write complete")

## write ????????? AWS->RPi Backend ?????? ?????? ????????? write?????? ?????? ??????
# ?????? True('1') ?????? ?????? ???????????? ???????????? ???
def write_food_action():
    global FOOD_EATEN
    # ???????????? ??????: ????????? ?????? ????????? ?????? write ?????? ??? ?????????
    # print("write")
    # str_value = bytes('1'.encode())
    # food_action_chrc[0].WriteValue(str_value, {}, reply_handler=write_cb,
    #                                  error_handler=generic_error_cb,
    #                                  dbus_interface=GATT_CHRC_IFACE)

    # FOOD??? ????????? ???????????? ?????? ??????
    if FOOD_EATEN:
        print("write")
        str_value = bytes('1'.encode())
        food_action_chrc[0].WriteValue(str_value, {}, reply_handler=write_cb,
                                         error_handler=generic_error_cb,
                                         dbus_interface=GATT_CHRC_IFACE)
        FOOD_EATEN = False

def write_food_amount(amount):

    print("write")
    # write??? string?????? ??????
    # str_value = bytes(str(amount).encode())
    str_value = bytes(amount.encode())
    food_amount_chrc[0].WriteValue(str_value, {}, reply_handler=write_cb,
                                     error_handler=generic_error_cb,
                                     dbus_interface=GATT_CHRC_IFACE)


# notify callbacks
# ?????? ???????????? ?????? notify ?????? ?????? ??? ?????? ????????? ??????
# ????????? action ??? ??? ??? ?????? ????????? True ??? ?????? action ??????
def food_eaten_changed_cb(iface, changed_props, invalidated_props):
    global FOOD_EATEN, EATEN_CHANGED_TRG
    print("eaten notify callback")
    if iface != GATT_CHRC_IFACE:
        return

    if not len(changed_props):
        return

    value = changed_props.get('Value', None)
    if not value:
        return

    print("decoded value: %s" % [bytes([v]).decode() for v in value])
    strr = [bytes([v]).decode() for v in value]
    CUR_STATE = None

    if strr[0] == '0':
        CUR_STATE = False
    elif strr[0] == '1':
        CUR_STATE = True

    # if CUR_STATE != None:
    #     if xor(FOOD_EATEN, CUR_STATE):
    #         if not FOOD_EATEN:
    #             FOOD_EATEN = CUR_STATE
    #         timestamp = get_timestamp()
    #         data = {'EATEN': FOOD_EATEN, 'DATE': timestamp}
    #         post_data(data,'pet/foodeat')
    # print("FOOD:",FOOD_EATEN)

    if CUR_STATE != None:
        if xor(EATEN_CHANGED_TRG, CUR_STATE):
            timestamp = get_timestamp()
            data = {'EATEN': CUR_STATE, 'DATE': timestamp}
            post_data(data,'pet/foodeat')
            if EATEN_CHANGED_TRG:
                EATEN_CHANGED_TRG = False
            else:
                EATEN_CHANGED_TRG = True
                if not FOOD_EATEN:
                    FOOD_EATEN = CUR_STATE

    print("FOOD:",FOOD_EATEN)

# ?????? ?????? ??? notify ??? ????????? ?????? POST
# int??? ????????? uint8 4???????????? ?????? ?????? ??? ??? ???????????? POST?????? ??? ???
def food_left_changed_cb(iface, changed_props, invalidated_props):
    print("left notify callback")
    if iface != GATT_CHRC_IFACE:
        return

    if not len(changed_props):
        return

    value = changed_props.get('Value', None)
    if not value:
        return

    print("decoded value: %s" % [bytes([v]).decode() for v in value])
    strr = [bytes([v]).decode() for v in value]

    left = "".join(strr)
    print(left)
    timestamp = get_timestamp()
    data = {"LEFT": left, 'DATE': timestamp}
    post_data(data, 'pet/foodleft')

# notify test
def food_amount_changed_cb(iface, changed_props, invalidated_props):
    print("amount notify callback")
    if iface != GATT_CHRC_IFACE:
        return

    if not len(changed_props):
        return

    value = changed_props.get('Value', None)
    if not value:
        return

    print("decoded value: %s" % [bytes([v]).decode() for v in value])
    strr = [bytes([v]).decode() for v in value]

# notify test
def food_action_changed_cb(iface, changed_props, invalidated_props):
    print("action notify callback")
    if iface != GATT_CHRC_IFACE:
        return

    if not len(changed_props):
        return

    value = changed_props.get('Value', None)
    if not value:
        return

    print("decoded value: %s" % [bytes([v]).decode() for v in value])
    strr = [bytes([v]).decode() for v in value]


# ???????????? notify ??? ????????? POST
def drink_drink_changed_cb(iface, changed_props, invalidated_props):
    print("drink notify callback")
    if iface != GATT_CHRC_IFACE:
        return

    if not len(changed_props):
        return

    value = changed_props.get('Value', None)
    if not value:
        return

    print("decoded value: %s" % [bytes([v]).decode() for v in value])
    strr = [bytes([v]).decode() for v in value]
    # ????????? ?????? post
    if strr[0] == '0':
        timestamp = get_timestamp()
        data = {'DRINK': True, 'DATE': timestamp}
        post_data(data)

# ??? ?????? ????????? ?????? ?????? ??????
# ??? ??? ????????? ?????? ?????? ?????? ????????? ???????????? ?????? ??? ????????? ??????
def drink_water_changed_cb(iface, changed_props, invalidated_props):
    global WATER_LACK
    print("water notify callback")
    if iface != GATT_CHRC_IFACE:
        return

    if not len(changed_props):
        return

    value = changed_props.get('Value', None)
    if not value:
        return

    print("decoded value: %s" % [bytes([v]).decode() for v in value])
    strr = [bytes([v]).decode() for v in value]
    timestamp = get_timestamp()

    if strr[0] == '0':
        WATER_LACK = True
        data = {'WATER_LACK': True, 'DATE': timestamp}
        post_data(data)
    else:
        if WATER_LACK:
            WATER_LACK = False
            data = {'WATER_LACK': False, 'DATE': timestamp}
            post_data(data)

# ??? ????????? ?????? ??????. ??? ?????? ?????? ?????? ??? ????????? ??????????????? ????????????
def temp_cb(value):
    print("chrc reading callback")
    print("decode: %s" % [bytes([v]).decode() for v in value])


def start_client():
    print("start client")
    if food_left_chrc is not None:

        # test reading
        food_left_chrc[0].ReadValue({}, reply_handler=temp_cb,
                                        error_handler=generic_error_cb,
                                        dbus_interface=GATT_CHRC_IFACE)

        food_eaten_chrc[0].ReadValue({}, reply_handler=temp_cb,
                                        error_handler=generic_error_cb,
                                        dbus_interface=GATT_CHRC_IFACE)
        food_amount_chrc[0].ReadValue({}, reply_handler=temp_cb,
                                        error_handler=generic_error_cb,
                                        dbus_interface=GATT_CHRC_IFACE)
        food_action_chrc[0].ReadValue({}, reply_handler=temp_cb,
                                        error_handler=generic_error_cb,
                                        dbus_interface=GATT_CHRC_IFACE)


        # Listen to PropertiesChanged signals
        food_left_prop_iface = dbus.Interface(food_left_chrc[0], DBUS_PROP_IFACE)
        food_left_prop_iface.connect_to_signal("PropertiesChanged",
                                              food_left_changed_cb)

        food_eaten_prop_iface = dbus.Interface(food_eaten_chrc[0], DBUS_PROP_IFACE)
        food_eaten_prop_iface.connect_to_signal("PropertiesChanged",
                                              food_eaten_changed_cb)

        food_amount_prop_iface = dbus.Interface(food_amount_chrc[0], DBUS_PROP_IFACE)
        food_amount_prop_iface.connect_to_signal("PropertiesChanged",
                                              food_amount_changed_cb)

        food_action_prop_iface = dbus.Interface(food_action_chrc[0], DBUS_PROP_IFACE)
        food_action_prop_iface.connect_to_signal("PropertiesChanged",
                                              food_action_changed_cb)

        # Subscribe to notifications.
        food_left_chrc[0].StartNotify(reply_handler=food_left_start_notify_cb,
                                     error_handler=generic_error_cb,
                                     dbus_interface=GATT_CHRC_IFACE)

        food_eaten_chrc[0].StartNotify(reply_handler=food_eaten_start_notify_cb,
                                     error_handler=generic_error_cb,
                                     dbus_interface=GATT_CHRC_IFACE)

        food_amount_chrc[0].StartNotify(reply_handler=food_amount_start_notify_cb,
                                     error_handler=generic_error_cb,
                                     dbus_interface=GATT_CHRC_IFACE)

        food_action_chrc[0].StartNotify(reply_handler=food_action_start_notify_cb,
                                     error_handler=generic_error_cb,
                                     dbus_interface=GATT_CHRC_IFACE)

    else:
        print("no food chrc")

    if drink_drink_chrc is not None:

        drink_drink_prop_iface = dbus.Interface(drink_drink_chrc[0], DBUS_PROP_IFACE)
        drink_drink_prop_iface.connect_to_signal("PropertiesChanged",
                                              drink_drink_changed_cb)

        drink_water_prop_iface = dbus.Interface(drink_water_chrc[0], DBUS_PROP_IFACE)
        drink_water_prop_iface.connect_to_signal("PropertiesChanged",
                                             drink_water_changed_cb)

        drink_drink_chrc[0].StartNotify(reply_handler=drink_drink_start_notify_cb,
                                     error_handler=generic_error_cb,
                                     dbus_interface=GATT_CHRC_IFACE)
        drink_water_chrc[0].StartNotify(reply_handler=drink_water_start_notify_cb,
                                    error_handler=generic_error_cb,
                                    dbus_interface=GATT_CHRC_IFACE)

    else:
        print("no drink chrc")

def temp_write_timer():
    print("write activate")
    if food_left_chrc is not None:
        write_food_action()
    else:
        print("why Noneeeeee")
    timer = threading.Timer(30, temp_write_timer)
    timer.start()


def process_chrc(chrc_path, svc_no):
    chrc = bus.get_object(BLUEZ_SERVICE_NAME, chrc_path)
    chrc_props = chrc.GetAll(GATT_CHRC_IFACE,
                             dbus_interface=DBUS_PROP_IFACE)

    uuid = chrc_props['UUID']
    print(uuid, svc_no)

    # ????????? ???????????? ?????? char ??????
    if svc_no == 0:
        if uuid == FOOD_CHR_LEFT_UUID:
            global food_left_chrc
            food_left_chrc = (chrc, chrc_props)
            print(food_left_chrc)
        elif uuid == FOOD_CHR_EATEN_UUID:
            global food_eaten_chrc
            food_eaten_chrc = (chrc, chrc_props)
            print(food_eaten_chrc)
        elif uuid == FOOD_CHR_AMOUNT_UUID:
            global food_amount_chrc
            food_amount_chrc = (chrc, chrc_props)
            print(food_amount_chrc)
        elif uuid == FOOD_CHR_ACTION_UUID:
            global food_action_chrc
            food_action_chrc = (chrc, chrc_props)
            print(food_action_chrc)
        else:
            print('Unrecognized characteristic: ' + uuid)
    elif svc_no == 1:
        if uuid == DRINK_CHR_DRINK_UUID:
            global drink_drink_chrc
            drink_drink_chrc = (chrc, chrc_props)
            print(drink_drink_chrc)
        elif uuid == DRINK_CHR_WATER_UUID:
            global drink_water_chrc
            drink_water_chrc = (chrc, chrc_props)
            print(drink_water_chrc)
        else:
            print('Unrecognized characteristic: ' + uuid)

    return True


def process_service(service_path, chrc_paths):
    service = bus.get_object(BLUEZ_SERVICE_NAME, service_path)
    service_props = service.GetAll(GATT_SERVICE_IFACE,
                                   dbus_interface=DBUS_PROP_IFACE)

    uuid = service_props['UUID']
    service_number = -1

    for idx, svc in enumerate(uuid_list):
        if uuid == svc:
            service_number = idx

    if service_number < 0:
        return False

    print(f'Service found: {service_number}'+ service_path)

    # Process the characteristics.
    for chrc_path in chrc_paths:
        process_chrc(chrc_path, service_number)

    service_list[service_number] = (service, service_props, service_path)
    print(service_number, service_list[service_number])
    return True


def main():
    # Set up the main loop.
    DBusGMainLoop(set_as_default=True)
    global bus, motor
    bus = dbus.SystemBus()
    motor = rpi_motor.MotorControl(2)

    # ==============================================================
    sebus = dbus.SessionBus()
    web_bus_name = dbus.service.BusName(FOOD_SERVICE_DOMAIN, bus=sebus)
    motor_bus_name = dbus.service.BusName(MOTOR_SERVICE_DOMAIN, bus=sebus)

    webComm = WebCommService(web_bus_name, FOOD_SERVICE_PATH)
    motorSvc = MotorService(motor_bus_name, MOTOR_SERVICE_PATH)

    sebus.add_signal_receiver(catchall_handler,
                            interface_keyword='dbus_interface',
                            member_keyword='member')
    sebus.add_signal_receiver(amount_changed_cb,
                            dbus_interface=FOOD_SERVICE_IFACE,
                            signal_name='AmountChanged')
    sebus.add_signal_receiver(action_activated_cb,
                            dbus_interface=FOOD_SERVICE_IFACE,
                            signal_name='ActionActivated')
    sebus.add_signal_receiver(cmd_handler,
                            dbus_interface=MOTOR_SERVICE_IFACE,
                            signal_name='MotorCommand')

# ==============================================================

    global mainloop
    mainloop = GLib.MainLoop()

    om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'), DBUS_OM_IFACE)
    om.connect_to_signal('InterfacesRemoved', interfaces_removed_cb)

    print('Getting objects...')
    objects = om.GetManagedObjects()
    chrcs = []

    # find device
    print("Finding Devices...")
    for path, interfaces in objects.items():
        dd = interfaces.get(DEVICE_IFACE)
        if dd is None:
            continue
        try:
            for idx, dev_name in enumerate(dev_name_list):
                print(dd["Address"], dd["Name"])
                if str(dd["Name"]) == dev_name:
                    device_list[idx] = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, path), DEVICE_IFACE)
                    print(device_list[idx])
                    device_list[idx].Connect()
                    print(f"device {idx} Connect!!")
        except Exception as e:
            print("error: ",e)
            continue


    # List characteristics found
    print("Finding Services...")
    for path, interfaces in objects.items():
        if GATT_CHRC_IFACE not in interfaces.keys():
            continue
        chrcs.append(path)

    # List sevices found
    for path, interfaces in objects.items():
        if GATT_SERVICE_IFACE not in interfaces.keys():
            continue

        chrc_paths = [d for d in chrcs if d.startswith(path + "/")]
        print(chrc_paths)

        if process_service(path, chrc_paths):
            continue

    for idx, svc in enumerate(service_list):
        if svc:
            print(f"service exist: {idx}")

    try:
        start_client()
        # temp_write_timer()
        # write_food_amount(300)
        # write_food_action()

        mainloop.run()
    except KeyboardInterrupt:
        print("keyboard")
    finally:
        for idx, dev in enumerate(device_list):
            if dev:
                print(f"device {idx} Disconnect!!")
                dev.Disconnect()

if __name__ == '__main__':
    main()
