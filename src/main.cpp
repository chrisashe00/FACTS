#include <Arduino.h>

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

/*================VARIABLE DEFINITIONS================*/
int stepnumber = 0;
int Pa; int Pb;

/*================LEDC DUTY CYCLE SETUP================*/
#define LEDC_TIMER_12_BIT 12
#define LEDC_BASE_FREQ  5000

/*================Struct Definitions================*/
//input parameters for ledc analogWrite function
typedef struct{
  uint8_t channel;
  uint32_t value; 
  uint32_t valueMax = 255;  
} ledc_aw_params;

//input parameters for move function
typedef struct {
  int stepnumber; 
  int MAXpower; 
  int wait; 
} move_params;

/*================Function Definitions================*/

//Analogwrite using LEDC capabilities
  void ledcAnalogWrite(uint8_t channel, uint32_t value, uint32_t valueMax = 255) {

    //casting the input struct from void back to correct struct
    //ledc_aw_params ledc_param = *(ledc_aw_params *) data;

    //calculation of duty cycle
    //uint32_t duty = (4095/ledc_param.valueMax)*min(ledc_param.value, ledc_param.valueMax); 

    uint32_t duty = (4095/valueMax)*min(value, valueMax); 
    ledcWrite(channel,duty);
  }

  
  
void move(int stepnumber, int MAXpower, int wait) {
    //move_params instruction = *(move_params *) instructions;

    Pa = (sin(stepnumber*0.098174)*MAXpower);
    Pb = (cos(stepnumber*0.098174)*MAXpower);

    if (Pa>0)
    { 
      ledcAnalogWrite(LEDC_CHANNEL_0,Pa);
      ledcAnalogWrite(LEDC_CHANNEL_1,0);
    }
    else
    {
      ledcAnalogWrite(LEDC_CHANNEL_0,0);
      ledcAnalogWrite(LEDC_CHANNEL_1,abs(Pa));
    }
    
    if (Pb>0)
    {
      ledcAnalogWrite(LEDC_CHANNEL_2,Pb);
      ledcAnalogWrite(LEDC_CHANNEL_3,0);
    }

    else
    {
      ledcAnalogWrite(LEDC_CHANNEL_2,0);
      ledcAnalogWrite(LEDC_CHANNEL_3,abs(Pb));
    }
}

void move_routine(void *parameters) {

  for (int i=0; i<3199; i++)
  {
    stepnumber++;
    move(stepnumber,255,250);
    }

    vTaskDelay(3000/portTICK_PERIOD_MS);
    for (int i=0; i<1599; i++)
    { 
      stepnumber--;
      move(stepnumber,255,1000);
      }

    vTaskDelay(3000/portTICK_PERIOD_MS);
}

void led_flash(void *parameters) {

  digitalWrite (ledPin, HIGH);  // turn on the LED
  delay(500); // wait for half a second or 500 milliseconds
  digitalWrite (ledPin, LOW); // turn off the LED
  delay(500); // wait for half a second or 500 milliseconds
}

void setup() {
 pinMode (ledPin, OUTPUT);

  ledcSetup(LEDC_CHANNEL_0, LEDC_BASE_FREQ, LEDC_TIMER_12_BIT); 
  ledcSetup(LEDC_CHANNEL_1, LEDC_BASE_FREQ, LEDC_TIMER_12_BIT);
  ledcSetup(LEDC_CHANNEL_2, LEDC_BASE_FREQ, LEDC_TIMER_12_BIT);
  ledcSetup(LEDC_CHANNEL_3, LEDC_BASE_FREQ, LEDC_TIMER_12_BIT);

  ledcAttachPin(A1A,LEDC_CHANNEL_0);
  ledcAttachPin(A1B,LEDC_CHANNEL_1);
  ledcAttachPin(B1A,LEDC_CHANNEL_2);
  ledcAttachPin(B2A,LEDC_CHANNEL_3);
    Serial.begin(115200);

  //pinning move_routine function to core
  xTaskCreatePinnedToCore(
    move_routine, 
    "move routine", 
    2048, 
    NULL, 
    1, 
    NULL, 
    APP_CPU_NUM
  );

  //pinning led_flash function to core 
  xTaskCreatePinnedToCore(
    led_flash, 
    "led flash", 
    1024, 
    NULL, 
    1, 
    NULL, 
    APP_CPU_NUM
  );

  //Delete "setup and loop" task 
  vTaskDelete(NULL);
}

void loop() {
  
} 
