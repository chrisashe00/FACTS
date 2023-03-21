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

const int ZA1A = 14; //Z Stage Stepper Pins
const int ZA1B = 27;
const int ZB1A = 26;
const int ZB1B = 25;
const int ZSLP = 33;
const int ZULT = 32;

const int blueLedPin = 12; // Blue LED
const int limeLedPin = 13; // Lime LED

const int xControlPin = 15; //X,Y,Z Switches
const int yControlPin = 16;
const int zControlPin = 17;

const int stepsPerRevolution = 200;


// ---------------- Variables ------------ //

Stepper myStepperX(stepsPerRevolution,XA1A,XA1B,XB1A,XB1B); // X
Stepper myStepperY(stepsPerRevolution,YA1A,YA1B,YB1A,YB1B); // Y 
Stepper myStepperZ(stepsPerRevolution,ZA1A,ZA1B,ZB1A,ZB1B); // Z 


// ------------------ Z Stage Stepper function -------------- //
void stepZ(void *parameters){
    for (;;) {

        if (Serial.available()){
            char receivedZ = Serial.read();

            switch(receivedZ){

            case '1': 

            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(10);
            Serial.print("Stepping 5 steps CW \n");
            digitalWrite(ZSLP, LOW);
            break;

            case '2': 
            vTaskDelay(10 / portTICK_PERIOD_MS);
            digitalWrite(ZSLP,HIGH);
            myStepperZ.step(-10);
            Serial.print("Stepping 5 steps CCW \n");
            digitalWrite(ZSLP, LOW);
            break;

            case '3': 

            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(5);
            Serial.print("Stepping 5 steps CW \n");
            digitalWrite(ZSLP, LOW);
            break;

            case '4': 
            vTaskDelay(10 / portTICK_PERIOD_MS);
            digitalWrite(ZSLP,HIGH);
            myStepperZ.step(-5);
            Serial.print("Stepping 5 steps CCW \n");
            digitalWrite(ZSLP, LOW);
            break;

            default:

            vTaskDelay(10 / portTICK_PERIOD_MS);

            break;
            }
  
}
            else{
                vTaskDelay(10 / portTICK_PERIOD_MS);
                taskYIELD();
                
            }
}
}


void setup(){


    pinMode(limeLedPin, OUTPUT);
    pinMode(blueLedPin,OUTPUT);

    pinMode(ZA1A,OUTPUT);
    pinMode(ZA1B,OUTPUT);
    pinMode(ZB1A,OUTPUT);
    pinMode(ZB1B,OUTPUT);
    pinMode(ZSLP, OUTPUT);
    pinMode(ZULT,OUTPUT);

    Serial.begin(115200); 
    myStepperZ.setSpeed(20); // set the speed of the stepper motors to 60 rpm
    myStepperX.setSpeed(60);

// ---------------- Function Calls ------------ //

    xTaskCreate(
        stepZ,
        "stepZ",
        2048,
        NULL,
        1,
        NULL
    );

}


void loop(){}