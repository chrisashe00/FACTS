#include <Arduino.h>
#include <Stepper.h>
#include <Ps3Controller.h>
 
// ---------------- Pin Assignment ------------ //

const int XA1A = 15; //X Stage Stepper Pins
const int XA1B = 2;
const int XB1A = 4;
const int XB1B = 5;
const int XSLP = 18;

const int YA1A = 33; //Y Stage Stepper Pins
const int YA1B = 32;
const int YB1A = 35;
const int YB1B = 34;
const int YSLP = 23;

const int ZA1A = 14; //Z Stage Stepper Pins
const int ZA1B = 27;
const int ZB1A = 26;
const int ZB1B = 25;
const int ZSLP = 33;

const int blueLedPin = 12; // Blue LED
const int limeLedPin = 13; // Lime LED

const int stepsPerRevZ = 200; // Z stage: 1.8 degree step angle
const int stepsPerRevXY = 20; // XY stage 18 degree step angle

int player = 0;


// ---------------- Stepper functions ------------ //

Stepper myStepperX(stepsPerRevXY,XA1A,XA1B,XB1A,XB1B); // X
Stepper myStepperY(stepsPerRevXY,YA1A,YA1B,YB1A,YB1B); // Y 
Stepper myStepperZ(stepsPerRevZ,ZA1A,ZA1B,ZB1A,ZB1B); // Z 


void limeLED(void *parameters){

}

// ------------------ Connect PS3 controller -------------- //
void onConnect(){
    Serial.println("Connected.");

         // Turn rumble on full intensity for 1 second


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
            myStepperZ.step(1);
            Serial.print("Stepping +1 step (UP)\n");
            digitalWrite(ZSLP, LOW);

            break;

            case '2': 

            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(-1);
            Serial.print("Stepping -1 step (DOWN) \n");
            digitalWrite(ZSLP, LOW);

            break;

            case '3': 

            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(10);
            Serial.print("Stepping 10 steps (UP) \n");
            digitalWrite(ZSLP, LOW);

            break;

            case '4': 

            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(- 10);
            Serial.print("Stepping -10 steps (DOWN) \n");
            digitalWrite(ZSLP, LOW);

            break;

            case '5': 

            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(50);
            Serial.print("Stepping 50 steps (UP) \n");
            digitalWrite(ZSLP, LOW);

            break;

            case '6': 

            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(- 50);
            Serial.print("Stepping -50 steps (DOWN) \n");
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

        if( Ps3.data.button.r1 ){
            Serial.println("Pressing the right bumper \n");

            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(5);
            Serial.print("Stepping Z +5 steps \n");
            digitalWrite(ZSLP,LOW);
        }
        
        if( Ps3.data.button.l1 ){
            Serial.println("Pressing the left bumper \n");
            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(-5);
            Serial.print("Stepping Z -5 steps \n");
            digitalWrite(ZSLP,LOW);
        }

        if( Ps3.data.button.triangle ){
            Serial.println("Pressing the triangle \n");
            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(+1);
            Serial.print("Stepping Z +1 steps \n");
            digitalWrite(ZSLP,LOW);
        }

        if( Ps3.data.button.cross ){
            Serial.println("Pressing the cross \n");
            digitalWrite(ZSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(-1);
            Serial.print("Stepping Z -1 steps \n");
            digitalWrite(ZSLP,LOW);
        }

        else{
            vTaskDelay(10 /portTICK_PERIOD_MS);
            taskYIELD();
        }
    }   
}


void stepX(void *paramaters){
    for (;;) {

        if( Ps3.data.button.circle ){
            Serial.println("Pressing the circle button");
            digitalWrite(XSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperX.step(20);
            Serial.print("Stepping X 20 steps \n");
            digitalWrite(XSLP,LOW);
        }
        
        if( Ps3.data.button.square ){
            Serial.println("Pressing the square button");
            digitalWrite(XSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperX.step(-20);
            Serial.print("Stepping X -20 steps \n");
            digitalWrite(XSLP,LOW);
        }

        else{
            vTaskDelay(10 /portTICK_PERIOD_MS);
            taskYIELD();
        }
    }   
}

void stepY(void *paramaters){
    for (;;) {

        if( Ps3.data.button.triangle ){
            Serial.println("Pressing the triangle button");
            digitalWrite(YSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(20);
            Serial.print("Stepping X 20 steps \n");
            digitalWrite(ZSLP,LOW);
        }
        
        if( Ps3.data.button.cross ){
            Serial.println("Pressing the cross button");
            digitalWrite(YSLP,HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(-20);
            Serial.print("Stepping Y -20 steps \n");
            digitalWrite(ZSLP,LOW);
        }

        else{
            vTaskDelay(10 /portTICK_PERIOD_MS);
            taskYIELD();
        }
    }   
}

void ledOnOff(void *parameters){
    for(;;){
        if( Ps3.data.button.up ){
            Serial.println("Pressing the up button");
            digitalWrite(limeLedPin,HIGH);
            digitalWrite(blueLedPin, HIGH);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(20);
            Serial.print("LED On \n");
        }
        
        if( Ps3.data.button.down ){
            Serial.println("Pressing the down button");
            digitalWrite(limeLedPin,LOW);
            digitalWrite(blueLedPin, LOW);
            vTaskDelay(10 / portTICK_PERIOD_MS);
            myStepperZ.step(-20);
            Serial.print("LED Off \n");
        }

        else{
            vTaskDelay(10 /portTICK_PERIOD_MS);
            taskYIELD();
        }        
    }
}

// Timer function //



void setup(){

    Ps3.attachOnConnect(onConnect);
    Ps3.begin("C0:49:EF:D3:6C:D6");

    Serial.println("Ready.");
    Serial.print("Setting LEDs to player "); 
    Serial.println(player, DEC);
    Ps3.setPlayer(player);

    player = 1;

    pinMode(limeLedPin, OUTPUT);
    pinMode(blueLedPin,OUTPUT);

    pinMode(ZA1A,OUTPUT);
    pinMode(ZA1B,OUTPUT);
    pinMode(ZB1A,OUTPUT);
    pinMode(ZB1B,OUTPUT);
    pinMode(ZSLP, OUTPUT);

    myStepperZ.setSpeed(30); // set the speed of the stepper motors
    myStepperX.setSpeed(30);
    myStepperY.setSpeed(30);

    Serial.begin(115200); 
    Serial.println("Hello I am ESP32 and I am running \n");


// ---------------- Create Tasks ------------ //

    // xTaskCreate(
    //     stepZ,
    //     "stepZ",
    //     2048,
    //     NULL,
    //     1,
    //     NULL
    // );

    // xTaskCreate(
    //     stepX,
    //     "stepX",
    //     2048,
    //     NULL,
    //     1,
    //     NULL
    // );

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
}


void loop(){}