#include <Arduino.h>

const int STEP_PIN = 26;   // connect the STEP pin of A4988 stepper driver to Arduino pin 3
const int DIR_PIN = 27;    // connect the DIR pin of A4988 stepper driver to Arduino pin 4
const int STEPS_PER_REV = 200; // number of steps per revolution for your stepper motor

void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'h') {
      // Set the direction to clockwise
      digitalWrite(DIR_PIN, HIGH);

      // Step the motor one revolution
      for (int i = 0; i < STEPS_PER_REV; i++) {
        digitalWrite(STEP_PIN, HIGH);
        delayMicroseconds(500);
        digitalWrite(STEP_PIN, LOW);
        delayMicroseconds(500);
      }

      // Send an acknowledgement message back to the Jetson
      Serial.println("Motor stepped one revolution. UP");
    }


    if (command == 'l') {
      // Set the direction to clockwise
      digitalWrite(DIR_PIN, LOW);

      // Step the motor one revolution
      for (int i = 0; i < STEPS_PER_REV; i++) {
        digitalWrite(STEP_PIN, HIGH);
        delayMicroseconds(500);
        digitalWrite(STEP_PIN, LOW);
        delayMicroseconds(500);
      }

      // Send an acknowledgement message back to the Jetson
      Serial.println("Motor stepped one revolution. DOWN");
    }
  }
}
