enum Commands {
  SETUP = 97, // COMMAND to set NLED
  LIGHT = 1
};
typedef enum Commands Commands;

#include <WS2812.h>

#define SERIAL_SPEED 500000
#define LED_PIN 7
#define MAX_LED_COUNT 300
#define BRIGHTNESS 100

WS2812 LED(MAX_LED_COUNT);
cRGB color_value;
unsigned short nLeds = MAX_LED_COUNT;
byte command = -1;

void wait_serial_bytes(int n) {
  while (Serial.available() < n) {}
  return;
}

void setup_command()
{
  //    Serial.println("Setup");
  wait_serial_bytes(2);
  unsigned char b0 = Serial.read();
  unsigned char b1 = Serial.read();
  // Serial.print("b0 : ");
  // Serial.print(b0);
  // Serial.print("b1 : ");
  // Serial.print(b1);
  // Serial.print(" ");
  // Serial.flush();

  nLeds = b1 + 256 * b0;

  Serial.print("nLeds : ");
  Serial.print(nLeds);
  Serial.println("");
  Serial.flush();
}
void light_command()
{
  // Serial.println("LIGHT");
  // Serial.flush();
  Serial.write((byte) 0);
  Serial.flush();
  for (int i = 0; i < nLeds; i++)
  {
    wait_serial_bytes(3);
    color_value.r = Serial.read();
    color_value.g = Serial.read();
    color_value.b = Serial.read();
    LED.set_crgb_at(i, color_value);
  }
  LED.sync();
  Serial.write(0);
  Serial.flush();
}

void setup()
{
  Serial.begin(SERIAL_SPEED);
  LED.setOutput(LED_PIN);
  LED.set_crgb_at(0,color_value);
  LED.sync();
  color_value.r = 255;
  delay(1000);
  LED.set_crgb_at(0,color_value);
  LED.sync();
  color_value.r = 0;
  delay(1000);
  LED.set_crgb_at(0,color_value);
  LED.sync();
} 

void loop()
{
  if (Serial.available() > 0)
  {
    command = Serial.read();
    switch (command)
    {
      case SETUP:
        setup_command();
        break;
      case LIGHT:
        light_command();
        break;
      default:
        Serial.println("Unknown");
        break;
    }
  }
}
