Adafruit_GPS GPS;
PulseOximeter pox;

void setup() {

  // temperature
  pinMode(A1, INPUT);
  Serial.begin(9600);

   // vitals
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);

  Serial.begin(9600);



}

void pos_func(){
    if (Serial.available() > 0) {
      if (pox.begin()) {
          string spO2_res = pox.getSpO2();
          string hb_res = pox.getHeartRate();
          Serial.println("Oxygen percentage: " + spO2_res + "; Heart rate: " + hb_res);
      }
      digitalWrite(3, HIGH);
  } else{
      Serial.println("No data");
      digitalWrite(3, LOW);
       }
  delay(1000);

}

void temp_func(){
   float temp = analogRead(A1) / 1023.0 * 5.0 * 100.0;
   Serial.println("temperature: " + to_string(temp));
   delay(1000);

}

void gps_func(){
    if (Serial.available() > 0) {
      string gpsResult = GPS.read();
      Serial.println("gps:" +gpsResult);
    } else {
        Serial.write("No data");
    }
    delay(1000);

}

void humidity_func(){
    float h = digitalRead(7);
   Serial.print("Humidity: ");
   Serial.println(h);
   delay(1000);
}

void loop() {
  pos_func();
  gps_func();
  temp_func();
  humidity_func();
}
