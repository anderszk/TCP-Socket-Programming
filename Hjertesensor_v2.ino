#include <analogWrite.h> //Import the analogWrite library for ESP32 so that analogWrite works properly
#include <WiFi.h>//Imports the needed WiFi libraries
#include <WiFiMulti.h> //We need a second one for the ESP32 (these are included when you have the ESP32 libraries)
#include <SocketIoClient.h> //Import the Socket.io library, this also imports all the websockets



const char* ssid = "Asus telefon"; const char* password =  "fiskekakey0";
//const char* ssid = "Get-DD3CA1"; const char* password =  "HEBJFBPBDD";
const char* ip_esp32 = "192.168.43.116";
const char* ip_raspberry = "192.168.43.19";
int port_raspberry = 2520; // eller 22??


unsigned long prev = 0;
unsigned long prev_tid = 0;
unsigned long spike = 0;
int n = 0;
bool reg = false;
int beats_per_minute;
int previous = 0;
char* json_string;
char* mason_drink;

WiFiMulti WiFiMulti; //Declare an instane of the WiFiMulti library
SocketIoClient webSocket; //Decalre an instance of the Socket.io library


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

void changeDriveState(const char * DriveStateData, size_t length) { //Same logic as earlier
  Serial.printf("Drive State: %s\n", DriveStateData);
  Serial.println(DriveStateData);

  //Data conversion
  String dataString(DriveStateData);
  int DriveState = dataString.toInt();

  Serial.print("This is the Drive state in INT: ");
  Serial.println(DriveState);
  Drive(DriveState);
}

void changeTurnState(const char * TurnStateData, size_t length) {
  Serial.printf("Turn State: %s\n", TurnStateData);
  Serial.println(TurnStateData);

  //Data conversion
  String dataString(TurnStateData);
  int TurnState = dataString.toInt();

  Serial.print("This is the Turn state in INT: ");
  Serial.println(TurnState);
  softTurn(TurnState);
}

void stopDriving(const char * StopStateData, size_t length) {
  Serial.printf("Stop State: %s\n", StopStateData);
  Serial.println(StopStateData);

  //Data conversion
  String dataString(StopStateData);
  int StopState = dataString.toInt();

  Serial.print("This is the Stop state in INT: ");
  Serial.println(StopState);
  Stop(StopState);
}

void dataRequest(const char * DataRequestData, size_t length) {//This is the function that is called everytime the server asks for data from the ESP32
  Serial.printf("Datarequest Data: %s\n", DataRequestData);
  Serial.println(DataRequestData);

    //Data conversion
  String dataString(DataRequestData);
  int RequestState = dataString.toInt();

  if(RequestState == 0) { //If the datarequest gives the variable 0, do this (default)
    
    Serial.println(json_string);
    
    webSocket.emit("dataFromBoard", json_string); //Here the data is sendt to the server and then the server sends it to the webpage
    //Str indicates the data that is sendt every timeintervall, you can change this to "250" and se 250 be graphed on the webpage
  }
}

void Drive(bool Direction){ //Drive the car forwards or backwards (THIS IS JUST AN EXAMPLE AND NOT WHAT YOU HAVE TO USE IT FOR)

  if(Direction) {
    Serial.println("KJØR");
  } else {
    Serial.println("KJØR");
  }
  
}

void Stop(bool state){ //Stop the car
  Serial.println("STOP!!!");
}

void softTurn(bool Direction) { //Turn the car left or right (turns with the frontwheels)
   
  if(Direction) {
    Serial.println("Trykket venstre");
    //Turn motors one direction
  }
  else {
    Serial.println("Trykket Høyre");
    //Turn it the other direction
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

float gps_test(int latlong) {
  int Lat = random(-180, 180);
  int Long = random(-180, 180);
  //Serial.print("Latitude: "); Serial.println(Lat); Serial.print("Longitude: "); Serial.println(Long);
  if (latlong == 1)      {return Lat;}
  else if (latlong == 2) {return Long;}
  else {Serial.println("Error: No arg in function gps()! lol");}
}

bool is_user_wearing() {
  if (touchRead(T0) < 80) {return true;}
  else                    {return false;}
}

int peak(int current) {
  if (current > previous) {
    previous = current;}
  return previous;}

bool prewarn(int bpm) { //TODO: fem siste avlesninger på signalstyrke overgår margin..bruke liste?
  if (bpm > 130) {return true;}
  //else           {return false;}
}
  
int temp() {
  int read_temp = random(18, 23);
  return read_temp;}

/* JSON FORMAT
[
  {
    "bpm": bpm,
    "peak": peak,
    "prewarn": prewarn,
    "temp": temp,
    "wear": wear,
    "latitude": lat,
    "longitude": lon,
  }
]

{"bpm":94,"peak":700,"prewarn":0,"temp":20,"wear":0,"latitude":-5,"longitude":69}

{"bpm":96,"peak":1073422152,"prewarn":0,"temp":20,"wear":0,"latitude":-161.00,"longitude":10.00}
*/

char* make_json(int bpm_sim) {
  int heart_read = heartbeat_sim(bpm_sim);
  //Serial.println(heart_read);
  int bpm_read = bpm(heart_read);
  String c = ",";
  String opening = "{";
  String bpm_id = "\"bpm\":" + String(bpm_read) + c; 
  String peak_id = "\"peak\":" + String(peak(heart_read)) + c;
  String prewarn_id = "\"prewarn\":" + String(prewarn(bpm_read)) + c;
  String temp_id = "\"temp\":" + String(temp()) + c;
  String wear_id = "\"wear\":" + String(is_user_wearing()) + c;
  String latitude_id = "\"latitude\":" + String(gps_test(1)) + c;
  String longitude_id = "\"longitude\":" + String(gps_test(2));
  String closing = "}";
  
  String all_strings = opening + bpm_id + peak_id + prewarn_id + temp_id + 
         wear_id + latitude_id + longitude_id + closing;
  char* char_list = const_cast<char*>(all_strings.c_str());
  return char_list;
}

void send_json() {
  webSocket.emit("json", json_string);
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
  webSocket.on("DriveStateChange", changeDriveState);
  webSocket.on("TurnStateChange", changeTurnState);
  webSocket.on("stopDriving", stopDriving);

  //Send data to server/webpage
  webSocket.on("dataRequest", dataRequest); //Listens for the command to send data

  webSocket.begin(ip_raspberry, port_raspberry); //This starts the connection to the server with the ip-address/domainname and a port (unencrypted)
}

void setup() {  /* <==============< SETUP >==============> */
    Serial.begin(9600); //Start the serial monitor
    socket_wifi_setup();
}


void loop() { /* <==============< VOID LOOP >==============> */
  
  webSocket.loop(); //Keeps the WebSocket connection running
  json_string = make_json(15);
  //mason_drink = bake_mason(15);
  



  /* <==============< Kjører en gang per sek >==============> */
  if (prev + 1000 < millis()) {
    prev = millis();
    //bpm(heartbeat_sim(6));
    //Serial.println(json_string);
    //send_json();
 
    
    }
  /* <==============< Kjører en gang per sek >==============> */
}
