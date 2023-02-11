#include <Arduino.h>
#include <Stepper.h>


const int stepsPerRevolution = 200; // change this to match the number of steps per revolution for your motor
const float stepAngle = 1.8; // NEMA 11 step angle in degrees
const float stepRad = stepAngle * (3.141 / 180); // step angle in radians 

Stepper myStepper(stepsPerRevolution, 14, 27, 26, 25); // initialize the stepper library with the number of steps per revolution and the pin numbers

int ZPosition = 0;  //initial positions
int YPosition = 0;
int XPosition = 0; 
float Revs = 4; //Enter number of revs here
float linDisp = 4 * stepsPerRevolution * 0.0314 * 2.5; //Rotational to Linear Displacement

int count1 = 0;


void task1(void * parameters)
{
    for(;;)
    {
        if (Serial.available())
        {

            char received1 = Serial.read();
            if (received1 == 'd')
            {
                Serial.println("Displacing -Z");
        
                ZPosition = ZPosition - Revs;
        

                Serial.print("\n");
                Serial.print("Z position:   ");
                Serial.print(ZPosition);
                Serial.println("mm");
        

                myStepper.step(- 4 * stepsPerRevolution); // rotate the stepper motor by a quarter turn in the counterclockwise direction
            }

            else if (received1 == 'u')
            {
                Serial.println("Displacing +Z");

                ZPosition = ZPosition + Revs ;


                Serial.print("\n");
                Serial.print("Z Position:  ");
                Serial.print(ZPosition);
                Serial.println("mm");

                myStepper.step(4 * stepsPerRevolution); // rotate the stepper motor by a quarter turn in the clockwise direction
            }
        }
    }
}


void setup()
{
    Serial.begin(115200); // initialize serial communication
    myStepper.setSpeed(60); // set the speed of the stepper motor

    xTaskCreate(
        task1,
        "task1",
        1000,
        NULL,
        1,
        NULL
    );
}


void loop()
{
    if (Serial.available())
    {
        char received1 = Serial.read();
        if (received1 == 'd')
        {
            Serial.println("Displacing -Z");
            
            ZPosition = ZPosition - Revs;
            

            Serial.print("\n");
            Serial.print("Z position:   ");
            Serial.print(ZPosition);
            Serial.println("mm");
            

            myStepper.step(- 4 * stepsPerRevolution); // rotate the stepper motor by a quarter turn in the counterclockwise direction
        }
        else if (received1 == 'u')
        {
            Serial.println("Displacing +Z");

            ZPosition = ZPosition + Revs ;


            Serial.print("\n");
            Serial.print("Z Position:  ");
            Serial.print(ZPosition);
            Serial.println("mm");

            myStepper.step(4 * stepsPerRevolution); // rotate the stepper motor by a quarter turn in the clockwise direction
        }

    }

    if (Serial.available() > 0) {
        String input = Serial.readString();
        if (input.equals("r")) {

            ZPosition = 0;

            Serial.println("Z Position set to 0 mm.");
        }
    }



}




