enum Commands {
  SETUP = 97, // COMMAND to set NLED
  LIGHT = 1
};
typedef enum Commands Commands;

#include <FastLED.h>

#define SERIAL_SPEED 500000
#define LED_PIN 7
#define COLOR_ORDER GRB
#define CHIPSET WS2812
#define MAX_LED_COUNT 500
#define BRIGHTNESS 100

CRGB leds[MAX_LED_COUNT];
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
    for(int c = 0; c < 3; c++)
    {
      leds[i][c] = Serial.read();
    }
  }
  FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, nLeds);
  FastLED.show();
  Serial.write(0);
  Serial.flush();
}

void setup()
{
  //Serial.begin(SERIAL_SPEED);
  FastLED.setBrightness( BRIGHTNESS );
  FastLED.setCorrection(Tungsten100W );
  Serial.begin(SERIAL_SPEED);
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
