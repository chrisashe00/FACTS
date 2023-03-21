#include <Arduino.h>

void setup(){
    Serial.begin(115200);

    while(!Serial){;}
}

const char TERMINATOR = '|';

void loop(){
    if (Serial.available()>0){

        String commandFromJetson = Serial.readStringUntil(TERMINATOR);

        String ackMsg = "Hello Jetson Nano! This is what I got from you: " + commandFromJetson;

        Serial.print(ackMsg);
    }
    delay(500);
    }
