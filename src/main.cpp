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

const int YA1A = 5; //Y Stage Stepper Pins
const int YA1B = 18;
const int YB1A = 19;
const int YB1B = 21;

const int ZA1A = 14; //Z Stage Stepper Pins
const int ZA1B = 27;
const int ZB1A = 26;
const int ZB1B = 25;
const int ZSLP = 33;
const int ZULT = 32;

const int fanCMDPin = 13; // Fan PWM pin 
const int limeLedPin = 0; // Lime LED pin
const int blueLedPin = 0; //Blue LED pin

// ---------------- PS3 Controller Initialise ------------ //
int player = 0;
int battery = 0;

// ---------------- Variables ------------ //

const int stepsPerRev = 200; // motor steps for one revolution
const float stepAngle = 1.8; // motor step angle in degrees

int blueBrightness = 255; // starting brightness for the blue LED
int limeBrightness = 255; // starting brightness for the lime LED
int fanBrightness = 255;

int fadeAmount = 17; // How much to change the brightness each step when fading
bool isFading = false; // Whether the LED is currently fading

int xPosition = 0;  //initialising stepper positions
int yPosition = 0;
int zPosition = 0;


// ---------------- Stepper.h functions ------------ //

Stepper myStepperX(stepsPerRev,XA1A,XA1B,XB1A,XB1B); // X
Stepper myStepperY(stepsPerRev,YA1A,YA1B,YB1A,YB1B); // Y 
Stepper myStepperZ(stepsPerRev,ZA1A,ZA1B,ZB1A,ZB1B); // Z 

// ------------------ Connect PS3 controller -------------- //
// void onConnect(){
//     Serial.println("Connected.");
// }

// ------------------ Z Stage Stepper function -------------- //

void stepZ(void *parameters) {
    for (;;) {
        if (Serial.available()){
            char receivedZ = Serial.read();
            switch(receivedZ){
                case '1':
                    digitalWrite(ZSLP,HIGH);
                    vTaskDelay(50 / portTICK_PERIOD_MS);
                    myStepperZ.step(1);
                    Serial.println("Z stage performing +1 step");
                    digitalWrite(ZSLP, LOW);
                    break;

                case '2':
                    digitalWrite(ZSLP,HIGH);
                    vTaskDelay(50 / portTICK_PERIOD_MS);
                    myStepperZ.step(-1);
                    Serial.println("Z stage performing -1 step");
                    digitalWrite(ZSLP, LOW);
                    break;

                case '3':
                    digitalWrite(ZSLP,HIGH);
                    myStepperZ.step(10);
                    Serial.println("Z stage performing +10 steps");
                    digitalWrite(ZSLP, LOW);
                    break;

                case '4':
                    digitalWrite(ZSLP,HIGH);
                    myStepperZ.step(-10);
                    Serial.println("Z stage performing -10 steps");
                    digitalWrite(ZSLP, LOW);
                    break;

                case '5':
                    digitalWrite(ZSLP,HIGH);
                    myStepperZ.step(50);
                    Serial.println("Z stage performing 50 steps");
                    digitalWrite(ZSLP, LOW);
                    break;

                case '6':
                    digitalWrite(ZSLP,HIGH);
                    myStepperZ.step(-50);
                    Serial.println("Z stage performing -50 steps");
                    digitalWrite(ZSLP, LOW);
                    break;

                case '7':
                    digitalWrite(ZSLP,HIGH);
                    myStepperZ.step(100);
                    Serial.println("Z stage performing 100 steps");
                    digitalWrite(ZSLP, LOW);
                    break;
                case '8':
                    digitalWrite(ZSLP,HIGH);
                    myStepperZ.step(-100);
                    Serial.println("Z stage performing -100 steps");
                    digitalWrite(ZSLP, LOW);
                    break;
                    
                default:
                    vTaskDelay(50 / portTICK_PERIOD_MS); //small delay between brightness updates
                    break;
            }
        
        }
    vTaskDelay(50 / portTICK_PERIOD_MS); //small delay between brightness updates
    }
}


// ------------------ Y Stage Stepper function -------------- //

void stepY(void *parameters) {
    for (;;) {
 
    }
}

// ---------------- X Stage Stepper function ------------ //

void stepX(void *parameters) {
    for (;;) {
  
    }
}

// ---------------- Blue LED Control function ------------ //

void blueLed(void *parameters) {
    for (;;) {
       
    }
}

// ---------------- Lime LED Control function ------------ //

void limeLed(void *parameters) {
    for (;;) {
        
    }
}

void fanPWM(void *parameters) {
    for (;;) {
        
    }
}




// ---------------- Setup: Simply calls the above Functions ------------ //

void setup()
{
    // Ps3.attachOnConnect(onConnect);
    // Ps3.begin("C0:49:EF:D3:6C:D6");

    // Serial.println("Ready.");
    // Serial.print("Setting LEDs to player "); 
    // Serial.println(player, DEC);
    // Ps3.setPlayer(player);

    // player = 1;

    // pinMode(limeLedPin, OUTPUT);
    // pinMode(blueLedPin,OUTPUT);
    pinMode(fanCMDPin, OUTPUT);

    pinMode(ZA1A, OUTPUT);
    pinMode(ZA1A, OUTPUT);
    pinMode(ZA1A, OUTPUT);
    pinMode(ZA1A, OUTPUT);

    pinMode(ZSLP, OUTPUT);
    pinMode(ZULT, OUTPUT);

    
    // default SLP and ULT pins to low 
    digitalWrite(ZSLP,LOW);
    digitalWrite(ZULT, LOW);

    Serial.begin(115200); 
    myStepperZ.setSpeed(60); // set the speed of the stepper motors to 60 rpm
    myStepperX.setSpeed(60);
    myStepperY.setSpeed(60);

// ---------------- Function Calls ------------ //

    xTaskCreate(
        stepZ,
        "stepZ",
        2048,
        NULL,
        1,
        NULL
    );

    xTaskCreate(
        fanPWM,
        "fanPWM",
        2048,
        NULL,
        0,
        NULL
    );


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
    //     8000,
    //     NULL,
    //     1,
    //     NULL
    // );

    //     xTaskCreate(
    //     stepY,
    //     "stepY",
    //     1000,
    //     NULL,
    //     0,
    //     0
    // );

    //     xTaskCreate(
    //     stepX,
    //     "stepX",
    //     1000,
    //     NULL,
    //     1,
    //     0
    // );

}


// Loop Not used //
void loop(){

}