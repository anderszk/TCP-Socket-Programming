#include <analogWrite.h> //Import the analogWrite library for ESP32 so that analogWrite works properly
#include <WiFi.h>//Imports the needed WiFi libraries
#include <TinyGPS++.h>
#include <WiFiMulti.h> //We need a second one for the ESP32 (these are included when you have the ESP32 libraries)
#include <SocketIoClient.h> //Import the Socket.io library, this also imports all the websockets
#include "DFRobot_Heartrate.h"

#define heartratePin 34
#define tempPin 33
#define gpsPin 26

const char* ssid = "Asus telefon"; const char* password =  "fiskekakey0";
//const char* ssid = ""; const char* password =  "";
const char* ip_esp32 = "192.168.43.116";
const char* ip_raspberry = "192.168.43.19";
int port_raspberry = 2520; // eller 22??


unsigned long prev_1 = 0;
unsigned long prev_2 = 0;
unsigned long prev_3 = 0;
unsigned long prev_4 = 0;
unsigned long prev_tid = 0;
unsigned long spike = 0;
unsigned long timer = 0;
int n = 0;
bool reg = false;
bool pre_warning = false;
bool critical_warning = false;
bool timer_starter = true;
int beats_per_minute;
int previous = 0;
int comparator = 0;
int dummy_for_bpm = 0;
char* json_string;
char* mason_drink;
bool gps_access = 1;
int noise;

WiFiMulti WiFiMulti; //Declare an instane of the WiFiMulti library
SocketIoClient webSocket; //Decalre an instance of the Socket.io library
TinyGPSPlus gps; // The TinyGPS++ object
HardwareSerial SerialGPS(1);
DFRobot_Heartrate heartrate(ANALOG_MODE); ///< ANALOG_MODE or DIGITAL_MODE


void event(const char * payload, size_t length) { //Default event, what happens when you connect
  Serial.printf("got message: %s\n", payload);
}

void changeLEDState(const char * LEDStateData, size_t length) { //What happens when the ESP32 receives a instruction from the server (with variable) to change the LED
  Serial.printf("LED State: %s\n", LEDStateData); //First we print the data formated with the "printf" command
  Serial.println(LEDStateData); //Then we just print the LEDStateData which will be a int (0 og 1 so in reeality bool) that tells us what to do with the LED

  //Data conversion //We need som data processing to make this work
  String dataString(LEDStateData); //First we convert the const char array(*) to a string in Arduino (this makes thing easier)
  int LEDState = dataString.toInt(); //When we have a string we can use the built in Arduino function to convert to an integer

  Serial.print("This is the LED state in INT: "); //We print the final state
  Serial.println(LEDState);
  digitalWrite(18, LEDState);//We now use the varible to change the light (1 is on, 0 is off)
}

void dataRequest(const char * DataRequestData, size_t length) {//This is the function that is called everytime the server asks for data from the ESP32
  Serial.printf("Datarequest Data: %s\n", DataRequestData);
  Serial.println(DataRequestData);

    //Data conversion
  String dataString(DataRequestData);
  int RequestState = dataString.toInt();

  if(RequestState == 0) { //If the datarequest gives the variable 0, do this (default)
    
    Serial.println(json_string);
    
    //webSocket.emit("dataFromBoard", json_string); //Here the data is sendt to the server and then the server sends it to the webpage
    //Str indicates the data that is sendt every timeintervall, you can change this to "250" and se 250 be graphed on the webpage
  }
}

/* ==========================<Health functions>========================== */

int heartbeat_sim(int bpm) { //60 bpm = 1hz, 10 liste iterasjoner per s.
  int liste[] = {400, 421, 420, 464, 580, 700, 611, 390, 411, 405};
  unsigned long tid_nu = millis();
  int updatetid = 5400 / bpm; //konverter fra bpm til periode tid. en faktor på 10 pga 10 elemter i liste.
  if (prev_tid + updatetid < tid_nu ) {
    prev_tid = millis();
    if (n > 8)        {n = 0;}
    else              {n++;}
    //Serial.print("heartrate liste: ");
    //Serial.println(liste[n]);
    }
  return liste[n];}

int heartsensor_read() {
  return heartbeat_sim(60);
  //return analogRead(heartratePin);
}

int bpm(int input) {
  int threshold = 600;
  if (input > threshold and reg == false) {
    //beats_per_minute = constrain((60 / 1000) / (millis() - spike), 0, 1000);
    beats_per_minute = 60000 / ((millis() - spike));
    spike = millis();
    reg = true;
    //Serial.print("bpm: ");
    //Serial.println(beats_per_minute);
    }
  else if (reg == true and input < threshold) {reg = false;}
  return beats_per_minute;}

void gps_allowed(const char * gps_allowed, size_t length) {

  //Data conversion //We need som data processing to make this work
  String dataString(gps_allowed); //First we convert the const char array(*) to a string in Arduino (this makes thing easier)
  gps_access = dataString.toInt(); //When we have a string we can use the built in Arduino function to convert to an integer
}

float gps_test(int latlong) {
  if (gps_access == 1) {
    float Lat = 63.415975; //random(-90, 90);
    float Long = 10.406444; //random(-90, 90);
    //Serial.print("Latitude: "); Serial.println(Lat); Serial.print("Longitude: "); Serial.println(Long);
    if (latlong == 1)      {return Lat;}
    else if (latlong == 2) {return Long;}
    else {Serial.println("Error: No arg in function gps()! lol");}}
  else if (gps_access == 0) {
    return 0;}
  }

double getGPS(String select) {
  if (gps_access) {
    if      (select == "lat") {return double(63.415975);} //gps.location.lat();}
    else if (select == "lng") {return double(10.406444);} //gps.location.lng();}
    else if (select == "alt") {return double(31);} //gps.altitude.meters();}
    else if (select == "sat") {return double(6);} //gps.satellites.value();}
    else    {Serial.println("Error: No arg in function gps()! lol");}
    }
  else      {return double(0.0);}
  }

bool is_user_wearing() { 
  if (touchRead(T0) < 80) {return true;}
  else                    {return false;}
}

int peak(int current) {
  if (current > previous) {
    previous = current;}
  return previous;}

bool prewarn(bool reset) {
  
  int threshold = 1800; //faktor på bpm??
  
  if (reset) {pre_warning = false;}
  if (noise < threshold && !pre_warning) {
    
    int Value = heartsensor_read();
    noise += abs(Value - comparator);
    comparator = Value;
    //Serial.println(noise);
  
    if (prev_3 + 1000 < millis()) {
    prev_3 = millis();
    noise = 0; 
  
    return false;
  }
  }
  
  else {

  pre_warning = true;
  noise = 0;
  return true;
  }

}

void reset() {
  prewarn(1);
  critical(1);
}

bool critical(bool reset) {
  
  dummy_for_bpm = 20; //bpm(); LEGG TIL
  
  if (reset) {critical_warning = false;}

  if (dummy_for_bpm > 10) {
    timer_starter = true;
    return false;
    }

  else if (is_user_wearing() and timer_starter and !critical_warning) {
    timer = millis();
    timer_starter = false;
    return false;
    }
    
  else {
    return false;}

  if (timer + 10000 < millis()) {
    critical_warning = true;
    return true;
    }



}

int temp() {
  //int read_temp = analogRead(tempPin);
  int read_temp = random(20, 23);
  return read_temp;}

/* JSON FORMAT
  {
    "bpm": bpm,
    "prewarn": prewarn,
    "critical": true/false,
    "temp": temp,
    "gps": {
      "latitude": lat,
      "longitude": lon,
      }
    "unit_data": {
      "home": "Lerkendal",
      "connection": "WIFI",
      "type": "ESP32 Wroom32"
      }
  }

{"bpm":94,"peak":700,"prewarn":0,"temp":20,"wear":0,"latitude":-5,"longitude":69}

{"bpm":96,"prewarn":0,"critial": 0,"temp":20,"gps":{"latitude":-161.00,"longitude":10.00},"unit_data":{"home": "Lerkendal", "connection": "WIFI", "type": "ESP32 Wroom32"}}
*/

char* make_json() {
  int heart_read = heartsensor_read();
  //Serial.println(heart_read);
  int bpm_read = bpm(heart_read);
  String lerkendal_string = "\"Lerkendal\"";
  String wifi_string = "\"WIFI\"";
  String esp32_string = "\"ESP32 Wroom32\"";
  String c = ",";
  String opening = "{";
  String closing = "}";
  String bpm_id =        "\"bpm\":"         + String(bpm_read) + c; 
  String prewarn_id =    "\"prewarn\":"     + String(prewarn(0)) + c;
  String critical_id =   "\"critical\":"    + String(critical(0)) + c;
  String temp_id =       "\"temp\":"        + String(temp()) + c;
  String gps_id =        "\"gps\":"         + opening;
  String latitude_id =   "\"latitude\":"    + String(getGPS("lat")) + c;
  String longitude_id =  "\"longitude\":"   + String(getGPS("lng")) + c;
  String altitude_id =   "\"altitude\":"    + String(getGPS("alt")) + c;
  String satellite_id =  "\"satellite\":"   + String(getGPS("sat")) + closing + c;
  String unit_data_id =  "\"unit_data\":"   + opening;
  String home_id =       "\"home\":"        + lerkendal_string + c;
  String connection_id = "\"connection\":"  + wifi_string + c;
  String type_id =       "\"type\":"        + esp32_string + closing;
  
  
  String all_strings = opening + bpm_id + prewarn_id + critical_id + temp_id + gps_id + latitude_id + longitude_id 
         + altitude_id + satellite_id + unit_data_id + home_id + connection_id + type_id + closing;
         
  char* char_list = const_cast<char*>(all_strings.c_str());
  return char_list;
}

void send_json() {
    if (is_user_wearing()){
      webSocket.emit("dataFromBoard", json_string);
    }
}

void send_livedata() {
  if (is_user_wearing()){
    String read_sensor = String(heartsensor_read());
    char* read_sensor_list = const_cast<char*>(read_sensor.c_str());
    webSocket.emit("livedata", read_sensor_list);
    Serial.println(read_sensor_list);
  }
}

void socket_wifi_setup() {

  Serial.setDebugOutput(true); //Set debug to true (during ESP32 booting)

  Serial.println();
  Serial.println();
  Serial.println();

    for(uint8_t t = 4; t > 0; t--) { //More debugging
        Serial.printf("[SETUP] BOOT WAIT %d...\n", t);
        Serial.flush();
        delay(1000);
    }

  WiFiMulti.addAP(ssid, password); //Add a WiFi hotspot (addAP = add AccessPoint)

  while(WiFiMulti.run() != WL_CONNECTED) { //Here we wait for a successfull WiFi connection untill we do anything else
    Serial.println("Not connected to wifi...");
      delay(100);
  }

  Serial.println("Connected to WiFi successfully!"); //When we have connected to a WiFi hotspot

  //Here we declare all the different events the ESP32 should react to if the server tells it to.
  //a socket.emit("identifier", data) with any of the identifieres as defined below will make the socket call the functions in the arguments below
  webSocket.on("clientConnected", event); //For example, the socket.io server on node.js calls client.emit("clientConnected", ID, IP) Then this ESP32 will react with calling the event function
  webSocket.on("LEDStateChange", changeLEDState);
  webSocket.on("gps_allowed", gps_allowed);
  //webSocket.on("reset", reset_warning);

  //Send data to server/webpage
  webSocket.on("dataRequest", dataRequest); //Listens for the command to send data

  webSocket.begin(ip_raspberry, port_raspberry); //This starts the connection to the server with the ip-address/domainname and a port (unencrypted)
}

void setup() {  /* <============<   SETUP   >==============> */
    Serial.begin(115200); //Start the serial monitor
    pinMode(heartratePin, INPUT);
    pinMode(tempPin, INPUT);
    SerialGPS.begin(9600, SERIAL_8N1, 16, 17);
    //socket_wifi_setup();
}


void loop() { /* <==============< VOID LOOP >==============> */
  
  webSocket.loop(); //Keeps the WebSocket connection running
  json_string = make_json();

    /* <==============< Kjører mange gang per sek >==============> */
  if (prev_1 + 100 < millis()) {
    prev_1 = millis();
    send_livedata();
    }
  /* <==============< Kjører en gang per sek >==============> */
  /* |||||||||||||||||||||||||||||||||||||||||||||||||||||||| */
  /* <==============< Kjører en gang per sek >==============> */
  if (prev_2 + 1000 < millis()) {
    prev_2 = millis();
    send_json();
    }
  /* <==============< Kjører en gang per sek >==============> */
}
