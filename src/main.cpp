#include <Arduino.h>
#include <Stepper.h>
#include <Ps3Controller.h>

// change this to the number of steps on your motor
#define STEPS 200

// create an instance of the stepper class, specifying
// the number of steps of the motor and the pins it's
// attached to

const int stepPin = 26;
const int dirPin = 27;

void setup() {
  Serial.begin(115200);
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

void rotateClockwise() {
  digitalWrite(dirPin, HIGH);
  Serial.println("Rotating full clockwise (UP)");
  for (int i = 0; i < 400; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1000);
  }
}

void rotateCounterClockwise() {
  digitalWrite(dirPin, LOW);
  Serial.println("Rotating full counter-clockwise (DOWN)");
  for (int i = 0; i < 400; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1000);
  }
}

void rotateClockwiseStep() {
  digitalWrite(dirPin, HIGH);
  Serial.println("Rotating steps clockwise (UP)");
  for (int i = 0; i < 10; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1000);
  }
}

void rotateCounterClockwiseStep() {
  digitalWrite(dirPin, LOW);
  Serial.println("Rotating steps counter clockwise (DOWN)");
  for (int i = 0; i < 10; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1000);
  }
}


void loop() {
  if (Serial.available() > 0) {
    char c = Serial.read();
    switch (c) {
      case 'h':
        rotateClockwise();
        break;
      case 'l':
        rotateCounterClockwise();
        break;
      case 'r':
        rotateClockwiseStep();
        break;
      case 't':
        rotateCounterClockwiseStep();
        break;
    }
  }
}


