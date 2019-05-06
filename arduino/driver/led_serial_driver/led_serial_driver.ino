enum Commands {
  SETUP = 97, // COMMAND to set NLED
  LIGHT = 1
};
typedef enum Commands Commands;
#include <math.h>
#include <FastLED.h>

#define SERIAL_SPEED 500000
#define LED_PIN 7
#define COLOR_ORDER GRB
#define CHIPSET WS2812
#define MAX_LED_COUNT 300
#define BRIGHTNESS 100

CRGB leds[MAX_LED_COUNT];
unsigned short nLeds = MAX_LED_COUNT;
byte command = -1;

void wait_serial_bytes(int n) {
  while (Serial.available() < n) {}
  return;
}
#define SIGMA2 900
void init_display() {
  int16_t left = 0, right = MAX_LED_COUNT - 1;
  uint8_t incr = 1;
  float coeffl, coeffr;
  for(uint16_t i=0; i < MAX_LED_COUNT/2; i++){
    for(int16_t k=0; k < MAX_LED_COUNT; k++){
      coeffl = exp(-pow(k-left,2)/(2*SIGMA2));
      coeffr = exp(-pow(k-right,2)/(2*SIGMA2));
      leds[k] = CHSV( HUE_GREEN, 255,floor(coeffl*255)) + CHSV( HUE_ORANGE, 255,floor(coeffr*255));
    }
    FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, MAX_LED_COUNT); 
    FastLED.show();
    left+=incr;
    right-=incr;
    if(i > 100)incr=2;
    else if(i > 250)incr = 3;
  }
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
  init_display();
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
