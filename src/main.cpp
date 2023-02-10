#include <Arduino.h>
#include <Stepper.h>
#include <AccelStepper.h>

// Steps per revolution for NEMA 11
const int STEPS_PER_REV = 200;

//Defining Motor Pins and number of wires required 

#define A1A 13
#define A1B 12
#define B1A 14
#define B1B 27

// number of motor wires 
#define MOTORWIRES 4

AccelStepper zStage(MOTORWIRES , A1A , A1B, B1A, B1B)

void setup(){

}

void loop(){
    
}