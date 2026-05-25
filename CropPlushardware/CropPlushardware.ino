#include <DHT.h>

#define DHTPIN 2     
#define DHTTYPE DHT11   

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600); 
  dht.begin();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  int m = analogRead(A0); 
  int c = analogRead(A1); 

  int mPercent = map(m, 1023, 0, 0, 100);

  // Format: Temp,Moisture,CO2,Humidity
  Serial.print(t);
  Serial.print(",");
  Serial.print(mPercent);
  Serial.print(",");
  Serial.print(c);
  Serial.print(",");
  Serial.println(h);

  delay(2000); 
}