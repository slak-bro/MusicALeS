#include <SoftwareSerial.h>
#define BURST_SIZE 63
byte data[BURST_SIZE];
int correct = 0;
SoftwareSerial SSerial(50, 8); // RX, TX
// Not working great above 38400
unsigned long speed = 57600;
void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(speed);
  while (!Serial) {}
  Serial.println("Starting Software Serial Data test...");
  Serial.flush();
}

void loop() { 
    correct = 0;
    SSerial.begin(speed);
    for(int i=0; i<BURST_SIZE; i++)data[i] = random(256);
    Serial.write(data, BURST_SIZE);
    Serial.flush();
    for(int i=0; i<BURST_SIZE; i++){
        while(SSerial.available()<=0){}
        if(SSerial.read() == data[i])correct++;
    }
    SSerial.end();
    Serial.println("");
    Serial.print("Correct: ");
    Serial.print(correct);
    Serial.print("/");
    Serial.print(BURST_SIZE);
    Serial.print("\n");
    Serial.flush();    
}