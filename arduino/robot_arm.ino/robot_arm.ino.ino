#include <Dhcp.h>
#include <Dns.h>
#include <Ethernet.h>
#include <EthernetClient.h>
#include <EthernetServer.h>
#include <EthernetUdp.h>

#include <Servo.h>

Servo baseServo;
Servo rArmServo;
Servo lArmServo;
Servo gripServo;
int GRIP_OPEN = 90;
int GRIP_CLOSE = 110;

void setup() {
  Serial.begin(9600);
  Serial.write("Arm Control\n");
  Serial.write("[lrb]angle\n");
  Serial.write("g[01]\n");
  
  baseServo.write(90);
  baseServo.attach(3);
  delay(100);
  
  rArmServo.write(45);
  rArmServo.attach(5);
  delay(100);

  lArmServo.write(100);
  lArmServo.attach(6);

  delay(100);
  gripServo.write(GRIP_OPEN);
  gripServo.attach(9);
}

void loop() {
  if (Serial.available() > 0) {
    byte servo = Serial.read();
    int angle = Serial.parseInt();

    switch (servo) {
      case 'l':
        Serial.print("left\n");
        lArmServo.write(angle);
        break;
      case 'r':
        Serial.print("right\n");
        rArmServo.write(angle);
        break;
      case 'b':
        Serial.print("base\n");
        baseServo.write(angle);
        break;
      case 'g':
        if (angle == 0) {
          Serial.write("Open grip\n");
          gripServo.write(GRIP_OPEN);
        } else if (angle == 1) {
          Serial.write("Close grip\n");
          gripServo.write(GRIP_CLOSE);
        }
        break;
      default:
        Serial.print("nothing\n");
    }
  }
}

