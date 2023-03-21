// Code to control three stepper motors and two LEDs in parallel using freeRTOS. Steppers are denoted X, Y, Z
// Christopher Ashe
// University of Strathclyde
// 01-03-2022

#include <Arduino.h>
#include <Stepper.h>
#include <Ps3Controller.h>
 
// ---------------- Pin Assignment ------------ //

const int XA1A = 5; //X Stage Stepper Pins
const int XA1B = 18;
const int XB1A = 19;
const int XB1B = 21;

const int YA1A = 5; //X Stage Stepper Pins
const int YA1B = 18;
const int YB1A = 19;
const int YB1B = 21;

const int ZA1A = 5; //Z Stage Stepper Pins
const int ZA1B = 18;
const int ZB1A = 19;
const int ZB1B = 21;

const int blueLedPin = 12; // Blue LED
const int limeLedPin = 13; // Lime LED

const int xControlPin = 15; //X,Y,Z Switches
const int yControlPin = 16;
const int zControlPin = 17;

// ---------------- Variables ------------ //

const int stepsPerRevolution = 200; // motor steps for one revolution
const float stepAngle = 1.8; // motor step angle in degrees
const float stepRad = stepAngle * (3.141 / 180); // step angle in radians 

int blueBrightness = 0; // starting brightness for the blue LED
int limeBrightness = 0; // starting brightness for the lime LED

int fadeAmount = 17; // How much to change the brightness each step when fading
bool isFading = false; // Whether the LED is currently fading

int xPosition = 0;  //initialising stepper positions
int yPosition = 0;
int zPosition = 0;

float Revs = 1; //Enter number of Revs here

// Screw Equation, gives linear displacement of Z stage
float linDispScrew = tan(0.5236) * 0.5 * 2 * 3.14159; 

// ---------------- Stepper.h functions ------------ //

Stepper myStepperX(stepsPerRevolution,XA1A,XA1B,XB1A,XB1B); // X
Stepper myStepperY(stepsPerRevolution,YA1A,YA1B,YB1A,YB1B); // Y 
Stepper myStepperZ(stepsPerRevolution,ZA1A,ZA1B,ZB1A,ZB1B); // Z 

// ------------------ Z Stage Stepper function -------------- //

void stepZ(void *parameters) {
    for (;;) {
        if (Serial.available()) {
            char receivedZ = Serial.read();
            if (receivedZ == 'd') {
                Serial.println("Displacing -Z");
                zPosition = zPosition - linDispScrew; //What ESP32 thinks displacement is
                Serial.println("\nZ position: ");
                Serial.println(zPosition);
                Serial.println("mm");
                //This performs actual rotation, should translate to Downward displacement
                myStepperZ.step(-Revs * stepsPerRevolution); 
            }
            else if (receivedZ == 'u') {
                Serial.println("Displacing +Z");
                zPosition = zPosition + linDispScrew ; //What ESP32 thinks displacement is
                Serial.print("\nZ Position:  ");
                Serial.print(zPosition);
                Serial.println("mm");
                //This performs actual rotation, should translate to Upward displacement
                myStepperZ.step(Revs * stepsPerRevolution);
            }
            else if (receivedZ == 'r') {
                zPosition = 0; //Reset the gauge displacement if char received is an r
                Serial.println("Z Position set to 0 mm.");
            }
        }
        vTaskDelay(30 / portTICK_PERIOD_MS); //This adds a short delay before starting a queued function
    }
}

// ------------------ Y Stage Stepper function -------------- //

void stepY(void *parameters) {
    for (;;) {
        if (Serial.available()) {
            char receivedY = Serial.read();
            if (receivedY == 'l') {
                Serial.println("Displacing -Y");
                yPosition = yPosition - linDispScrew; //What ESP32 thinks displacement is
                Serial.println("\nY position: ");
                Serial.println(yPosition);
                Serial.println("mm");
                //This performs actual rotation, should translate to -Y displacement
                myStepperY.step(-Revs * stepsPerRevolution); 
            }
            else if (receivedY == 'r') {
                Serial.println("Displacing +Y");
                yPosition = yPosition + linDispScrew ; //What ESP32 thinks displacement is
                Serial.print("\nY Position: ");
                Serial.print(yPosition);
                Serial.println("mm");
                //This performs actual rotation, should translate to Upward displacement
                myStepperY.step(Revs * stepsPerRevolution);
            }
            else if (receivedY == 'r') {
                zPosition = 0; //Reset the gauge displacement if char received is an r
                Serial.println("Y Position set to 0 mm.");
            }
        }
        vTaskDelay(30 / portTICK_PERIOD_MS); //This adds a short delay before starting a queued function
    }
}

// ---------------- X Stage Stepper function ------------ //

void stepX(void *parameters) {
    for (;;) {
        if (Serial.available()) {
            char receivedX = Serial.read();
            if (receivedX == 'l') {
                Serial.println("Displacing -X");
                xPosition = xPosition - linDispScrew; //What ESP32 thinks displacement is
                Serial.println("\nx position: ");
                Serial.println(xPosition);
                Serial.println("mm");
                //This performs actual rotation, should translate to -Y displacement
                myStepperX.step(-Revs * stepsPerRevolution); 
            }
            else if (receivedX == 'r') {
                Serial.println("Displacing +X");
                xPosition = xPosition + linDispScrew ; //What ESP32 thinks displacement is
                Serial.print("\nX Position: ");
                Serial.print(xPosition);
                Serial.println("mm");
                //This performs actual rotation, should translate to Upward displacement
                myStepperX.step(Revs * stepsPerRevolution);
            }
            else if (receivedX == 'r') {
                xPosition = 0; //Reset the gauge displacement if char received is an r
                Serial.println("X Position set to 0 mm.");
            }
        }
        vTaskDelay(30 / portTICK_PERIOD_MS); //This adds a short delay before starting a queued function
    }
}

// ---------------- Blue LED Control function ------------ //

void blueLed(void *parameters) {
    for (;;) {
        if (Serial.available()) {
            char blueInput = Serial.read();
            if (blueInput == '1'){
                blueBrightness = max(0, blueBrightness - 32); // decrease brightness by 32 (out of 255)
                analogWrite(blueLedPin, blueBrightness);
                Serial.print("\n");
                Serial.print("Current Blue LED Brightness: ");
                Serial.print(blueBrightness);
                Serial.print('\n');
            } 
            else if (blueInput == '2'){
                blueBrightness = min(255, blueBrightness + 32); // increase brightness by 32 (out of 255)
                analogWrite(blueLedPin, blueBrightness);
                Serial.print("\n");
                Serial.print("Current Blue LED Brightness: ");
                Serial.print(blueBrightness);
                Serial.print('\n');
            }
            else if (blueInput == 'f'){
                // Toggle fading on or off
                isFading = !isFading;
                if (isFading) {
                    Serial.println("Fading started");
                } 
                else {
                    Serial.println("Fading stopped");
                }
            }
        }
        if (isFading) {
            blueBrightness += fadeAmount;
            if (blueBrightness <= 0 || blueBrightness >= 255) {
                // Reverse the fade direction when the brightness reaches the min or max value
                fadeAmount = -fadeAmount;
            }
            analogWrite(blueLedPin, blueBrightness); //Write the updated brightness value to Pin
            vTaskDelay(50 / portTICK_PERIOD_MS); //small delay between brightness updates
        } 
        else {
            blueBrightness = 255; //Otherwise have 0 Brightness
        }
    }
}

// ---------------- Lime LED Control function ------------ //

void limeLed(void *parameters) {
    for (;;) {
        if (Serial.available()) {
            char limeInput = Serial.read();
            if (limeInput == '1'){
                limeBrightness = max(0, limeBrightness - 32); // decrease brightness by 32 (out of 255)
                analogWrite(limeLedPin, limeBrightness);
                Serial.print("\n");
                Serial.print("Current Lime LED Brightness: ");
                Serial.print(limeBrightness);
                Serial.print('\n');
            } 
            else if (limeInput == '2'){
                blueBrightness = min(255, limeBrightness + 32); // increase brightness by 32 (out of 255)
                analogWrite(limeLedPin, limeBrightness);
                Serial.print("\n");
                Serial.print("Current Lime LED Brightness: ");
                Serial.print(limeBrightness);
                Serial.print('\n');
            }
            else if (limeInput == 'f'){
                // Toggle fading on or off
                isFading = !isFading;
                if (isFading) {
                    Serial.println("Fading started");
                } 
                else {
                    Serial.println("Fading stopped");
                }
            }
        }
        if (isFading) {
            limeBrightness += fadeAmount;
            if (limeBrightness <= 0 || limeBrightness >= 255) {
                // Reverse the fade direction when the brightness reaches the min or max value
                fadeAmount = -fadeAmount;
            }
            analogWrite(limeLedPin, blueBrightness); //Write the updated brightness value to Pin
            vTaskDelay(50 / portTICK_PERIOD_MS); //small delay between brightness updates
        } 
        else {
            limeBrightness = 255; //Otherwise have 0 Brightness
        }
    }
}

// ---------------- Setup: Simply calls the above Functions ------------ //

void setup()
{
    pinMode(limeLedPin, OUTPUT);
    pinMode(blueLedPin,OUTPUT);
    pinMode(xControlPin,OUTPUT);
    pinMode(yControlPin,OUTPUT);
    pinMode(zControlPin,OUTPUT);
    Serial.begin(115200); 
    myStepperZ.setSpeed(60); // set the speed of the stepper motors to 60 rpm
    myStepperX.setSpeed(60);
    myStepperY.setSpeed(60);

// ---------------- Function Calls ------------ //

    // xTaskCreate(
    //     stepZ,
    //     "stepZ",
    //     1000,
    //     NULL,
    //     1,
    //     0
    // );

    //     xTaskCreate(
    //     blueLed,
    //     "blueLed",
    //     1000,
    //     NULL,
    //     1,
    //     1
    // );

    //     xTaskCreate(
    //     limeLed,
    //     "limeLed",
    //     1000,
    //     NULL,
    //     1,
    //     1
    // );

    //     xTaskCreate(
    //     stepY,
    //     "stepY",
    //     1000,
    //     NULL,
    //     0,
    //     0
    // );

        xTaskCreate(
        stepX,
        "stepX",
        1000,
        NULL,
        1,
        0
    );

}


// Loop Not used //
void loop(){
}