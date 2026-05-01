#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

#define MQ135_PIN        34
#define SAMPLE_COUNT     10
#define READ_INTERVAL_MS 2000
#define BASELINE_SAMPLES 50   // Number of readings for calibration

Adafruit_BMP280 bmp;

float temperature, pressure;
int gasValue;
float BASELINE_GAS = 0;

// =========================
// 📌 Read averaged gas
// =========================
int readGasAverage() {
  long sum = 0;
  for (int i = 0; i < SAMPLE_COUNT; i++) {
    sum += analogRead(MQ135_PIN);
    delay(10);
  }
  return (int)(sum / SAMPLE_COUNT);
}

// =========================
// 📌 Auto baseline calibration
// =========================
void calibrateBaseline() {
  Serial.println("\n🔄 Calibrating baseline... Keep sensor in clean air");

  long sum = 0;

  for (int i = 0; i < BASELINE_SAMPLES; i++) {
    int val = readGasAverage();
    sum += val;

    Serial.print("Reading ");
    Serial.print(i + 1);
    Serial.print(": ");
    Serial.println(val);

    delay(200);
  }

  BASELINE_GAS = sum / BASELINE_SAMPLES;

  Serial.println("\n✅ Baseline calibration complete!");
  Serial.print("Baseline Gas Value: ");
  Serial.println(BASELINE_GAS);
  Serial.println("====================================\n");
}

// =========================
// 📌 Setup
// =========================
void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);

  bool status = bmp.begin(0x76);
  if (!status) status = bmp.begin(0x77);
  if (!status) {
    Serial.println("[ERROR] BMP280 not found!");
    while (1);
  }

  Serial.println("[OK] BMP280 ready");

  delay(3000);  // allow MQ135 to stabilize

  calibrateBaseline();   // 🔥 AUTO BASELINE HERE
}

// =========================
// 📌 Loop
// =========================
void loop() {

  temperature = bmp.readTemperature();
  pressure    = bmp.readPressure() / 100.0F;
  gasValue    = readGasAverage();

  int delta = gasValue - BASELINE_GAS;

  Serial.print(temperature, 2); Serial.print(",");
  Serial.print(pressure, 2); Serial.print(",");
  Serial.print(gasValue); Serial.print(",");
  Serial.println(delta);

  delay(READ_INTERVAL_MS);
}