#include <MPU6050.h>
#include <Wire.h>

MPU6050 my_mpu;
byte cur_led = 0;
byte writed = 0;
byte ledPins[] = {9, 10, 11}; // green[9], red[10], blue[11];

void setup() {
  Serial.begin(115200);
  Serial.println("BEGIN");
  while (!my_mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)){
    Serial.print(".");
  }
  Serial.println();
  my_mpu.setGyroOffsetX(0);
  my_mpu.setGyroOffsetY(0);
  my_mpu.setGyroOffsetZ(0);

  my_mpu.calibrateGyro();
  my_mpu.setThreshold(3);

  pinMode(12, INPUT_PULLUP);
  pinMode(8, INPUT_PULLUP);
}

void loop() {
  Vector normGyro = my_mpu.readNormalizeGyro();
  Serial.print(normGyro.XAxis);
  Serial.print(",");
  Serial.print(normGyro.YAxis);
  Serial.print(",");
  Serial.print(normGyro.ZAxis);
  Serial.print(",");
  Serial.print(digitalRead(12));
  Serial.print(",");
  Serial.print(digitalRead(8));
  Serial.println();
  // LED WORK (DIM TO HIGH ANIMATION!)
  analogWrite(ledPins[cur_led], writed);
  if (writed == 255){
    writed = 0;
    analogWrite(ledPins[cur_led], 0);
    if (cur_led == 2){
      cur_led = 0;
    }
    else{
      cur_led+=1;
    }
  }
  writed += 3;
  delay(10);
}
