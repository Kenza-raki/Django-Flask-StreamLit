#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// Informations de connexion Wi-Fi
const char* ssid = "Etudiants";
const char* password = "ENSAJ2020";

// Déclaration des pins pour les LEDs
#define Led_r D1      
#define Led_v D2       
#define Led_o D3      
#define Led_r2 D5     
#define Led_o2 D6     
#define Led_v2 D7

// Temps pour chaque état (default times)
int greenTime = 6000;
int orangeTime = 2000;
int redTime = 6000;

int state = 0;
unsigned long previousMillis = 0;
unsigned long interval = greenTime;

ESP8266WebServer server(80);

String current_traffic_direction = "default";
int current_traffic_duration = 6;
int total_vehicles = 0;
int way1_vehicles = 0; // Added variable for way 1 vehicles
int way2_vehicles = 0; // Added variable for way 2 vehicles
float confidenceThreshold = 0.4;
int framesBeforeEvaluation = 30;
void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println("Connexion au %s \n,ssid");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Wi-Fi connecté au %s \n,ssid");
  Serial.print("Adresse IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("***************");
  // Configuration des LEDs comme sorties
  pinMode(Led_r, OUTPUT);
  pinMode(Led_v, OUTPUT);
  pinMode(Led_o, OUTPUT);
  pinMode(Led_r2, OUTPUT);
  pinMode(Led_o2, OUTPUT);
  pinMode(Led_v2, OUTPUT);

  // Configuration des routes du serveur web
  server.on("/", handleRoot);
  server.on("/changeState", changeStateHandler);
  server.on("/getStatus", getStatusHandler);
  server.on("/setTraffic", handleSetTraffic);
    server.on("/getTrafficData", handleGetTrafficData);
   server.on("/setConfig", handleSetConfig);
    server.on("/getConfig", handleGetConfig);


  server.begin();
  Serial.println("Serveur web démarré");
}

void loop() {
  server.handleClient();

  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    changeState();
    previousMillis = currentMillis;
  }
}

// Fonction pour afficher la page web principale
void handleRoot() {
 String page = "<html><head>";
  page += "<title>Contrôle des Feux Rouge</title>";
  page += "<style>";

  // Style général de la page
  page += "body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f4; }";
  page += "h1 { color: #333; }";

  // Style pour les feux
  page += ".intersection { display: flex; justify-content: center; gap: 50px; margin-top: 50px; }";
  page += ".traffic-light { display: flex; flex-direction: column; align-items: center; width: 100px; background: #333; padding: 20px; border-radius: 10px; }";
  page += ".light { width: 60px; height: 60px; margin: 10px auto; border-radius: 50%; background: #555; }";
  page += ".red { background: #ff0000; }";
  page += ".orange { background: #ffa500; }";
  page += ".green { background: #00ff00; }";

  // Bouton de contrôle
  page += "button { padding: 10px 20px; margin: 20px; font-size: 16px; background: #007bff; color: #fff; border: none; border-radius: 5px; cursor: pointer; }";
  page += "button:hover { background: #0056b3; }";

    page += "input[type='number'] { padding: 8px; margin: 10px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; }";
    page += "label { display: block; margin-top: 10px; }";
    page += "section { margin: 20px; padding: 15px; border: 1px solid #ddd; background: #fff; border-radius: 5px; }";

  page += "</style></head><body>";
  page += "<h1>Contrôle des Feux de Croisement</h1>";

  // Section pour les deux feux de signalisation
  page += "<div class='intersection'>";

  // Feu 1
  page += "<div class='traffic-light'>";
  page += "<div class='light' id='lightRed1'></div>";
  page += "<div class='light' id='lightOrange1'></div>";
  page += "<div class='light' id='lightGreen1'></div>";
  page += "</div>";

  // Feu 2
  page += "<div class='traffic-light'>";
  page += "<div class='light' id='lightRed2'></div>";
  page += "<div class='light' id='lightOrange2'></div>";
  page += "<div class='light' id='lightGreen2'></div>";
  page += "</div>";

  page += "</div>";

  // Bouton pour changer l'état
  page += "<button onclick='changeState()'>Changer d'état</button>";
    page += "<section class='traffic-info'>";
    page += "<h2>Traffic Information</h2>";
    page += "<p>Current Direction: <span id='currentDirection'>default</span></p>";
    page += "<p>Time Left: <span id='timeLeft'>0</span> s</p>";
    page += "<p>Way 1 Vehicles: <span id='way1Vehicles'>0</span></p>"; // Show way 1 vehicles
    page += "<p>Way 2 Vehicles: <span id='way2Vehicles'>0</span></p>"; // Show way 2 vehicles
      page += "<p>Total Vehicles: <span id='totalVehicles'>0</span></p>";
        page += "<p>Frames before evaluation: <span id='framesBeforeEvaluation'>30</span></p>";
          page += "<p>Confidence Threshold: <span id='confidenceThreshold'>0.4</span></p>";
     page += "<p>Way with more traffic: <span id='wayWithMoreTraffic'>default</span></p>";  // Way with more traffic
     page += "</section>";
    page += "<section class='manual-controls'>";
        page += "<h2>Manual Control</h2>";
          page += "<label for='duration'>Duration (s):</label>";
            page += "<input type='number' id='duration' name='duration' min='0' value='" + String(current_traffic_duration) + "'>";
           page += "<button onclick='setDuration()'>Set Duration</button>";
        page += "<label for='confidenceThresholdInput'>Confidence Threshold:</label>";
           page += "<input type='number' id='confidenceThresholdInput' name='confidenceThreshold' min='0' max='1' step='0.1' value='" + String(confidenceThreshold) + "'>";
           page += "<button onclick='setConfidenceThreshold()'>Set Confidence Threshold</button>";
    page += "</section>";

  // JavaScript pour la mise à jour dynamique
  page += "<script>";

  // Fonction pour changer d'état
    page += "function changeState() {";
  page += "fetch('/changeState').then(response => response.text()).then(data => {";
      page += "updateLights();";
      page += "updateTrafficData();";
      page += "});";
   page += "}";
    page += "function setDuration() {";
         page += " const duration = document.getElementById('duration').value;";
       page += " fetch('/setConfig?duration=' + duration).then(response => response.text()).then(data => {";
      page += " updateTrafficData();";
        page += "});";
  page += "}";
       page += "function setConfidenceThreshold() {";
          page += " const confidenceThresholdInput = document.getElementById('confidenceThresholdInput').value;";
           page += " fetch('/setConfig?confidenceThreshold=' + confidenceThresholdInput).then(response => response.text()).then(data => {";
      page += " updateTrafficData();";
        page += "});";
       page += "}";


  // Fonction pour mettre à jour les feux
    page += "function updateLights() {";
  page += "fetch('/getStatus').then(response => response.text()).then(data => {";
  page += "const states = data.split(',');";
  page += "document.getElementById('lightRed1').className = states[0] == '1' ? 'light red' : 'light';";
  page += "document.getElementById('lightOrange1').className = states[1] == '1' ? 'light orange' : 'light';";
  page += "document.getElementById('lightGreen1').className = states[2] == '1' ? 'light green' : 'light';";
  page += "document.getElementById('lightRed2').className = states[3] == '1' ? 'light red' : 'light';";
  page += "document.getElementById('lightOrange2').className = states[4] == '1' ? 'light orange' : 'light';";
  page += "document.getElementById('lightGreen2').className = states[5] == '1' ? 'light green' : 'light';";
  page += "});";
  page += "}";
  // Fonction pour mettre à jour les informations de trafic
    page += "function updateTrafficData() {";
     page += " fetch('/getTrafficData').then(response => response.text()).then(data => {";
       page += "const trafficData = data.split(',');";
           page += "document.getElementById('currentDirection').textContent = trafficData[0];";
      page += "document.getElementById('timeLeft').textContent = trafficData[1];";
         page += "document.getElementById('totalVehicles').textContent = trafficData[2];";
         page += "document.getElementById('way1Vehicles').textContent = trafficData[3];"; // Update way 1 vehicles count
        page += "document.getElementById('way2Vehicles').textContent = trafficData[4];";  // Update way 2 vehicles count
       page += "  document.getElementById('framesBeforeEvaluation').textContent = trafficData[5];";
           page += "document.getElementById('confidenceThreshold').textContent = trafficData[6];";
          page += "document.getElementById('wayWithMoreTraffic').textContent = trafficData[7];";  // Update the way with more traffic
     page += "});";
      page += "}";

  // Mise à jour automatique toutes les 2 secondes
    page += "setInterval(updateLights, 2000);";
      page += "setInterval(updateTrafficData, 2000);";
  page += "updateLights();";  // Mise à jour initiale au chargement
    page += "updateTrafficData();";  // Mise à jour initiale au chargement
  page += "</script>";

  page += "</body></html>";
  server.send(200, "text/html", page);
}

// Fonction appelée lorsque le bouton est pressé
void changeStateHandler() {
  changeState();
  server.send(200, "text/plain", "Etat changé");
}

// Fonction pour obtenir l'état des LEDs sous forme HTML
void getStatusHandler() {
  String status = "";
  status += String(digitalRead(Led_r)) + ",";   // Feu 1 - Rouge
  status += String(digitalRead(Led_o)) + ",";   // Feu 1 - Orange
  status += String(digitalRead(Led_v)) + ",";   // Feu 1 - Vert
  status += String(digitalRead(Led_r2)) + ",";  // Feu 2 - Rouge
  status += String(digitalRead(Led_o2)) + ",";  // Feu 2 - Orange
  status += String(digitalRead(Led_v2));        // Feu 2 - Vert
  server.send(200, "text/plain", status);
}

// Function to handle traffic information from Python script
void handleSetTraffic() {
    if (server.hasArg("direction") && server.hasArg("duration") && server.hasArg("total_vehicles") && server.hasArg("way1_vehicles") && server.hasArg("way2_vehicles"))
    {
        current_traffic_direction = server.arg("direction");
        current_traffic_duration = server.arg("duration").toInt();
        total_vehicles = server.arg("total_vehicles").toInt();
        way1_vehicles = server.arg("way1_vehicles").toInt();
        way2_vehicles = server.arg("way2_vehicles").toInt();

        Serial.print("Traffic info received: ");
        Serial.print("Direction: ");
        Serial.print(current_traffic_direction);
        Serial.print("  Duration: ");
        Serial.print(current_traffic_duration);
        Serial.print("  Total vehicles: ");
        Serial.print(total_vehicles);
        Serial.print("  Way 1 vehicles: ");
        Serial.print(way1_vehicles);
          Serial.print("  Way 2 vehicles: ");
        Serial.println(way2_vehicles);
         server.send(200, "text/plain", "Traffic info received");
     }
    else
     {
       server.send(400, "text/plain", "Invalid parameters");
     }
}

void handleGetTrafficData() {
    String wayWithMoreTraffic = "default"; // Default value
  if (way1_vehicles > way2_vehicles){
      wayWithMoreTraffic = "way1";
  }
   if (way2_vehicles > way1_vehicles){
       wayWithMoreTraffic = "way2";
   }
  String trafficData = "";
  trafficData += current_traffic_direction + ",";
  trafficData += String(interval / 1000) + ",";
    trafficData += String(total_vehicles) + ",";
      trafficData += String(way1_vehicles) + ","; // Added way 1 vehicles to the string
      trafficData += String(way2_vehicles) + ","; // Added way 2 vehicles to the string
      trafficData += String(framesBeforeEvaluation) + ",";
       trafficData += String(confidenceThreshold) + ",";
        trafficData +=  wayWithMoreTraffic; // Added the way with more traffic
  server.send(200, "text/plain", trafficData);
}
void handleSetConfig() {
    if (server.hasArg("duration"))
    {
      current_traffic_duration = server.arg("duration").toInt();
         greenTime = current_traffic_duration*1000;
      redTime = current_traffic_duration*1000;

    }
     if (server.hasArg("confidenceThreshold"))
    {
          confidenceThreshold = server.arg("confidenceThreshold").toFloat();
    }
     server.send(200, "text/plain", "Config set");
}

void handleGetConfig() {
 String config = "";
  config += String(current_traffic_duration) + ",";
     config += String(confidenceThreshold);
  server.send(200, "text/plain", config);
}

// Fonction pour changer l'état des LEDs
void changeState() {
  state = (state + 1) % 4;
  Serial.print("Changement d'état: ");
  Serial.println(state);

   switch (state) {
    case 0:
      // État 1: led_v2 = HIGH pendant 6 secondes
      digitalWrite(Led_v2, HIGH);
      digitalWrite(Led_o2, LOW);
      digitalWrite(Led_r2, LOW);
      digitalWrite(Led_v, LOW);
      digitalWrite(Led_o, LOW);
      digitalWrite(Led_r, HIGH);
       if (current_traffic_direction == "way1")
       {
         interval = current_traffic_duration * 1000; // Convert to milliseconds
       }
       else
       {
          interval = greenTime;
       }
      break;

    case 1:
      // État 2: led_o2 = HIGH et led_v2 = LOW pendant 2 secondes
      digitalWrite(Led_v2, LOW);
      digitalWrite(Led_o2, HIGH);
      digitalWrite(Led_r2, LOW);
      interval = orangeTime;  // 2 secondes
      break;

    case 2:
      // État 3: led_r2 = HIGH et led_v = HIGH pendant 6 secondes
      digitalWrite(Led_v2, LOW);
      digitalWrite(Led_r, LOW);

      digitalWrite(Led_o2, LOW);
      digitalWrite(Led_r2, HIGH);
      digitalWrite(Led_v, HIGH);
     if (current_traffic_direction == "way2")
       {
         interval = current_traffic_duration * 1000; // Convert to milliseconds
       }
       else
       {
          interval = redTime;
       }
      break;

    case 3:
      // État 4: led_o = HIGH, led_r2 = HIGH et led_v = LOW pendant 2 secondes
      digitalWrite(Led_o, HIGH);
      digitalWrite(Led_r2, HIGH);
      digitalWrite(Led_v, LOW);
      interval = orangeTime;  // 2 secondes
      break;
  }
}
