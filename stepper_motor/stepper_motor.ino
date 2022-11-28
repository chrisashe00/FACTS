#define LEDC_CHANNEL_0  0
#define LEDC_CHANNEL_1  1
#define LEDC_CHANNEL_2  2
#define LEDC_CHANNEL_3  3

#define LEDC_TIMER_12_BIT 12
#define LEDC_BASE_FREQ  5000

  void ledcAnalogWrite(uint8_t channel, uint32_t value, uint32_t valueMax = 255) {
    uint32_t duty = (4095/valueMax)*min(value, valueMax); 

    ledcWrite(channel,duty);
  }
  
  const int A1A =  14;
  const int A1B = 27;
  const int B1A = 26;
  const int B2A = 25;
  const int ledPin = 33;
  int stepnumber = 0;
  int Pa; int Pb;

void setup() {

//  pinMode(A1A, OUTPUT);
//  pinMode(A1B, OUTPUT);
//  pinMode(B1A, OUTPUT);
//  pinMode(B2A, OUTPUT);

 ledcSetup(LEDC_CHANNEL_0, LEDC_BASE_FREQ, LEDC_TIMER_12_BIT); 
 ledcSetup(LEDC_CHANNEL_1, LEDC_BASE_FREQ, LEDC_TIMER_12_BIT);
 ledcSetup(LEDC_CHANNEL_2, LEDC_BASE_FREQ, LEDC_TIMER_12_BIT);
 ledcSetup(LEDC_CHANNEL_3, LEDC_BASE_FREQ, LEDC_TIMER_12_BIT);

 ledcAttachPin(A1A,LEDC_CHANNEL_0);
 ledcAttachPin(A1B,LEDC_CHANNEL_1);
 ledcAttachPin(B1A,LEDC_CHANNEL_2);
 ledcAttachPin(B2A,LEDC_CHANNEL_3);
 
 Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:


  digitalWrite (ledPin, HIGH);  // turn on the LED
  delay(500); // wait for half a second or 500 milliseconds
  digitalWrite (ledPin, LOW); // turn off the LED
  delay(500); // wait for half a second or 500 milliseconds
  
  for (int i=0; i<3199; i++)
  {
    stepnumber++;
    move(stepnumber,255,250);
    }

    delay(3000);
    for (int i=0; i<1599; i--)
    {
      move(stepnumber,255,1000);
      }
    delay(3000);
} 

void move(int stepnumber, int MAXpower, int wait) {
    Pa = (sin(stepnumber*0.098174)*MAXpower);
    Pb = (cos(stepnumber*0.098174)*MAXpower);
    if (Pa>0)
    {
      //analogWrite(A1A, Pa);
      //analogWrite(A1B,0); 
      ledcAnalogWrite(LEDC_CHANNEL_0,Pa);
      ledcAnalogWrite(LEDC_CHANNEL_1,0);
    }
    else
    {
      //analogWrite(A1A,0);
      //analogWrite(A1B, abs(Pa));
      ledcAnalogWrite(LEDC_CHANNEL_0,0);
      ledcAnalogWrite(LEDC_CHANNEL_1,abs(Pa));
    }
    
    if (Pb>0)
    {
      //analogWrite(B1A, Pb);
      //analogWrite(B2A,0); 
      ledcAnalogWrite(LEDC_CHANNEL_2,Pb);
      ledcAnalogWrite(LEDC_CHANNEL_3,0);
    }

    else
    {
      //analogWrite(B1A, 0);
      //analogWrite(B2A, abs(Pb));
      ledcAnalogWrite(LEDC_CHANNEL_2,0);
      ledcAnalogWrite(LEDC_CHANNEL_3,abs(Pb));
    }


    delayMicroseconds(wait);
    
  }
