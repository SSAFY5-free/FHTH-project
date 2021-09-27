#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>

#define SERVICE_UUID        "00002230-0000-1000-8000-00805F9B34FB"
#define CHAR_UUID_DRINK      "00002231-0000-1000-8000-00805F9B34FB"  // 물 마셨는지 여부
#define CHAR_UUID_WATER      "00002232-0000-1000-8000-00805F9B34FB" // 물 보충 여부

// for control motor_driver(water_pump)
#define PUMP_A 12
#define PUMP_B 13

// for read data about water level
#define WATER_LEVEL_PIN 14
// for distance sensor
#define ECHO_PIN 2
#define TRIG_PIN 4 

// waterlevel 1000 이상이면 클라이언트로 1 전송,
// distance 30 이상이면 클라이언트로 1 전송,
#define LIMIT_WATER_LEVEL 1000
#define LIMIT_DISTANCE 30

void BLE_init();
void BLE_loop();
void init_water_divider();
void init_waterpump();
void init_waterlevel();
void active_motor();
void stop_motor();
int check_waterlevel();
void init_distance();
long microsecondsToCentimeters(long microseconds);
int get_distance();

BLEServer* pServer;
BLEService* pService;
BLECharacteristic* pChar_drink;
BLECharacteristic* pChar_water;

bool deviceConnected = false;
bool oldDeviceConnected = false;
bool drink = false;
bool water_lack = false;

class ServerCallbacks: public BLEServerCallbacks {
  void onConnect(BLEServer* pServer){
    deviceConnected = true;
    Serial.println("DRINK: Device Connected");
  }

  void onDisconnect(BLEServer* pServer){
    deviceConnected = false;
    Serial.println("DRINK: Device Disconnected");
  }
};

void setup() {
  Serial.begin(115200);
  BLE_init();
  init_water_divider();
  active_motor();
}

void loop() {
  BLE_loop();
}

void BLE_init(){
  Serial.println("Starting BLE work!");
  BLEDevice::init("FHTH_DRINK");
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new ServerCallbacks());
  pService = pServer->createService(SERVICE_UUID);
  pChar_drink = pService->createCharacteristic(
                                         CHAR_UUID_DRINK,
                                         BLECharacteristic::PROPERTY_NOTIFY |
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );

  pChar_water = pService->createCharacteristic(
                                         CHAR_UUID_WATER,
                                         BLECharacteristic::PROPERTY_NOTIFY |
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );
  
  BLE2902* pDesc2902 = new BLE2902();
  BLE2902* pDesc2902_2 = new BLE2902();
  pDesc2902->setNotifications(true);
  pDesc2902_2->setNotifications(true);
  pChar_drink->addDescriptor(pDesc2902);
  pChar_water->addDescriptor(pDesc2902_2);
  
  pChar_drink->setValue("0");
  pChar_water->setValue("0");
  
  pService->start();
  // BLEAdvertising *pAdvertising = pServer->getAdvertising();  // this still is working for backward compatibility
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  // functions that help with iPhone connections issue
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();
  Serial.println("Characteristic defined! Now you can read it in your phone!");
}

void BLE_loop(){
  if (deviceConnected){
    // 임시로 notify 계속 주는거 관찰하기 위해서
    // drink == true면 false로 바꿔주고 false면 true로 바꿔주면서 notify 함
    if (check_waterlevel()){
      Serial.println("1 보냄!");
      pChar_drink->setValue("1");
      pChar_drink->notify();
    }else{
      Serial.println("0 보냄!");
      pChar_drink->setValue("0");
      pChar_drink->notify();
    }
    delay(3000);
    if (get_distance() > LIMIT_DISTANCE){
      pChar_water->setValue("1");
      pChar_water->notify();
    }else{
      pChar_water->setValue("0");
      pChar_water->notify();
    }
    delay(3000);
  }
  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
    Serial.println("DRINK: disconnecting~~");
    delay(500); // give the bluetooth stack the chance to get things ready
    pServer->startAdvertising(); // restart advertising
    Serial.println("DRINK: start advertising");
    oldDeviceConnected = deviceConnected;
  }
  // connecting
  if (deviceConnected && !oldDeviceConnected) {
    Serial.println("DRINK: connecting~~");
    // do stuff here on connecting
    oldDeviceConnected = deviceConnected;
  }
}

void init_water_divider(){
  init_waterpump();
  init_waterlevel();
  init_distance();
}

void init_waterpump() {
  pinMode( PUMP_A,   OUTPUT); // 12번 핀을 워터펌프 제어를 위한 출력으로 설정
  pinMode( PUMP_B,   OUTPUT); // 13번 핀을 워터펌프 제어를 위한 출력으로 설정
}

void init_distance(){
  pinMode(TRIG_PIN,OUTPUT); // 센서 Trig 핀
  pinMode(ECHO_PIN,INPUT); // 센서 Echo 핀
}

void init_waterlevel(){
  pinMode( WATER_LEVEL_PIN,   INPUT); // 14번 핀을 수위센서를 위한 입력핀으로 설정
}


void active_motor(){
  digitalWrite(PUMP_A, HIGH);
  digitalWrite(PUMP_B, LOW);
}

void stop_motor(){
  digitalWrite(PUMP_A, LOW);
  digitalWrite(PUMP_B, LOW); 
}

int check_waterlevel(){
  int level = analogRead(WATER_LEVEL_PIN);
  Serial.println("Water Level is " + String(level));
  if (level > LIMIT_WATER_LEVEL){
    return 1;
  }
  return 0;
}

long microsecondsToCentimeters(long microseconds){
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  return microseconds / 29 / 2;
}

int get_distance(){
  long duration, cm;

  digitalWrite(TRIG_PIN,HIGH); // 센서에 Trig 신호 입력
  delayMicroseconds(10); // 10us 정도 유지
  digitalWrite(TRIG_PIN,LOW); // Trig 신호 off

  duration = pulseIn(ECHO_PIN,HIGH); // Echo pin: HIGH->Low 간격을 측정
  cm = microsecondsToCentimeters(duration); // 거리(cm)로 변환
  Serial.println(cm);

  return cm;
}
