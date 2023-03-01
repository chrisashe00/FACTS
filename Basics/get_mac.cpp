#include <Ps3Controller.h>

void setup() {
    Serial.begin(115200);
    Ps3.begin();
    delay(1000); // Add a delay after calling Ps3.begin()

    String address = Ps3.getAddress();

    Serial.print("The ESP32 MAC address is: ");
    Serial.println(address);
}

void loop () {
    Serial.println("hello world");
    delay(2000);

    String address = Ps3.getAddress();

    Serial.print("The ESP32 MAC address is: ");
    Serial.println(address);

}
