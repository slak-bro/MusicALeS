//First arduino script done to have fancy led device
#include <FastLED.h>

#define LED_PIN     7
#define COLOR_ORDER GRB
#define CHIPSET     WS2811
#define NUM_LEDS    600

#define BRIGHTNESS  20
#define FRAMES_PER_SECOND 60
#define PERIOD 600

CRGB * leds;
//CRGB start = CRGB(144, 19, 200);
//CRGB end = CRGB(10, 200, 10);
#define COLORS 6
CRGB colors[] = {
  CHSV( HUE_PURPLE, 255, 255),
  CHSV( HUE_BLUE, 255, 255),
  CHSV( HUE_GREEN, 255, 255),
  CHSV( HUE_ORANGE, 255, 255),
  CHSV( HUE_YELLOW, 255, 255),
  CHSV( HUE_PINK, 255, 255),
};
CRGB current_color, next_color;
CRGB new_led;
unsigned int n = 0;
CRGB buf[NUM_LEDS * 2];

void choose_next_color(){
  current_color = next_color;
  int color_index = random(0, COLORS-1);
  if (colors[color_index] == current_color){
    color_index = color_index + 1 % COLORS;
  }
  next_color = colors[color_index];
}

CRGB grad(int i, CRGB start, CRGB end, int count = NUM_LEDS){
  CRGB out;
  out.r = start.r + (end.r-start.r)*(float(i)/count);
  out.g = start.g + (end.g-start.g)*(float(i)/count);
  out.b = start.b + (end.b-start.b)*(float(i)/count);
  return out;
}
void update_buf(int n){
  if (n%NUM_LEDS == 0){
    choose_next_color();
  }
  new_led = grad(n%NUM_LEDS, current_color, next_color);
  buf[n%(NUM_LEDS)] = new_led;
  buf[n%(NUM_LEDS) + NUM_LEDS] = new_led;
  
}
CRGB bigrad(int i, CRGB start, CRGB end){
  if(i < NUM_LEDS/2){
    return grad(i, start, end, NUM_LEDS/2);
  } else {
    return grad(i - NUM_LEDS/2, end, start, NUM_LEDS/2);
  }
}
void generateGradient(){
  for(int i=0; i < NUM_LEDS;i++){
      buf[i] = grad(i, colors[0], colors[1]);
  }
}

void setup_colors(){
  current_color = colors[0];
  next_color = colors[1];
}

void setup() {
  delay(3000); // sanity delay
  FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness( BRIGHTNESS );
  FastLED.setCorrection(Tungsten100W );
  generateGradient();
  setup_colors();
}

void loop()
{
  update_buf(n);
  leds = &buf[n%(NUM_LEDS)+1];
  FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.show(); // display this frame
  //FastLED.delay(1000 / FRAMES_PER_SECOND);
  n++;
  n%=NUM_LEDS;
}