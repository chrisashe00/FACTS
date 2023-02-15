#include <Arduino.h>
#include <Stepper.h>

const int stepsPerRevolution = 200; // change this to match the number of steps per revolution for your motor
const int stepsPerRevolutionx = 200;
const int stepsPerRevolutiony = 200;
const float stepAngle = 1.8; // NEMA 11 step angle in degrees
const float stepRad = stepAngle * (3.141 / 180); // step angle in radians 

Stepper myStepperz(stepsPerRevolution, 1,2,3,4); // initialize the stepper library with the number of steps per revolution and the pin numbers
Stepper myStepperx(stepsPerRevolutionx,14,27,26,25);
Stepper mySteppery(stepsPerRevolutiony,33,32,35,34);

int ZPosition = 0;  //initial positions
int YPosition = 0;
int XPosition = 0; 
float Revs = 0.5; //Enter number of revs here
float linDispScrew = ( 3.141 * 2.84 * Revs ) / 0.5;

void stepz(void * parameters)
{
    for(;;)
    {
        if (Serial.available())
        {

            char received1 = Serial.read();
            if (received1 == 'd')
            {
                Serial.println("Displacing -Z");
        
                ZPosition = ZPosition - linDispScrew;
        

                Serial.print("\n");
                Serial.print("Z position:   ");
                Serial.print(ZPosition);
                Serial.println("mm");
        

                myStepperz.step(- Revs * stepsPerRevolution); // rotate the stepper motor by a quarter turn in the counterclockwise direction
            }

            else if (received1 == 'u')
            {
                Serial.println("Displacing +Z");

                ZPosition = ZPosition + linDispScrew ;

                Serial.print("\n");
                Serial.print("Z Position:  ");
                Serial.print(ZPosition);
                Serial.println("mm");

                myStepperz.step(Revs * stepsPerRevolution); // rotate the stepper motor by a quarter turn in the clockwise direction
            }
        

            else if (received1 == 'r')
            { 
                ZPosition = 0;

                Serial.println("Z Position set to 0 mm.");
            }
        }
            
        // Print the stack high water mark for task1
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        // Serial.print("stepz stack high water mark: ");
        // Serial.println(uxTaskGetStackHighWaterMark(NULL));
    }
}


void stepy(void * parameters)
{
    for(;;)
    {
        if (Serial.available())
        {

            char receivedy = Serial.read();
            if (receivedy == 'v')
            {
                Serial.println("Displacing -Y");
        
                YPosition = YPosition - linDispScrew;
        

                Serial.print("\n");
                Serial.print("Y position:   ");
                Serial.print(ZPosition);
                Serial.println("mm");
        

                mySteppery.step(- stepsPerRevolution); // rotate the stepper motor by a quarter turn in the counterclockwise direction
            }

            else if (receivedy == 'b')
            {
                Serial.println("Displacing +Y");

                YPosition = YPosition + linDispScrew ;

                Serial.print("\n");
                Serial.print("Y Position:  ");
                Serial.print(YPosition);
                Serial.println("mm");

                mySteppery.step(stepsPerRevolution); // rotate the stepper motor by a quarter turn in the clockwise direction
            }
        

            else if (receivedy == 'r')
            { 
                YPosition = 0;

                Serial.println("Y Position set to 0 mm.");
            }
        }
            
        // Print the stack high water mark for task1
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        Serial.print("stepy stack high water mark: ");
        Serial.println(uxTaskGetStackHighWaterMark(NULL));
    }
}

void stepx(void * parameters)
{
    for(;;)
    {
        if (Serial.available())
        {

            char receivedx = Serial.read();
            if (receivedx == 'c')
            {
                Serial.println("Displacing -X (left)");
        
                XPosition = XPosition - linDispScrew;
        

                Serial.print("\n");
                Serial.print("X position:   ");
                Serial.print(XPosition);
                Serial.println("mm");
        

                myStepperx.step(stepsPerRevolution); // rotate the stepper motor by a quarter turn in the counterclockwise direction
            }

            else if (receivedx == 'x')
            {
                Serial.println("Displacing +X (right)");

                XPosition = XPosition + linDispScrew ;

                Serial.print("\n");
                Serial.print("X Position:  ");
                Serial.print(XPosition);
                Serial.println("mm");

                myStepperx.step(stepsPerRevolution); // rotate the stepper motor by a quarter turn in the clockwise direction
            }
        

            else if (receivedx == 'r')
            { 
                YPosition = 0;

                Serial.println("X Position set to 0 mm.");
            }
        }
            
        // Print the stack high water mark for task1
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        Serial.print("stepx stack high water mark: ");
        Serial.println(uxTaskGetStackHighWaterMark(NULL));
    }
}


void setup()
{
        // Set the pin mode for the pins to be output
    pinMode(14, OUTPUT);
    pinMode(27, OUTPUT);
    pinMode(26, OUTPUT);
    pinMode(25, OUTPUT);
    pinMode(33, OUTPUT);
    pinMode(32, OUTPUT);
    pinMode(35, OUTPUT);
    pinMode(34, OUTPUT);

    Serial.begin(115200); // initialize serial communication
    myStepperz.setSpeed(60); // set the speed of the stepper motor
    myStepperx.setSpeed(60);
    mySteppery.setSpeed(60);


    // xTaskCreate(
    //     stepz,
    //     "stepz",
    //     5000,
    //     NULL,
    //     1,
    //     NULL
    // );

        xTaskCreate(
        stepy,
        "stepy",
        6000,
        NULL,
        2,
        NULL
    );

        xTaskCreate(
        stepx,
        "stepx",
        6000,
        NULL,
        1,
        NULL
    );

}


void loop(){}
