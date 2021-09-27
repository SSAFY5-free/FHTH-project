# #!/usr/bin/env python3
# # SPDX-License-Identifier: LGPL-2.1-or-later

# import dbus
# try:
#   from gi.repository import GLib
# except ImportError:
#   import gobject as GObject<template>
# import sys
# import threading
# import requests
# from datetime import datetime
# from dbus.mainloop.glib import DBusGMainLoop

# bus = None
# mainloop = None

# BLUEZ_SERVICE_NAME = 'org.bluez'
# DBUS_OM_IFACE =      'org.freedesktop.DBus.ObjectManager'
# DBUS_PROP_IFACE =    'org.freedesktop.DBus.Properties'

# GATT_SERVICE_IFACE = 'org.bluez.GattService1'
# GATT_CHRC_IFACE =    'org.bluez.GattCharacteristic1'
# DEVICE_IFACE = 'org.bluez.Device1'

# FOOD_SVC_UUID = '00002220-0000-1000-8000-00805f9b34fb'
# FOOD_CHR_LEFT_UUID = '00002221-0000-1000-8000-00805f9b34fb'
# FOOD_CHR_EATEN_UUID = '00002222-0000-1000-8000-00805f9b34fb'
# FOOD_CHR_AMOUNT_UUID = '00002223-0000-1000-8000-00805f9b34fb'
# FOOD_CHR_ACTION_UUID = '00002224-0000-1000-8000-00805f9b34fb'

# DRINK_SVC_UUID = '00002230-0000-1000-8000-00805f9b34fb'
# DRINK_CHR_DRINK_UUID = '00002231-0000-1000-8000-00805f9b34fb'
# DRINK_CHR_WATER_UUID = '00002232-0000-1000-8000-00805f9b34fb'

# food_device = None
# food_service = None
# food_left_chrc = None
# food_eaten_chrc = None
# food_amount_chrc = None
# food_action_chrc = None

# drink_device = None
# drink_service = None
# drink_drink_chrc = None
# drink_water_chrc = None

# FOOD_EATEN = True
# FOOD_LEFT = 0
# WATER_LACK = False

# PORT = 3000
# API = ''
# url = 'http://localhost:{PORT}/{API}'.format(PORT=PORT, API=API)

# # index: SVC number
# uuid_list = [FOOD_SVC_UUID, DRINK_SVC_UUID]
# service_list = [food_service, drink_service]
# device_list = [food_device, drink_device]
# dev_name_list = ["FHTH_FOOD","FHTH_DRINK"]

# def get_timestamp():
#     timestamp = datetime.now()
#     time = [timestamp.year,
#             timestamp.month,
#             timestamp.day,
#             timestamp.hour,
#             timestamp.minute,
#             timestamp.second]
#     for i,v in enumerate(time):
#         if v < 10:
#             time[i] = '{0:02d}'.format(v) 

#     return f"{time[0]}{time[1]}{time[2]} {time[3]}:{time[4]}:{time[5]}"

# def post_data(data):
#     try:
#         res = requests.post(url, json=data, headers={})
#         print("Server status: ", res.status_code)
#     except Exception as e:
#         print("Server errors: ", e)

# def xor(condition1, condition2):
#     if condition1:
#         return (not condition2)
#     else:
#         return condition2

# # callbacks
# def generic_error_cb(error):
#     print('D-Bus call failed: ' + str(error))
#     mainloop.quit()

# # 연결 끊겼을 때 remove callback
# def interfaces_removed_cb(object_path, interfaces):
#     print("interfaces removed callback")
#     print(object_path)
#     print(interfaces)

# # registration callbacks
# def food_left_start_notify_cb():
#     print('FOOD-LEFT notifications enabled')

# def food_eaten_start_notify_cb():
#     print('FOOD-EATEN notifications enabled')

# def drink_drink_start_notify_cb():
#     print('DRINK-DRINK notifications enabled')

# def drink_water_start_notify_cb():
#     print('DRINK-WATER notifications enabled')

# # write callback (제대로 write 됐는지 확인용)
# def write_cb():
#     print("Write complete")

# ## write 함수는 AWS->RPi Backend 에서 값을 받아서 write해야 되는 상황
# # 항상 True('1') 값만 보내 하드웨어 동작하게 함
# def write_food_action():
#     if FOOD_EATEN:
#         print("write")
#         str_value = bytes('1'.encode())
#         food_action_chrc[0].WriteValue(str_value, {}, reply_handler=write_cb,
#                                          error_handler=generic_error_cb,
#                                          dbus_interface=GATT_CHRC_IFACE)

# def write_food_amount(amount):
#     print("write")
#     # write는 string으로 보냄
#     str_value = bytes(str(amount).encode())
#     food_amount_chrc[0].WriteValue(str_value, {}, reply_handler=write_cb,
#                                      error_handler=generic_error_cb,
#                                      dbus_interface=GATT_CHRC_IFACE)

# # notify callbacks
# # 음식 먹었는지 여부 notify 오면 해당 값 전역 변수에 저장
# # 나중에 action 값 쓸 때 해당 변수가 True 일 때만 action 보냄
# def food_eaten_changed_cb(iface, changed_props, invalidated_props):
#     global FOOD_EATEN
#     print("eaten notify callback")
#     if iface != GATT_CHRC_IFACE:
#         return

#     if not len(changed_props):
#         return

#     value = changed_props.get('Value', None)
#     if not value:
#         return

#     # strr = [chr for chr in value]
#     # print('notify value: ',value)
#     # print(strr)
#     # print("value:%s" % [bytes([v]) for v in value])
#     print("decoded value: %s" % [bytes([v]).decode() for v in value])
#     strr = [bytes([v]).decode() for v in value]
#     CUR_STATE = None

#     if strr[0] == 'F':
#         CUR_STATE = False
#     elif strr[0] == 'T':
#         CUR_STATE = True

#     # 먹었는지 안 먹었는지 여부도 DB에 보냈던가?? 몰라 일단 보내
#     if CUR_STATE != None:
#         if xor(FOOD_EATEN, CUR_STATE):
#             FOOD_EATEN = CUR_STATE
#             timestamp = get_timestamp()
#             data = {'EATEN': FOOD_EATEN, 'DATE': timestamp}
#             post_data(data)

# # 남은 음식 양 notify 올 때마다 바로 POST
# # int가 아니라 uint8 4바이트가 와서 일단 맨 앞 인덱스만 POST하게 해 둠
# def food_left_changed_cb(iface, changed_props, invalidated_props):
#     print("left notify callback")
#     if iface != GATT_CHRC_IFACE:
#         return

#     if not len(changed_props):
#         return

#     value = changed_props.get('Value', None)
#     if not value:
#         return

#     print("decoded value: %s" % [bytes([v]).decode() for v in value])
#     strr = [bytes([v]).decode() for v in value]
#     # for char in strr:
#     #     print(type(char), char)
#     #     print(ord(char))
#     #     data = {"LEFT": ord(char)}
#     #     post_data(data)
#     left = ord(strr[0])
#     print(strr[0], left)
#     timestamp = get_timestamp()
#     data = {"LEFT": left, 'DATE': timestamp}
#     post_data(data)

# # 마셨는지 notify 올 때마다 POST
# def drink_drink_changed_cb(iface, changed_props, invalidated_props):
#     print("drink notify callback")
#     if iface != GATT_CHRC_IFACE:
#         return

#     if not len(changed_props):
#         return

#     value = changed_props.get('Value', None)
#     if not value:
#         return

#     print("decoded value: %s" % [bytes([v]).decode() for v in value])
#     strr = [bytes([v]).decode() for v in value]
#     # 마셨을 때만 post
#     if strr[0] == '1':
#         timestamp = get_timestamp()
#         data = {'DRINK': True, 'DATE': timestamp}
#         post_data(data)

# # 물 부족 신호가 오면 계속 알림
# # 물 안 부족할 때는 계속 보낼 필요가 없으므로 바뀔 때 한번만 보냄
# def drink_water_changed_cb(iface, changed_props, invalidated_props):
#     global WATER_LACK
#     print("water notify callback")
#     if iface != GATT_CHRC_IFACE:
#         return

#     if not len(changed_props):
#         return

#     value = changed_props.get('Value', None)
#     if not value:
#         return

#     print("decoded value: %s" % [bytes([v]).decode() for v in value])
#     strr = [bytes([v]).decode() for v in value]
#     timestamp = get_timestamp()

#     if strr[0] == '1':
#         WATER_LACK = True
#         data = {'WATER_LACK': True, 'DATE': timestamp}
#         post_data(data)
#     else:
#         if WATER_LACK:
#             WATER_LACK = False
#             data = {'WATER_LACK': False, 'DATE': timestamp}
#             post_data(data)

# # 값 임시로 읽는 콜백. 쓸 일은 없고 그냥 값 제대로 읽어오는지 테스트용
# def temp_cb(value):
#     print("chrc reading callback")
#     print("decode: %s" % [bytes([v]).decode() for v in value])


# def start_client():
#     # test reading
#     food_left_chrc[0].ReadValue({}, reply_handler=temp_cb,
#                                     error_handler=generic_error_cb,
#                                     dbus_interface=GATT_CHRC_IFACE)

#     food_eaten_chrc[0].ReadValue({}, reply_handler=temp_cb,
#                                     error_handler=generic_error_cb,
#                                     dbus_interface=GATT_CHRC_IFACE)
#     food_amount_chrc[0].ReadValue({}, reply_handler=temp_cb,
#                                     error_handler=generic_error_cb,
#                                     dbus_interface=GATT_CHRC_IFACE)
#     food_action_chrc[0].ReadValue({}, reply_handler=temp_cb,
#                                     error_handler=generic_error_cb,
#                                     dbus_interface=GATT_CHRC_IFACE)

#     # test writing
#     write_food_amount(300)


#     # Listen to PropertiesChanged signals
#     food_left_prop_iface = dbus.Interface(food_left_chrc[0], DBUS_PROP_IFACE)
#     food_left_prop_iface.connect_to_signal("PropertiesChanged",
#                                           food_left_changed_cb)

#     food_eaten_prop_iface = dbus.Interface(food_eaten_chrc[0], DBUS_PROP_IFACE)
#     food_eaten_prop_iface.connect_to_signal("PropertiesChanged",
#                                           food_eaten_changed_cb)

#     drink_drink_prop_iface = dbus.Interface(drink_drink_chrc[0], DBUS_PROP_IFACE)
#     drink_drink_prop_iface.connect_to_signal("PropertiesChanged",
#                                           drink_drink_changed_cb)

#     drink_water_prop_iface = dbus.Interface(drink_water_chrc[0], DBUS_PROP_IFACE)
#     drink_water_prop_iface.connect_to_signal("PropertiesChanged",
#                                          drink_water_changed_cb)

#     # # Subscribe to notifications.
#     food_left_chrc[0].StartNotify(reply_handler=food_left_start_notify_cb,
#                                  error_handler=generic_error_cb,
#                                  dbus_interface=GATT_CHRC_IFACE)

#     food_eaten_chrc[0].StartNotify(reply_handler=food_eaten_start_notify_cb,
#                                  error_handler=generic_error_cb,
#                                  dbus_interface=GATT_CHRC_IFACE)

#     drink_drink_chrc[0].StartNotify(reply_handler=drink_drink_start_notify_cb,
#                                  error_handler=generic_error_cb,
#                                  dbus_interface=GATT_CHRC_IFACE)
#     drink_water_chrc[0].StartNotify(reply_handler=drink_water_start_notify_cb,
#                                 error_handler=generic_error_cb,
#                                 dbus_interface=GATT_CHRC_IFACE)


# def process_chrc(chrc_path, svc_no):
#     chrc = bus.get_object(BLUEZ_SERVICE_NAME, chrc_path)
#     chrc_props = chrc.GetAll(GATT_CHRC_IFACE,
#                              dbus_interface=DBUS_PROP_IFACE)

#     uuid = chrc_props['UUID']
#     print(uuid, svc_no)

#     # 서비스 인덱스에 따라 char 등록
#     if svc_no == 0:
#         if uuid == FOOD_CHR_LEFT_UUID:
#             global food_left_chrc
#             food_left_chrc = (chrc, chrc_props)
#             print(food_left_chrc)
#         elif uuid == FOOD_CHR_EATEN_UUID:
#             global food_eaten_chrc
#             food_eaten_chrc = (chrc, chrc_props)
#             print(food_eaten_chrc)
#         elif uuid == FOOD_CHR_AMOUNT_UUID:
#             global food_amount_chrc
#             food_amount_chrc = (chrc, chrc_props)
#             print(food_amount_chrc)
#         elif uuid == FOOD_CHR_ACTION_UUID:
#             global food_action_chrc
#             food_action_chrc = (chrc, chrc_props)
#             print(food_action_chrc)
#         else:
#             print('Unrecognized characteristic: ' + uuid)
#     elif svc_no == 1:
#         if uuid == DRINK_CHR_DRINK_UUID:
#             global drink_drink_chrc
#             drink_drink_chrc = (chrc, chrc_props)
#             print(drink_drink_chrc)
#         elif uuid == DRINK_CHR_WATER_UUID:
#             global drink_water_chrc
#             drink_water_chrc = (chrc, chrc_props)
#             print(drink_water_chrc)
#         else:
#             print('Unrecognized characteristic: ' + uuid)

#     return True


# def process_service(service_path, chrc_paths):
#     service = bus.get_object(BLUEZ_SERVICE_NAME, service_path)
#     service_props = service.GetAll(GATT_SERVICE_IFACE,
#                                    dbus_interface=DBUS_PROP_IFACE)

#     uuid = service_props['UUID']
#     service_number = -1

#     for idx, svc in enumerate(uuid_list):
#         if uuid == svc:
#             service_number = idx

#     if service_number < 0:
#         return False

#     print(f'Service found: {service_number}'+ service_path)

#     # Process the characteristics.
#     for chrc_path in chrc_paths:
#         process_chrc(chrc_path, service_number)

#     service_list[service_number] = (service, service_props, service_path)
#     print(service_number, service_list[service_number])
#     return True


# def main():
#     # Set up the main loop.
#     DBusGMainLoop(set_as_default=True)
#     global bus
#     bus = dbus.SystemBus()
#     global mainloop
#     mainloop = GLib.MainLoop()

#     om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'), DBUS_OM_IFACE)
#     om.connect_to_signal('InterfacesRemoved', interfaces_removed_cb)

#     print('Getting objects...')
#     objects = om.GetManagedObjects()
#     chrcs = []

#     # find device
#     print("Finding Devices...")
#     for path, interfaces in objects.items():
#         dd = interfaces.get(DEVICE_IFACE)
#         if dd is None:
#             continue
#         try:
#             for idx, dev_name in enumerate(dev_name_list):
#                 print(dd["Address"], dd["Name"])
#                 if str(dd["Name"]) == dev_name:
#                     device_list[idx] = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, path), DEVICE_IFACE)
#                     print(device_list[idx])
#                     device_list[idx].Connect()
#                     print(f"device {idx} Connect!!")
#         except Exception as e:
#             print("error: ",e)
#             continue


#     # List characteristics found
#     print("Finding Services...")
#     for path, interfaces in objects.items():
#         if GATT_CHRC_IFACE not in interfaces.keys():
#             continue
#         chrcs.append(path)

#     # List sevices found
#     for path, interfaces in objects.items():
#         if GATT_SERVICE_IFACE not in interfaces.keys():
#             continue

#         chrc_paths = [d for d in chrcs if d.startswith(path + "/")]
#         print(chrc_paths)

#         if process_service(path, chrc_paths):
#             continue

#     for idx, svc in enumerate(service_list):
#         if svc:
#             print(f"service exist: {idx}")

#     try:
#         start_client()
#         mainloop.run()
#     except KeyboardInterrupt:
#         print("keyboard")
#     finally:
#         for idx, dev in enumerate(device_list):
#             if dev:
#                 print(f"device {idx} Disconnect!!")
#                 dev.Disconnect()

# if __name__ == '__main__':
#     main()

print("갇혔어...")
