#include <Servo.h>

Servo servo;

void setup() {
  servo.attach(5);  // Set the servo pin
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    int angle = Serial.parseInt();
    if (angle >= 0 && angle <= 180) {
      servo.write(angle);
    }
  }
  delay(20);
}
