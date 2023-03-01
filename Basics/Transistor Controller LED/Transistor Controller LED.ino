// controls an LED using NPN transistor

#define LED 13

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
}

// the loop function runs over and over again forever
void loop() {

  digitalWrite(LED,LOW);

  if (Serial.available())
  {
    char button =  Serial.read();
    if (button == 'r') 
    {
      Serial.println("received R, setting HIGH");
      digitalWrite(LED, HIGH);   // turn the LED off by making the voltage LOW
      delay(1000);
    }

    else{
    Serial.println("Nothing Received, Staying LOW");
    delay(1000);
    digitalWrite(LED, LOW);
    }
  }
  } 
