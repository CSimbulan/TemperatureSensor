#include <dht.h>
dht DHT;  // redefines dht to DHT, not really necessary

#include <Wire.h>
#include <Adafruit_MLX90614.h>
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

#include "RTClib.h"  //RTC module, for time keeping
RTC_DS1307 rtc;

#include <SD.h>         //SD Card Library
#include <SPI.h>

const int CS_pin = 53;     // pin 53 is for SD data logging **ON THE MEGA**
/*Pololu SD card reader
DI - 51
DO - 10
SCLK - 52
CS - 53 */

const int DHT22_PIN = 28;   // we chose pin 28 to be the input pin of the analog signal

#include <Adafruit_GFX.h> //Graphics Library
#include <Adafruit_PCD8544.h> //OLED Library

// Software SPI (slower updates, more flexible pin options):
// pin 7 - Serial clock out (SCLK)
// pin 6 - Serial data out (DIN)
// pin 5 - Data/Command select (D/C)
// pin 4 - LCD chip select (CS)
// pin 3 - LCD reset (RST)
Adafruit_PCD8544 display = Adafruit_PCD8544(7, 6, 5, 4, 3);

// analog input pins
#define TMP36_pin A0
#define photoresistor_pin A1

const float refresh_rate = 60e3;   // main refresh rate on the 'void loop()'

String hr;
String mn;

long previousMillis = 0;
long previousMillis2 = 0;
const long interval = 1000;      // main refresh rate on the 'void loop()'
const long saveInterval = 30000;   // SD card logging period in ms

boolean SDstatus = true;

/////////////////////////////////////////
//----------- VOID SETUP --------------//
/////////////////////////////////////////
void setup()
{
  Serial.begin(9600);
  Wire.begin();
  mlx.begin();
  rtc.begin();
  display.begin();
  display.setTextSize(0);
  display.setTextColor(BLACK);
  display.setCursor(0, 0);
  display.setContrast(50);
  display.setRotation(2);
  display.clearDisplay();

  if (! rtc.isrunning()) {       // this is just to check if RTC is running
    Serial.println("RTC is NOT running!");
  }

  //Initialize Card
  if (!SD.begin(CS_pin)) {   //check if SD card works
    Serial.println("SD Card Failure");
    return;
  }

  Serial.println("SD Card Ready");

  // printing header in Serial com
  Serial.print("--- Program begin ---  \t   program last updated 2015/4/30");
  Serial.print("\t refresh rate=");   Serial.print(refresh_rate / 1000.0);  Serial.println(" s");
  DateTime now = rtc.now();
  String date = String(now.year()) + "/" + String(now.month()) + "/" + String(now.day());
  Serial.print("Today's date: "); Serial.println(date);
  Serial.println();
  String header = "Year, Month, Day, Hour, Min, Sec, DHT.hum, DHT.temp, lightvalue, timer(min)";
  Serial.print(header);
  Serial.println();


}/************END SETUP************/

/////////////////////////////////////////
//----------- VOID LOOP ---------------//
/////////////////////////////////////////
void loop() {
  unsigned long currentMillis = millis();
  //--- DHT sensor ---//
  if (currentMillis - previousMillis > interval) {

    previousMillis = currentMillis;
    int chk = DHT.read22(DHT22_PIN);  //reads a value from DHT sensor called chk

    //--- photoresistor ---//
    float lightVal = analogRead(photoresistor_pin);

    ///// Organizing data into long string ////////////////

    // next 2 lines obtains the date and time in RTC module
    DateTime now = rtc.now();    // takes snapshot of date and time values in RTC
    String timestamp = String(now.year()) + " " + String(now.month()) + " " + String(now.day()) + " " + String(now.hour()) + " " + String(now.minute()) + " " + String(now.second());
    String timer = String(millis() / 60000.0); // this is a backup in case RTC stops working

    //Display the data on the OLED mintor

    //Reset the display
    display.clearDisplay();

    //Format the hour and minute
    if (now.hour() > 12) {
      hr = String(now.hour() - 12);
    } else {
      hr = String(now.hour());
    };
    if (now.minute() > 10) {
      mn = String(now.minute());
    } else {
      mn = "0" + String(now.minute());
    };
    String currentTime = hr + ":" + mn + "."  + String(now.second());
    display.print(currentTime);
    display.println();
    display.print("Temp: ");
    display.print(DHT.temperature);
    display.print(" C");
    display.println();
    display.print("Hmd: ");
    display.print(DHT.humidity);
    display.print("%");
    display.println();
    display.print("Light: ");
    display.print(lightVal);
    display.drawCircle(68, 9, 1, BLACK);    // degree symbol
    display.println();
//    display.display();

    //Create Data string for storing to SD card
    //We will use CSV Format
    String dataString = String(timestamp) + " " + String(DHT.humidity) + " " + String(DHT.temperature) + " " + String(lightVal) + " " + String(timer);
    //  + String(mlx.readAmbientTempC()) + ", " + String(mlx.readObjectTempC());

    // this loop happens every dt= saveInternal, which determines the logging frequency of the SD card
    if (currentMillis - previousMillis2 > saveInterval) {
      previousMillis2 = currentMillis;
      //Open a file in the SD card to write in

      File logFile2 = SD.open("data011d.txt", FILE_WRITE);   // make sure the file name is consistent with the one in VOID SETUP
      if (logFile2)
      {
        logFile2.println(dataString);  //prints the data string in a txt file in SD card
        logFile2.close();
        SDstatus = true;
      }
      else
      {
        Serial.println("Couldn't open log file in SD card");  // If SD card stops working, it will show in serial com
        SDstatus = false;
      }
      Serial.println("Data recorded to SD card");
    }  
    
    Serial.println(dataString);   //prints data string in Serial com monitor
    
    if (SDstatus){
      display.print("SD logging :) ");
    }
    else{
      display.print("SD fail :( " );
    }
    display.display();
  }

}/************END LOOP************/





