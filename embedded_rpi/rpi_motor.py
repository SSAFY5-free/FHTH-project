# 모터 드라이버 다운받는 곳
# http://raspberrypiwiki.com/images/a/ac/Raspi-MotorHAT-python3.zip
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM

# MotorControl 클래스를 통해서 동작시킬수 있음
class MotorControl:
    def __init__(self, m_ch, ch=0):
        super().__init__()
        # Motor 설정
        self.mh = Raspi_MotorHAT(addr=0x6f)
        self.myMotor = self.mh.getMotor(m_ch)

        # Servo 초기화
        self.pwm = PWM(0x6F)
        self.pwm.setPWMFreq(60)

        # Servo 중간으로 맞추기
        self.ch = ch
        self.pwm.setPWM(self.ch, 0, 350)

    # go 뒷바퀴 모터를 전방으로 회전시킵니다.
    def go(self, speed=100):
        print(f"MOTOR GO : speed {speed}")
        self.myMotor.setSpeed(speed)
        self.myMotor.run(Raspi_MotorHAT.FORWARD)

    # back 뒷바퀴 모터를 후방으로 회전시킵니다.
    def back(self, speed=100):
        print(f"MOTOR BACK : speed {speed}")
        self.myMotor.run(Raspi_MotorHAT.BACKWARD)

    # stop 뒷바퀴 모터를 정지 시킵니다.
    def stop(self):
        self.myMotor.run(Raspi_MotorHAT.RELEASE)

    # left 앞바퀴 좌측으로 조향, value 값을 같이 입력하면 원하는 만큼 조향 가능
    def left(self, value=300):
        print(f"MOTOR LEFT : {value}")
        self.pwm.setPWM(self.ch, 0, value)

    # right 앞바퀴 우측으로 조향, value 값을 같이 입력하면 원하는 만큼 조향 가능
    def right(self, value=430):
        print(f"MOTOR RIGHT : {value}")
        self.pwm.setPWM(self.ch, 0, value)

    # left 앞바퀴 중앙으로 조향.
    def middle(self):
        print("MOTOR MIDDLE")
        self.pwm.setPWM(self.ch, 0, 350)

if __name__ == "__main__":
    motor = MotorControl(2)
    try:
        while 1:
            cmd = input("input: ")
            if cmd == "go":
                motor.go()
            elif cmd == "stop":
                motor.stop()
            elif cmd == "back":
                motor.back()
            elif cmd == "left":
                motor.left()
            elif cmd == "right":
                motor.right()
            elif cmd == "middle":
                motor.middle()
            else:
                print("Wrong Command")

    except KeyboardInterrupt:
        print("keyboard")
