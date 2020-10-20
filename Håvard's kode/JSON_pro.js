/* deklarer varibler (kan vell gjøres ved oppdaterte variabler?) */

var bpm = 1
var peak = 1
var prewarn = 1
var wear = 1
var latitude = 1
var longitude = 1

// var data_string = DATA_FRA_ESP32
var data_string = `{"bpm":96,"peak":1073,"prewarn":0,"temp":20,"wear":0,"latitude":-161.50,"longitude":10.00}`
console.log("\n\nRaw string from ESP32:")
console.log(data_string) //printer stringen
var data_json = JSON.parse(data_string) //konverterer til JSON
console.log("\n\nJSON format from string:")
console.log(data_json) //printer JSON

//Oppdaterer variabler
bpm = data_json.bpm
peak = data_json.peak
prewarn = data_json.prewarn
wear = data_json.wear
latitude = data_json.latitude
longitude = data_json.longitude


//printer nye variabler
console.log("\n\nUpdated Variables:")
console.log("bpm = " + bpm);
console.log("peak = " + peak);
console.log("prewarn = " + prewarn);
console.log("wear = " + wear);
console.log("latitude = " + latitude);
console.log("longitude = " + longitude);


