#include <OneWire.h> //Se importan las librerías
#include <DallasTemperature.h>
 
#define TEMPERATURE_PIN 3//Se declara el pin donde se conectará la DATA
#define VOL_CODE 9999 // El identificador de datos de volumen
#define TEMP_CODE 9998 //El identificador de datos de temperatura
#define END_CODE -1.0 //Indica que ha finalizado el envío de un burst de datos
const int pingPin = 2;

//Necesario para sensor de temperatura
OneWire ourWire(TEMPERATURE_PIN); //Se establece el pin declarado como bus para la comunicación OneWire
DallasTemperature sensors(&ourWire);


void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  sensors.begin();
}

void loop() {
  
  long duration, inches;
  float cm;
  short int identifier_code; //Codigo identificador
  int k = Serial.available();
  if (k > 0) {
    if (k == 4){
      identifier_code = get_incomming_code_4();
    }
    //Serial.print(identifier_code);
    if (identifier_code == VOL_CODE){
      //Serial.print(VOL_CODE);
      //Serial.println();
      for (int i = 0; i <10; i++){
        pinMode(pingPin, OUTPUT);
        digitalWrite(pingPin, LOW);
        delayMicroseconds(2);
        digitalWrite(pingPin, HIGH);
        delayMicroseconds(5);
        digitalWrite(pingPin, LOW);
        pinMode(pingPin, INPUT);
        duration = pulseIn(pingPin, HIGH);
      
        //inches = microsecondsToInches(duration);
        cm = microsecondsToCentimeters(duration);
      
        Serial.print(cm);
        Serial.println();
      
        delay(100);
      }
    //Al final enviamos -1 para indicar que se ha terminado el envío de datos
    Serial.print(END_CODE);
    Serial.println();
    }
  if (identifier_code == TEMP_CODE){
    sensors.requestTemperatures(); //Prepara el sensor para la lectura
    //Serial.print(TEMP_CODE);
    //Serial.println();
    Serial.print(sensors.getTempCByIndex(0)); //Se lee e imprime la temperatura en grados Celsius
    Serial.println();
    //Serial.print(sensors.getTempFByIndex(0)); //Se lee e imprime la temperatura en grados Fahrenheit
    //Serial.println(" grados Fahrenheit"); 
    delay(1000);
  }
  }
}

float microsecondsToCentimeters(float microseconds) {
  return microseconds / 29.0 / 2.0;
}

int get_incomming_code_4(){
  char incommingcode[4];
  for (int i = 0; i < 4; ++i) incommingcode[i] = Serial.read();
  return atoi(incommingcode);
}

