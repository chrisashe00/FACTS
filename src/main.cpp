#include <Arduino.h>
#include <Stepper.h>

const int stepsPerRevolution = 200; // steps per rev for our motors
const float stepAngle = 1.8; // our motor's step angle in degrees
const float stepRad = stepAngle * (3.141 / 180); // step angle in radians 

int brightness = 128; // starting brightness for the LED
int blue_brightness = 0; // starting brightness for the blue LED
int lime_brightness = 0; // starting brightness for the lime LED

int fadeAmount = 5; // How much to change the brightness each step when fading
bool isFading = false; // Whether the LED is currently fading


// -----pins 33,32,35,34 give error-----
Stepper myStepperz(stepsPerRevolution,1,2,3,4); // Z stepper and pins 
Stepper myStepperx(stepsPerRevolution,5,18,19,21); // X stepper and pins
Stepper mySteppery(stepsPerRevolution,14,27,26,25); // Y stepper and pins 

const int BLUE_LED_PIN = 12; // Blue LED pin assignment
const int LIME_LED_PIN = 13; // Lime LED pin assignment

int ZPosition = 0;  //initialise positions
int YPosition = 0;
@ -226,37 +232,120 @@ void blueLED(void * parameters)
  for(;;)
  {
     if (Serial.available()) {
    char input = Serial.read();
    if (input == '8') {
      brightness = max(0, brightness - 32); // decrease brightness by 32 (out of 255)
      analogWrite(BLUE_LED_PIN, brightness);
    char blue_input = Serial.read();
    if (blue_input == '9') {
      blue_brightness = max(0, blue_brightness - 32); // decrease brightness by 32 (out of 255)
      analogWrite(BLUE_LED_PIN, blue_brightness);
      Serial.print("\n");
      Serial.print("Current Brightness: ");
      Serial.print(brightness);
      Serial.print("Current BLUE Brightness: ");
      Serial.print(blue_brightness);
      Serial.print('\n');
    } 
    
    else if (input == '9') {
      brightness = min(255, brightness + 32); // increase brightness by 32 (out of 255)
      analogWrite(BLUE_LED_PIN, brightness);
    else if (blue_input == '8') {
      blue_brightness = min(255, blue_brightness + 32); // increase brightness by 32 (out of 255)
      analogWrite(BLUE_LED_PIN, blue_brightness);
      Serial.print("\n");
      Serial.print("Current Brightness: ");
      Serial.print(brightness);
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
  }

  vTaskDelay(1000/portTICK_PERIOD_MS);

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

        else{
            lime_brightness = 255;
        }
    

     //   vTaskDelay(500/portTICK_PERIOD_MS);
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
@ -279,27 +368,36 @@
        1000,
        NULL,
        1,
        NULL
        0
    );

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