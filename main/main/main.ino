volatile unsigned int period_time = 0;
const uint8_t kInput = 4;//4 はpin 7を指す（Arduino Microの場合）
void freqCount();
void setup()
{
  Serial.begin(115200); // connect to the serial port
  Serial.println("Frequency Counter");
  attachInterrupt(kInput, freqCount, FALLING);
}

/*=========================
===   INTERUPT    ===
===========================*/

void freqCount()
{
  static unsigned long last_time = 0;
  unsigned long temp_time = micros();
  period_time = temp_time - last_time;
  last_time = temp_time;
}

/*=========================
===   MAIN LOOP   ===
===========================*/
void loop()
{
  static double freqold = 0;
  double freq;
  if (period_time != 0)
  {
    freq = double(1000000) / double(period_time);
    freq = 0.1*freq + 0.9*freqold;
    freqold = freq;
    Serial.println(freq);
  }

}
