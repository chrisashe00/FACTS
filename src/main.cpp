#include <Arduino.h>
#include <Stepper.h>

const int stepsPerRevolution = 200; // steps per rev for our motors
const float stepAngle = 1.8; // our motor's step angle in degrees
const float stepRad = stepAngle * (3.141 / 180); // step angle in radians 

int blue_brightness = 0; // starting brightness for the blue LED
int lime_brightness = 0; // starting brightness for the lime LED

int fadeAmount = 17; // How much to change the brightness each step when fading
bool isFading = false; // Whether the LED is currently fading


// -----pins 33,32,35,34 give error-----
Stepper myStepperz(stepsPerRevolution,1,2,3,4); // Z stepper and pins 
Stepper myStepperx(stepsPerRevolution,5,18,19,21); // X stepper and pins 
Stepper mySteppery(stepsPerRevolution,14,27,26,25); // Y stepper and pins 

const int BLUE_LED_PIN = 12; // Blue LED pin assignment
const int LIME_LED_PIN = 13; // Lime LED pin assignment

int ZPosition = 0;  //initialise positions
int YPosition = 0;
int XPosition = 0;

float Revs = 1; //Enter number of revs here

// Screw Equation,gives linear displacement of Z stage, tan(helix angle) * Thread Pitch * 2 * pi ... *M3 screw
float linDispScrew = tan(0.5236) * 0.5 * 2 * 3.14159; 

//Z stage step function
void stepz(void * parameters)
{
    for(;;)
    {
        if (Serial.available())
        //read the character received and perform operations if it matches what the code wants
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
        
            //Reset the gauge displacement if char received is an r
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
        

                mySteppery.step(- Revs * stepsPerRevolution); 
            }

            else if (receivedy == 'b')
            {
                Serial.println("Displacing +Y");

                YPosition = YPosition + linDispScrew ;

                Serial.print("\n");
                Serial.print("Y Position:  ");
                Serial.print(YPosition);
                Serial.println("mm");

                mySteppery.step(Revs * stepsPerRevolution); 
            }
        
            else if (receivedy == 'c')
            {
                Serial.println("Displacing -X (left)");
        
                XPosition = XPosition - linDispScrew;
        

                Serial.print("\n");
                Serial.print("X position:   ");
                Serial.print(XPosition);
                Serial.println("mm");
        

                myStepperx.step(- Revs *stepsPerRevolution); 
            }

            else if (receivedy == 'x')
            {
                Serial.println("Displacing +X (right)");

                XPosition = XPosition + linDispScrew ;

                Serial.print("\n");
                Serial.print("X Position:  ");
                Serial.print(XPosition);
                Serial.println("mm");

                myStepperx.step(Revs * stepsPerRevolution);
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
        // vTaskDelay(1000 / portTICK_PERIOD_MS);
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
    char blue_input = Serial.read();
    if (blue_input == '9') {
      blue_brightness = max(0, blue_brightness - 32); // decrease brightness by 32 (out of 255)
      analogWrite(BLUE_LED_PIN, blue_brightness);
      Serial.print("\n");
      Serial.print("Current BLUE Brightness: ");
      Serial.print(blue_brightness);
      Serial.print('\n');
    } 
    
    else if (blue_input == '8') {
      blue_brightness = min(255, blue_brightness + 32); // increase brightness by 32 (out of 255)
      analogWrite(BLUE_LED_PIN, blue_brightness);
      Serial.print("\n");
      Serial.print("Current BLUE Brightness: ");
      Serial.print(blue_brightness);
      Serial.print('\n');
    }

    else if (blue_input == 'f') {
      // Toggle fading on or off
      isFading = !isFading;
      if (isFading) {
        Serial.println("Fading started");
      } else {
        Serial.println("Fading stopped");
      }
    }
    }

    if (isFading) {
    blue_brightness += fadeAmount;
    if (blue_brightness <= 0 || blue_brightness >= 255) {
      // Reverse the fade direction when the brightness reaches the min or max value
      fadeAmount = -fadeAmount;
    }
    analogWrite(BLUE_LED_PIN, blue_brightness);
    vTaskDelay(50/portTICK_PERIOD_MS);
    }

    else{
            blue_brightness = 255;
        }
  }
  vTaskDelay(50/portTICK_PERIOD_MS);

  }

void limeLED(void * parameters)
{
  for(;;)
  {
     if (Serial.available()) {
    char lime_input = Serial.read();
    if (lime_input == '7') {
      lime_brightness = max(0, lime_brightness - 32); // decrease brightness by 32 (out of 255)
      analogWrite(LIME_LED_PIN, lime_brightness);
      Serial.print("\n");
      Serial.print("Current LIME Brightness: ");
      Serial.print(lime_brightness);
      Serial.print('\n');
    } 
    
    else if (lime_input == '6') {
      lime_brightness = min(255, lime_brightness + 32); // increase brightness by 32 (out of 255)
      analogWrite(LIME_LED_PIN, lime_brightness);
      Serial.print("\n");
      Serial.print("Current LIME Brightness: ");
      Serial.print(lime_brightness);
      Serial.print('\n');
    }

    else if (lime_input == 'f') 
    {
      // Toggle fading on or off
      isFading = !isFading;
      if (isFading) 
      {
        Serial.println("Fading started");
      } 
      
      else 
      {
        Serial.println("Fading stopped");
      }

    }

    }
        if (isFading) {
            lime_brightness += fadeAmount;
            if (lime_brightness <= 0 || lime_brightness >= 255) 
            {
                // Reverse the fade direction when the brightness reaches the min or max value
                fadeAmount = -fadeAmount;
            }
            analogWrite(LIME_LED_PIN, lime_brightness);
            vTaskDelay(50/portTICK_PERIOD_MS);
        }
    

       vTaskDelay(500/portTICK_PERIOD_MS);
  // Serial.print("LED stack high water mark: ");
  // Serial.println(uxTaskGetStackHighWaterMark(NULL));
  }
}

void setup()
{
    pinMode(BLUE_LED_PIN, OUTPUT);
    pinMode(LIME_LED_PIN,OUTPUT);
    Serial.begin(115200); 
    myStepperz.setSpeed(60); // set the speed of the stepper motors
    myStepperx.setSpeed(60);
    mySteppery.setSpeed(60);

    //functions are below, you can comment them out if you don't wanna call them 

    xTaskCreate(
        stepz,
        "stepz",
        5000,
        NULL,
        1,
        1
    );

    //     xTaskCreate(
    //     blueLED,
    //     "blueLED",
    //     1000,
    //     NULL,
    //     1,
    //     0
    // );

        xTaskCreate(
        limeLED,
        "limeLED",
        1000,
        NULL,
        1,
        0
    );

    //     xTaskCreate(
    //     stepy,
    //     "stepy",
    //     8000,
    //     NULL,
    //     1,
    //     NULL
    // );

    //     xTaskCreate(
    //     stepx,
    //     "stepx",
    //     8000,
    //     NULL,
    //     1,
    //     NULL
    // );

}

void loop(){}