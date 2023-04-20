// Code Written by Christopher Ashe in Academic year 2022/2023 for MENG Project
// University of Strathclyde
// These headers must be included, you can find them on the platformIO home

#include <Arduino.h>
#include <Stepper.h>
#include <Ps3Controller.h>
#include <AccelStepper.h>
 
// ---------------- Pin Assignment ------------ //
const int XA1A = 32; //X Stage Stepper Pins
const int XA1B = 18;
const int XB1A = 19;
const int XB1B = 15;
const int XSLP = 4;

const int ZA1A = 14; //Z Stage Stepper Pins
const int ZA1B = 27;
const int ZB1A = 26;
const int ZB1B = 25;
const int ZSLP = 33;

const int YA1A = 5; //Y Stage Stepper Pins
const int YA1B = 21;
const int YB1A = 22;
const int YB1B = 23;

const int blueLedPin = 12; // Blue LED
const int limeLedPin = 13; // Lime LED

const int stepsPerRevZ = 200; // Z stage: 1.8 degree step angle
const int stepsPerRevXY = 20; // XY stage 18 degree step angle

int player = 0;

bool ps3Connected = false;
bool zLock = false;
bool xLock = false;
bool yLock = false;
bool ledLock = false;

int blueBrightness = 60; // starting brightness for blue LED
int limeBrightness = 60; // starting brightness for lime LED

// ---------------- Stepper functions ------------ //
Stepper myStepperX(stepsPerRevXY,XA1A,XA1B,XB1A,XB1B); // X
Stepper myStepperY(stepsPerRevXY,YA1A,YA1B,YB1A,YB1B); // Y 
Stepper myStepperZ(stepsPerRevZ,ZA1A,ZA1B,ZB1A,ZB1B); // Z 

// Initialize the stepper with your chosen pins and settings
AccelStepper myStepperAccelZ(AccelStepper::FULL4WIRE, ZA1A, ZA1B, ZB1A, ZB1B);


// ------------------ Connect PS3 controller -------------- //
void onConnect(){
    Serial.println("Connected.");
}

void reconnectController(void *parameters) {
    for(;;){
        if (Ps3.isConnected()){
            Serial.print("PS3 Connectivity is: ");
            Serial.println(Ps3.isConnected());
            vTaskDelay(10000 / portTICK_PERIOD_MS);
            taskYIELD();
        }

        else if (!Ps3.isConnected()){    
            Ps3.attachOnConnect(onConnect);
            Ps3.begin("C0:49:EF:D3:6C:D6");
            Serial.print("PS3 Connectivity is: ");
            Serial.println(Ps3.isConnected());
            Serial.println("Ready.");
            Serial.print("Setting LEDs to player "); 
            Serial.println(player, DEC);
            Ps3.setPlayer(player);

            player = 1;
            ps3Connected = true; 

            vTaskDelay(1000 / portTICK_PERIOD_MS);
            }

        else{
            vTaskDelay(10 / portTICK_PERIOD_MS);
            taskYIELD();
        }
    }


}

// ------------------ Z Stage Stepper function -------------- //
void stepZ(void *parameters){
    for (;;) {

        if (Serial.available()){
            char receivedZ = Serial.read();

            switch(receivedZ){

            case '1': 

            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            Serial.print("case 1\n");
            myStepperZ.step(1);
            while (myStepperAccelZ.isRunning()) {
                // Wait until the stepper has finished moving
                vTaskDelay(1 / portTICK_PERIOD_MS);
            }
            Serial.println("complete\n");
            digitalWrite(ZSLP, LOW);

            break;

            case '2': 

            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            Serial.print("case 2\n");
            myStepperZ.step(-1);
            while (myStepperAccelZ.isRunning()) {
                // Wait until the stepper has finished moving
                vTaskDelay(1 / portTICK_PERIOD_MS);
            }
            Serial.println("complete\n");
            digitalWrite(ZSLP, LOW);

            break;

            case '3': 

            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            Serial.print("case 3\n");
            myStepperZ.step(10);
            while (myStepperAccelZ.isRunning()) {
                // Wait until the stepper has finished moving
                vTaskDelay(1 / portTICK_PERIOD_MS);
            }
            Serial.println("complete\n");
            digitalWrite(ZSLP, LOW);

            break;

            case '4': 

            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            Serial.println("case 4\n");
            myStepperZ.step(- 10);
            while (myStepperAccelZ.isRunning()) {
                // Wait until the stepper has finished moving
                vTaskDelay(1 / portTICK_PERIOD_MS);
            }
            Serial.print("complete\n");
            digitalWrite(ZSLP, LOW);

            break;

            case '5': 

            digitalWrite(ZSLP,HIGH);
            Serial.print("case 5\n");
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(50);
            while (myStepperAccelZ.isRunning()) {
                // Wait until the stepper has finished moving
                vTaskDelay(1 / portTICK_PERIOD_MS);
            }
            Serial.println("complete\n");
            digitalWrite(ZSLP, LOW);

            break;

            case '6': 

            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            Serial.print("case 6\n");
            myStepperZ.step(- 50);
            Serial.println("complete\n");
            digitalWrite(ZSLP, LOW);

            break;

            default:

            vTaskDelay(10 / portTICK_PERIOD_MS);
            taskYIELD();

            break;
            }
  
        }
            else{
                vTaskDelay(10 / portTICK_PERIOD_MS);
                taskYIELD();
                
            }
    }
}

void stepZPs3(void *paramaters){
    for (;;) {
            if( Ps3.data.button.r1 && zLock == false){
                zLock = true;
                Serial.println("Pressing right bumper\n");
                digitalWrite(ZSLP,HIGH);
                vTaskDelay(10 / portTICK_PERIOD_MS);
                myStepperZ.step(10);
                Serial.print("Stepping Z +10 steps \n");
                digitalWrite(ZSLP,LOW);

            }


            if( Ps3.data.button.l1 && zLock == false){
                zLock = true;
                Serial.println("Pressing the left bumper \n");
                digitalWrite(ZSLP,HIGH);
                vTaskDelay(50 / portTICK_PERIOD_MS);
                myStepperZ.step(-10);
                Serial.print("Stepping Z -10 steps \n");
                digitalWrite(ZSLP,LOW);

            }

            if( Ps3.data.button.triangle && zLock == false ){
                zLock = true;
                Serial.println("Pressing the triangle \n");
                myStepperZ.setSpeed(10); // set the speed of the stepper motors
                digitalWrite(ZSLP,HIGH);
                vTaskDelay(10 / portTICK_PERIOD_MS);
                myStepperZ.step(+1);
                Serial.print("Stepping Z +1 step \n");
                digitalWrite(ZSLP,LOW);
                myStepperZ.setSpeed(60); // set the speed of the stepper motors

            }

            if( Ps3.data.button.cross && zLock == false ){
                zLock = true;
                Serial.println("Pressing the cross \n");
                myStepperZ.setSpeed(10); // set the speed of the stepper motors
                digitalWrite(ZSLP,HIGH);
                vTaskDelay(10 / portTICK_PERIOD_MS);
                myStepperZ.step(-1);
                Serial.print("Stepping Z -1 step \n");
                digitalWrite(ZSLP,LOW);
                myStepperZ.setSpeed(60); // set the speed of the stepper motors
            }

            if( Ps3.data.button.l2 && zLock == false){
                zLock = true;
                Serial.println("Pressing the left trigger \n");
                digitalWrite(ZSLP,HIGH);
                vTaskDelay(10 / portTICK_PERIOD_MS);
                myStepperZ.step(-100);
                Serial.print("Stepping Z -100 steps\n");
                vTaskDelay(10/ portTICK_PERIOD_MS);
                digitalWrite(ZSLP,LOW);

            }

            if( Ps3.data.button.r2 && zLock == false){
                zLock = true;
                Serial.println("Pressing the right bumper \n");
                digitalWrite(ZSLP,HIGH);
                vTaskDelay(10 / portTICK_PERIOD_MS);
                myStepperZ.step(100);
                Serial.print("Stepping Z +100 steps\n");
                vTaskDelay(10 / portTICK_PERIOD_MS);
                digitalWrite(ZSLP,LOW);

            }

            if( Ps3.data.button.r1 && zLock == false){
                zLock = true;
                Serial.println("Pressing right bumper\n");
                digitalWrite(ZSLP,HIGH);
                vTaskDelay(10 / portTICK_PERIOD_MS);
                myStepperZ.step(10);
                Serial.print("Stepping Z +10 steps \n");
                vTaskDelay(1000 / portTICK_PERIOD_MS);
                digitalWrite(ZSLP,LOW);


            }

            if( Ps3.data.button.start && zLock == false){
                zLock = true;
                Serial.println("Pressing the left bumper \n");
                digitalWrite(ZSLP,HIGH);
                vTaskDelay(50 / portTICK_PERIOD_MS);
                myStepperZ.step(+5 * stepsPerRevZ);
                Serial.print("Stepping Z +5 \n");
                digitalWrite(ZSLP,LOW);
            }

            if( Ps3.data.button.select && zLock == false){
                zLock = true;
                Serial.println("Pressing the select \n");
                digitalWrite(ZSLP,HIGH);
                vTaskDelay(50 / portTICK_PERIOD_MS);
                myStepperZ.step(-5 * stepsPerRevZ);
                Serial.print("Stepping Z -5 revs\n");
                digitalWrite(ZSLP,LOW);

            }

            else{
                vTaskDelay(100 /portTICK_PERIOD_MS);
                // Serial.print("ZSLP is: ");
                // Serial.print(digitalRead(ZSLP));
                taskYIELD();
                zLock = false;
            }
        }
    }   

void stepX(void *paramaters){
    for (;;) {
        if( Ps3.data.button.circle && xLock == false ){
            xLock = true;
            Serial.println("Pressing the circle button");
            digitalWrite(ZSLP, LOW);
            digitalWrite(ZA1A, LOW);
            digitalWrite(ZA1B, LOW);
            digitalWrite(ZB1A, LOW);
            digitalWrite(ZB1B, LOW);
            digitalWrite(XSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            digitalWrite(XSLP,HIGH);
            myStepperX.step(25);
            Serial.print("Stepping X 200 steps \n");
            digitalWrite(XSLP,LOW);
            int switchState = digitalRead(XSLP);
            Serial.print("XSLP pin: ");
            Serial.println(switchState);
        }
        
        if( Ps3.data.button.square && xLock == false ){
            xLock = true;
            Serial.println("Pressing the square button");
            digitalWrite(ZSLP, LOW);
            digitalWrite(ZA1A, LOW);
            digitalWrite(ZA1B, LOW);
            digitalWrite(ZB1A, LOW);
            digitalWrite(ZB1B, LOW);
            digitalWrite(XSLP,HIGH);

            vTaskDelay(10 / portTICK_PERIOD_MS);
            digitalWrite(XSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperX.step(-25);
            Serial.print("Stepping X -10 steps \n");
            digitalWrite(XSLP,LOW);
            int switchState = digitalRead(XSLP);
            Serial.print("XSLP pin: ");
            Serial.println(switchState);
        }

        else{
            xLock = false;
            vTaskDelay(500 /portTICK_PERIOD_MS);
            taskYIELD();
        }
    }   
}

void stepY(void *paramaters){
    for (;;) {
        if( Ps3.data.button.circle && yLock == false ){
            yLock = true;
            Serial.println("Pressing the circle button");
            digitalWrite(ZSLP, LOW);
            digitalWrite(ZA1A, LOW);
            digitalWrite(ZA1B, LOW);
            digitalWrite(ZB1A, LOW);
            digitalWrite(ZB1B, LOW);
            digitalWrite(XSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            digitalWrite(XSLP,HIGH);
            myStepperY.step(100);
            Serial.print("Stepping Y 100 steps \n");
            digitalWrite(XSLP,LOW);
            int switchState = digitalRead(XSLP);
            Serial.print("XSLP pin: ");
            Serial.println(switchState);
        }
        
        if( Ps3.data.button.square && yLock == false ){
            yLock = true;
            Serial.println("Pressing the square button");
            digitalWrite(ZSLP, LOW);
            digitalWrite(ZA1A, LOW);
            digitalWrite(ZA1B, LOW);
            digitalWrite(ZB1A, LOW);
            digitalWrite(ZB1B, LOW);
            digitalWrite(XSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            digitalWrite(XSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperY.step(-100);
            Serial.print("Stepping Y -100 steps \n");
            digitalWrite(XSLP,LOW);
            int switchState = digitalRead(XSLP);
            Serial.print("XSLP pin: ");
            Serial.println(switchState);
        }

        else{
            yLock = false;

            vTaskDelay(2000 /portTICK_PERIOD_MS);
            taskYIELD();
        }
    }   
}

void ledOnOff(void *parameters){
    for(;;){
        if( Ps3.data.button.down && ledLock == false){
            ledLock = true;
            Serial.println("Pressing the down button");
            blueBrightness = min(blueBrightness + 10, 255); // increment blue brightness by 10 PWM increments, up to a maximum of 255
            analogWrite(blueLedPin, blueBrightness);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            Serial.print("Blue LED brightness: ");
            Serial.println(blueBrightness);
        }

        if( Ps3.data.button.left && ledLock == false ){
            ledLock = true;
            Serial.println("Pressing the left button");
            limeBrightness = min(limeBrightness + 10, 255); // increment lime brightness by 10 PWM increments, up to a maximum of 255
            analogWrite(limeLedPin, limeBrightness);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            Serial.print("Lime LED brightness: ");
            Serial.println(limeBrightness);
        }

        if( Ps3.data.button.up && ledLock == false){
            ledLock = true;
            Serial.println("Pressing the up button");
            blueBrightness = max(blueBrightness - 10, 0); // decrement blue brightness by 10 PWM increments, down to a minimum of 0
            analogWrite(blueLedPin, blueBrightness);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            Serial.print("Blue LED brightness: ");
            Serial.println(blueBrightness);
        }

        if( Ps3.data.button.right && ledLock == false ){
            ledLock = true;
            Serial.println("Pressing the right button");
            limeBrightness = max(limeBrightness - 10, 0); // decrement lime brightness by 10 PWM increments, down to a minimum of 0
            analogWrite(limeLedPin, limeBrightness);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            Serial.print("Lime LED brightness: ");
            Serial.println(limeBrightness);
        }

        else{
            ledLock = false;
            vTaskDelay(10 /portTICK_PERIOD_MS);
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

    pinMode(XA1A,OUTPUT);
    pinMode(XA1B,OUTPUT);
    pinMode(XB1A,OUTPUT);
    pinMode(XB1B,OUTPUT);
    pinMode(XSLP, OUTPUT);

    digitalWrite(XSLP,LOW);

    myStepperZ.setSpeed(80); // set the speed of the stepper motors
    myStepperX.setSpeed(70);
    // myStepperY.setSpeed(70);

    Serial.begin(115200); 
    Serial.println("Hello I am ESP32 and I am running \n");


// ---------------- Create Tasks ------------ //

    xTaskCreate(
        stepZ,
        "stepZ",
        2048,
        NULL,
        1,
        NULL
    );

    xTaskCreate(
        stepX,
        "stepX",
        2048,
        NULL,
        1,
        NULL
    );

    // xTaskCreate(
    //     stepY,
    //     "stepY",
    //     2048,
    //     NULL,
    //     1,
    //     NULL
    // );

    xTaskCreate(
        ledOnOff,
        "ledOnOff",
        1000,
        NULL,
        1,
        NULL
    );

    xTaskCreate(
        stepZPs3,
        "stepZPs3",
        2048,
        NULL,
        1,
        NULL
    );

    xTaskCreatePinnedToCore(
        reconnectController,      // Task function
        "reconnectController",       // Task name
        4096,              // Stack size
        NULL,              // Task parameters
        1,                 // Task priority
        NULL,      // Task handle
        0                  // Core ID (0 or 1)
    );
}

void loop(){}