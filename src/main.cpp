#include <Arduino.h>
#include <Stepper.h>

const int stepsPerRevolution = 200; // change this to match the number of steps per revolution for your motor

const float stepAngle = 1.8; // NEMA 11 step angle in degrees
const float stepRad = stepAngle * (3.141 / 180); // step angle in radians 


const int BLUE_LED_PIN = 12; // change this to match the pin you've connected the LED to
int brightness = 128; // starting brightness for the LED

// pins 33,32,35,34 give error? 
Stepper myStepperz(stepsPerRevolution,1,2,3,4); // initialize the stepper library with the number of steps per revolution and the pin numbers
Stepper myStepperx(stepsPerRevolution,15,2,4,5);
Stepper mySteppery(stepsPerRevolution,14,27,26,25);

int ZPosition = 0;  //initial positions
int YPosition = 0;
int XPosition = 0;
int ledPin = 12; 


float Revs = 0.4; //Enter number of revs here
float linDispScrew = tan(0.5236) * 0.5 * 2 * 3.14159;

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
        // vTaskDelay(1000 / portTICK_PERIOD_MS);
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
        

                mySteppery.step(- Revs * stepsPerRevolution); // rotate the stepper motor by a quarter turn in the counterclockwise direction
            }

            else if (receivedy == 'b')
            {
                Serial.println("Displacing +Y");

                YPosition = YPosition + linDispScrew ;

                Serial.print("\n");
                Serial.print("Y Position:  ");
                Serial.print(YPosition);
                Serial.println("mm");

                mySteppery.step(Revs * stepsPerRevolution); // rotate the stepper motor by a quarter turn in the clockwise direction
            }
        
            else if (receivedy == 'c')
            {
                Serial.println("Displacing -X (left)");
        
                XPosition = XPosition - linDispScrew;
        

                Serial.print("\n");
                Serial.print("X position:   ");
                Serial.print(XPosition);
                Serial.println("mm");
        

                myStepperx.step(- Revs *stepsPerRevolution); // rotate the stepper motor by a quarter turn in the counterclockwise direction
            }

            else if (receivedy == 'x')
            {
                Serial.println("Displacing +X (right)");

                XPosition = XPosition + linDispScrew ;

                Serial.print("\n");
                Serial.print("X Position:  ");
                Serial.print(XPosition);
                Serial.println("mm");

                myStepperx.step(Revs * stepsPerRevolution); // rotate the stepper motor by a quarter turn in the clockwise direction
            }
        

            else if (receivedy == 'r')
            { 
                YPosition = 0;
                XPosition = 0;

                Serial.println("X Position set to 0 mm");
                Serial.println("Y Position set to 0 mm");
            }


        }

        // Print the stack high water mark for task1
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        // Serial.print("delaying input: ");
        // Serial.println(uxTaskGetStackHighWaterMark(NULL));
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
        

                myStepperx.step(- Revs *stepsPerRevolution); // rotate the stepper motor by a quarter turn in the counterclockwise direction
            }

            else if (receivedx == 'x')
            {
                Serial.println("Displacing +X (right)");

                XPosition = XPosition + linDispScrew ;

                Serial.print("\n");
                Serial.print("X Position:  ");
                Serial.print(XPosition);
                Serial.println("mm");

                myStepperx.step(Revs * stepsPerRevolution); // rotate the stepper motor by a quarter turn in the clockwise direction
            }
        

            else if (receivedx == 'r')
            { 
                YPosition = 0;

                Serial.println("X Position set to 0 mm.");
            }
        }
            
        // Print the stack high water mark for task1
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        // Serial.print("Delaying Inputs");
        // Serial.println(uxTaskGetStackHighWaterMark(NULL));
    }
}

void blueLED(void * parameters)
{
  for(;;)
  {
     if (Serial.available()) {
    char input = Serial.read();
    if (input == '8') {
      brightness = max(0, brightness - 32); // decrease brightness by 32 (out of 255)
      analogWrite(BLUE_LED_PIN, brightness);
      Serial.print("\n");
      Serial.print("Current Brightness: ");
      Serial.print(brightness);
      Serial.print('\n');
    } 
    
    else if (input == '9') {
      brightness = min(255, brightness + 32); // increase brightness by 32 (out of 255)
      analogWrite(BLUE_LED_PIN, brightness);
      Serial.print("\n");
      Serial.print("Current Brightness: ");
      Serial.print(brightness);
      Serial.print('\n');
    }
  }

  // vTaskDelay(1000/portTICK_PERIOD_MS);
  // Serial.print("LED stack high water mark: ");
  // Serial.println(uxTaskGetStackHighWaterMark(NULL));

  }

}

void setup()
{
    pinMode(BLUE_LED_PIN, OUTPUT);
    Serial.begin(115200); // initialize serial communication
    myStepperz.setSpeed(60); // set the speed of the stepper motor
    myStepperx.setSpeed(20);
    mySteppery.setSpeed(20);


    // xTaskCreate(
    //     stepz,
    //     "stepz",
    //     5000,
    //     NULL,
    //     1,
    //     NULL
    // );

    //     xTaskCreate(
    //     blueLED,
    //     "blueLED",
    //     10000,
    //     NULL,
    //     1,
    //     NULL
    // );

    //     xTaskCreate(
    //     stepy,
    //     "stepy",
    //     8000,
    //     NULL,
    //     1,
    //     NULL
    // );

        xTaskCreate(
        stepx,
        "stepx",
        8000,
        NULL,
        1,
        NULL
    );

}

void loop(){}
