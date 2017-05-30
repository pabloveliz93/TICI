#define TEMPERATURE_PIN 3//Se declara el pin donde se conectará la DATA
#define PING_PIN 2 //Pin para sensor volumen
#define FLUX_PIN 0 //Pin para sensor de flujo
#define VOL_SETUP_CODE 9999 // El identificador de datos de SETUP de volumen
#define VOL_CODE 9997 // El identificador de datos de volumen
#define TEMP_CODE 9998 //El identificador de datos de temperatura
#define FLUX_CODE 9996 //El identificador de datos de flujo
#define END_CODE -1.0 //Indica que ha finalizado el envío de un burst de datos

#include <NewPing.h> //Para sensor de volumen
NewPing sonar(PING_PIN, PING_PIN );

#include <OneWire.h> //Para sensor de temperatura
#include <DallasTemperature.h>
OneWire ourWire(TEMPERATURE_PIN);
DallasTemperature sensors(&ourWire);

void setup(){
  Serial.begin(9600);          //  setup serial
  sensors.begin();             //  setup sensor de temperatura
}
void loop(){
    short int code;
    int k = Serial.available();
    if (k > 0) {
      if (k == 4){
        code = get_incomming_code_4();
      }
    switch (code){
      case FLUX_CODE:
        //for (int i = 0; i < 100; i ++){
        int flux = analogRead(FLUX_PIN);
        Serial.println(flux);
        delay(100);
        //}
      break;
      case VOL_CODE:
        //for (int i = 0; i < 100; i ++){
        float uS = sonar.ping();
        Serial.println((float)(uS / US_ROUNDTRIP_CM));
        delay(100);
        //}
      break;
      case VOL_SETUP_CODE:
        for (int i = 0; i <10; i++){
          float uS = sonar.ping();
          Serial.println((float)(uS / US_ROUNDTRIP_CM));
          delay(100);
        }
        //Al final enviamos -1 para indicar que se ha terminado el envío de datos
        Serial.println(END_CODE);
      break;
      case TEMP_CODE:
        sensors.requestTemperatures(); //Prepara el sensor para la lectura
        Serial.println(sensors.getTempCByIndex(0)); //Se lee e imprime la temperatura en grados Celsius
        delay(1000);
      break;
    }
  }
}

int get_incomming_code_4(){
  char incommingcode[4];
  for (int i = 0; i < 4; ++i) incommingcode[i] = Serial.read();
  return atoi(incommingcode);
}
