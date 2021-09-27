// 현재 사용중인 핀 번호 2 4 12 13 16 25 26 27 
// 쓸수있는 핀 번호 32 33

// 라이브러리
#include <ESP32_Servo.h> // <ESP32_Servo.h>에서 구동확인 타 소스 호환가능
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>
#include "HX711.h" //HX711로드셀 엠프 관련함수 호출

#define calibration_factor -450.0 // 로드셀 스케일 값 선언(케이싱 후 맞춰줘야함)
#define ECHO_PIN 2
#define TRIG_PIN 4
#define CLK  12  //엠프 클락 핀 넘버 
#define DOUT  13 //엠프 데이터 아웃 핀 넘버 선언
#define ECHO_PIN2 25
#define TRIG_PIN2 26
#define servo180_Pin 16 // 배식
#define servo360_Pin 27 // 사료량 조절

#define SERVICE_UUID        "00002220-0000-1000-8000-00805F9B34FB"
#define CHAR_UUID_LEFT      "00002221-0000-1000-8000-00805F9B34FB"  // 남은 사료 양

#define CHAR_UUID_EATEN     "00002222-0000-1000-8000-00805F9B34FB"  // 사료 먹었는지 여부
#define CHAR_UUID_AMOUNT    "00002223-0000-1000-8000-00805F9B34FB"  // 급식량
#define CHAR_UUID_ACTION    "00002224-0000-1000-8000-00805F9B34FB"  // 급식기 작동 플래그 
 
#define True 1
#define False 0
#define TRUE 1
#define FALSE 0

/// 수정
int food_amount = 100; // 한번에 급식량
int dog_eat = 20; // 개가 밥먹을때 거리값cm

bool deviceConnected = false;
bool oldDeviceConnected = false;

HX711 scale;
Servo servo180;
Servo servo360;

BLEServer* pServer;
BLEService* pService;
BLECharacteristic* pChar_left;
BLECharacteristic* pChar_eaten;
BLECharacteristic* pChar_amount;
BLECharacteristic* pChar_action;

void board_init();
void loadcell_init();
int loadcell_action(float target_weight);
void servo360_init();
void servo360_action();
void servo180_init();
void servo180_action();
long microsecondsToCentimeters(long microseconds);
void distance_init();
int get_distance();
int get_distance2();
void hardware_action();
void BLE_init();
void BLE_loop();

class ServerCallbacks: public BLEServerCallbacks {
  void onConnect(BLEServer* pServer){
    deviceConnected = true;
    Serial.println("FOOD: Device Connected");
  } 

  void onDisconnect(BLEServer* pServer){
    deviceConnected = false;
    Serial.println("FOOD: Device Disconnected");
  }
};

void setup() {
  board_init();
  loadcell_init();
  servo360_init();
  servo180_init();
  distance_init();
  BLE_init();
  Serial.println(String("FOOD: Setup Done"));
}

void loop() {
  BLE_loop();
}

void BLE_init(){
  Serial.println("FOOD: Starting BLE work!");
  BLEDevice::init("FHTH_FOOD");
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new ServerCallbacks());
  pService = pServer->createService(SERVICE_UUID);
  pChar_left = pService->createCharacteristic(
                                         CHAR_UUID_LEFT,
                                         BLECharacteristic::PROPERTY_NOTIFY |
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );
  pChar_eaten = pService->createCharacteristic(
                                         CHAR_UUID_EATEN,
                                         BLECharacteristic::PROPERTY_NOTIFY |
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );
  pChar_amount = pService->createCharacteristic(
                                         CHAR_UUID_AMOUNT,
                                         BLECharacteristic::PROPERTY_NOTIFY |
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );

  pChar_action = pService->createCharacteristic(
                                         CHAR_UUID_ACTION,
                                         BLECharacteristic::PROPERTY_NOTIFY |
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );
  
  BLE2902* pDesc2902 = new BLE2902();
  BLE2902* pDesc2902_2 = new BLE2902();
  BLE2902* pDesc2902_3 = new BLE2902();
  BLE2902* pDesc2902_4 = new BLE2902();

  pDesc2902->setNotifications(true);
  pDesc2902_2->setNotifications(true);
  pDesc2902_3->setNotifications(true);
  pDesc2902_4->setNotifications(true);

  pChar_left->addDescriptor(pDesc2902);
  pChar_eaten->addDescriptor(pDesc2902_2);
  pChar_action->addDescriptor(pDesc2902_3);
  pChar_amount->addDescriptor(pDesc2902_4);

  pChar_left->setValue("0");
  pChar_eaten->setValue("0");
  pChar_action->setValue("0");
  pChar_amount->setValue("0");
  
  pService->start();
  // BLEAdvertising *pAdvertising = pServer->getAdvertising();  // this still is working for backward compatibility
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  // functions that help with iPhone connections issue
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();
  Serial.println("FOOD: Characteristic defined! Now you can read it in your phone!");
}

void BLE_loop(){
  char restchar[4];
  int restint=0;
  if (deviceConnected){
    std::string temp = pChar_amount->getValue();
    String temp2=temp.c_str();
    
    Serial.println("AMOUNT!");
    Serial.println(temp2.toInt());
    if(!temp2.toInt()){
      pChar_amount->setValue("2");
      pChar_amount->notify();
      food_amount=2;
    }
    else{
      food_amount=temp2.toInt();
    }
    
    temp=pChar_action->getValue();
    temp2=temp.c_str();
    Serial.println("READ ACTION!");
    Serial.println(temp2.toInt());
    if(temp2.toInt()) {
      hardware_action();
      pChar_action->setValue("0");
      pChar_action->notify();
    }
    
    restint= (10-get_distance())*10;
    if(restint > 99){
      restchar[0]=1+48;
      restchar[1]=0+48;
      restchar[2]=0+48;
      restchar[3]='\0';
    }
    else if(restint > 9){
      restchar[0]=restint/10+48;
      restchar[1]=restint%10+48;
      restchar[2]='\0';
      restchar[3]='\0';
    }
    else if(restint > 0){
      restchar[0]=restint+48;
      restchar[1]='\0';
      restchar[2]='\0';
      restchar[3]='\0';
    }
    else{
      restchar[0]= 0+48;
      restchar[1]='\0';
      restchar[2]='\0';
      restchar[3]='\0';
    }
    Serial.print("남은 사료량 : ");
    Serial.println(restchar);
    pChar_left->setValue(restchar);
    pChar_left->notify();

    if (get_distance2() < dog_eat){
      Serial.println("Dog eat food");
      pChar_eaten->setValue("1");
      pChar_eaten->notify();
    }
    else{
      pChar_eaten->setValue("0");
      pChar_eaten->notify();
    }
    delay(1000);
  }  
  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
    Serial.println("FOOD: disconnecting~~");
      delay(500); // give the bluetooth stack the chance to get things ready
      pServer->startAdvertising(); // restart advertising
      Serial.println("FOOD: start advertising");
      oldDeviceConnected = deviceConnected;
  }
  // connecting
  if (deviceConnected && !oldDeviceConnected) {
    Serial.println("FOOD: connecting~~");
      // do stuff here on connecting
      oldDeviceConnected = deviceConnected;
  }
}

void board_init(){
  Serial.begin(115200);
  Serial.println("FOOD: Board init");
}

void servo180_init(){
  servo180.attach(servo180_Pin);
}

void servo360_init(){
  servo360.attach(servo360_Pin);
}

void loadcell_init(){
  scale.begin(DOUT, CLK);
  Serial.println("HX711 scale TEST");
  scale.set_scale(calibration_factor);  // 스케일 지정
  scale.tare();  // 영점 설정 : 현재 상태가 0이 됨
  scale.get_units(10);
  Serial.print("initial reading : ");
  Serial.println(scale.get_units(2));
}

void distance_init(){
  pinMode(TRIG_PIN,OUTPUT); // 센서 Trig 핀
  pinMode(ECHO_PIN,INPUT); // 센서 Echo 핀
  pinMode(TRIG_PIN2,OUTPUT); // 센서 Trig2 핀
  pinMode(ECHO_PIN2,INPUT); // 센서 Echo2 핀
}

long microsecondsToCentimeters(long microseconds){
  return microseconds / 29 / 2;
}

int get_distance(){
  long duration, cm;

  digitalWrite(TRIG_PIN,HIGH); // 센서에 Trig 신호 입력
  delayMicroseconds(10); // 10us 정도 유지
  digitalWrite(TRIG_PIN,LOW); // Trig 신호 off

  duration = pulseIn(ECHO_PIN,HIGH); 
  cm = microsecondsToCentimeters(duration);
  Serial.print("남은 사료거리");
  Serial.println(cm);
  return cm;
}

int get_distance2(){
  long duration, cm;

  digitalWrite(TRIG_PIN2,HIGH); // 센서에 Trig 신호 입력
  delayMicroseconds(10); // 10us 정도 유지
  digitalWrite(TRIG_PIN2,LOW); // Trig 신호 off

  duration = pulseIn(ECHO_PIN2,HIGH); // Echo pin: HIGH->Low 간격을 측정
  cm = microsecondsToCentimeters(duration); // 거리(cm)로 변환
  Serial.print("급식기 개와의 거리");
  Serial.println(cm);
  return cm;
}

void servo360_action(){
  for(int posDegrees = 30; posDegrees < 75; posDegrees++) {
      servo360.write(posDegrees);
      delay(25);
  }  
  return;
}

void servo180_action(){
    for(int posDegrees = 83; posDegrees >= 23; posDegrees--) {
        servo180.write(posDegrees);
        delay(30);
    }
    
    for(int posDegrees = 23; posDegrees <= 83; posDegrees++) {
        servo180.write(posDegrees);
        delay(30);
    }
    delay(1000);
    return;
}

int loadcell_action(int target_weight){
  int food_weight = scale.get_units(2);
  Serial.print("load cell weight : ");
  Serial.println(food_weight);
  if (food_weight >= target_weight){
    servo180_action();
    return 1;
  }
  return 0;
}

void hardware_action(){
    while(1){
      servo360_action();
      if(loadcell_action(food_amount)){
        return;
      }
  }  
}
