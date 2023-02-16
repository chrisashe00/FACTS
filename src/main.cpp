#include <Arduino.h>
#include <Stepper.h>

const int stepsPerRevolution = 200;  // change this to fit the number of steps per revolution
// for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 14, 27, 26, 25);
// define LED pin
const int LED_PIN = 12; // change this to match the pin you've connected the LED to
int brightness = 128; // starting brightness for the LED

void setup() {
  // initialize serial communication
  Serial.begin(115200);
  // set LED pin as output
  pinMode(LED_PIN, OUTPUT);

  myStepper.setSpeed(60);
  // initialize the serial port:

}

void loop() {
  // read serial input
  // if (Serial.available()) {
  //   char input = Serial.read();
  //   if (input == '8') {
  //     brightness = max(0, brightness - 32); // decrease brightness by 32 (out of 255)
  //     analogWrite(LED_PIN, brightness);
  //   } else if (input == '9') {
  //     brightness = min(255, brightness + 32); // increase brightness by 32 (out of 255)
  //     analogWrite(LED_PIN, brightness);
  //   }
  // }

  Serial.println("clockwise");
  myStepper.step(stepsPerRevolution);
  delay(500);

  // step one revolution in the other direction:
  Serial.println("counterclockwise");
  myStepper.step(-stepsPerRevolution);
  delay(500);
}
