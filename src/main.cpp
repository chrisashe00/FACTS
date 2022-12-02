#include <Arduino.h>
#include <Stepper.h>

/*================PIN DEFINITIONS================*/
#define LEDC_CHANNEL_0  0
#define LEDC_CHANNEL_1  1
#define LEDC_CHANNEL_2  2
#define LEDC_CHANNEL_3  3

const int A1A =  14;
const int A1B = 27;
const int B1A = 26;
const int B2A = 25;
const int ledPin = 33;

const int stepsPerRev = 200;

Stepper myStepper(stepsPerRev, 14,27,26,25);


void task1(void * parameters){
      for(;;){
          Serial.println("clockwise");
          myStepper.step(stepsPerRev);
          vTaskDelay(1000 / portTICK_PERIOD_MS);

          // step one revolution in the other direction:
          Serial.println("counterclockwise");
          myStepper.step(-stepsPerRev);
          vTaskDelay(1000 / portTICK_PERIOD_MS);
      }

}

void task2(void * parametrs){
  digitalWrite(ledPin, HIGH); 
  vTaskDelay(500/portTICK_PERIOD_MS); 
  digitalWrite(ledPin, LOW); 
  vTaskDelay(500/portTICK_PERIOD_MS);
}

void setup(){
  myStepper.setSpeed(60);
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);




xTaskCreate(
    task1, 
    "Task 1",
    1000,
    NULL,
    1,
    NULL
  );

  xTaskCreate(
    task2, 
    "Task 2", 
    1024, 
    NULL, 
    1, 
    NULL
  );


}

void loop(){

}


