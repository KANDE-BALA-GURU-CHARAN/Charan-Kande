/*
 * ============================================================
 *  GAS EXCHANGE SYSTEM — Prototype v1.0
 *  Author : KANDE BALA GURU CHARAN
 *  Target : Arduino Uno R3
 *
 *  Sensors
 *    MQ-135  → A0  (CO₂ / NH₃ / smoke — general air quality)
 *    MQ-7    → A1  (Carbon Monoxide)
 *
 *  Outputs
 *    Relay (fan)   → D7
 *    Buzzer alert  → D8
 *    Status LED    → D13
 *
 *  Optional I²C LCD 16×2
 *    SDA → A4   SCL → A5
 *
 *  Logic overview
 *  ──────────────
 *  • Read both sensors every SAMPLE_INTERVAL ms.
 *  • Map raw ADC values to approximate PPM levels.
 *  • Determine pollution level: CLEAN / MODERATE / DANGER.
 *  • CLEAN    → fan OFF, no alert.
 *  • MODERATE → fan ON (purification), short beep.
 *  • DANGER   → fan ON at max, continuous alarm, LED blink.
 *  • Serial monitor prints real-time data (9600 baud).
 * ============================================================
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>    // remove if not using LCD

// ── Pin definitions ──────────────────────────────────────────
#define MQ135_PIN   A0
#define MQ7_PIN     A1
#define RELAY_PIN   7
#define BUZZER_PIN  8
#define LED_PIN     13

// ── Thresholds (tune after sensor warm-up calibration) ───────
// MQ-135 raw ADC thresholds (0-1023)
#define AQ_MODERATE_THRESHOLD   400   // above → moderate pollution
#define AQ_DANGER_THRESHOLD     700   // above → dangerous

// MQ-7 raw ADC thresholds (0-1023)
#define CO_MODERATE_THRESHOLD   300   // ~50 ppm CO (approx)
#define CO_DANGER_THRESHOLD     600   // ~100 ppm CO (approx)

// ── Timing ───────────────────────────────────────────────────
#define SAMPLE_INTERVAL   2000   // ms between readings
#define WARMUP_TIME      60000   // 60-second sensor warm-up

// ── LCD (optional — comment out if not used) ─────────────────
LiquidCrystal_I2C lcd(0x27, 16, 2);  // I²C address 0x27
bool lcdPresent = true;              // set false to disable LCD

// ── Pollution level enum ──────────────────────────────────────
enum PollutionLevel { CLEAN, MODERATE, DANGER };

// ── Global state ─────────────────────────────────────────────
unsigned long lastSampleTime = 0;
PollutionLevel currentLevel  = CLEAN;
bool fanRunning = false;

// ─────────────────────────────────────────────────────────────
//  Helper: map raw ADC value to approximate PPM for MQ-135
//  (simplified linear approximation — replace with datasheet
//   RS/RO curve for better accuracy)
// ─────────────────────────────────────────────────────────────
float rawToPPM_MQ135(int raw) {
    // Vout rises with pollution; rough linear mapping
    return map(raw, 0, 1023, 0, 10000);  // 0–10 000 ppm scale
}

float rawToPPM_MQ7(int raw) {
    // MQ-7: 10–10 000 ppm CO range on datasheet
    return map(raw, 0, 1023, 0, 10000);
}

// ─────────────────────────────────────────────────────────────
//  Helper: compute overall pollution level from both sensors
// ─────────────────────────────────────────────────────────────
PollutionLevel computeLevel(int aqRaw, int coRaw) {
    if (aqRaw >= AQ_DANGER_THRESHOLD || coRaw >= CO_DANGER_THRESHOLD) {
        return DANGER;
    }
    if (aqRaw >= AQ_MODERATE_THRESHOLD || coRaw >= CO_MODERATE_THRESHOLD) {
        return MODERATE;
    }
    return CLEAN;
}

// ─────────────────────────────────────────────────────────────
//  Helper: LCD status line
// ─────────────────────────────────────────────────────────────
void updateLCD(int aqRaw, int coRaw, PollutionLevel level) {
    if (!lcdPresent) return;

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("AQ:");
    lcd.print(aqRaw);
    lcd.print(" CO:");
    lcd.print(coRaw);

    lcd.setCursor(0, 1);
    if (level == CLEAN)    lcd.print("Status: CLEAN   ");
    if (level == MODERATE) lcd.print("Status: MODERATE");
    if (level == DANGER)   lcd.print("Status: DANGER! ");
}

// ─────────────────────────────────────────────────────────────
//  Helper: actuate fan relay
// ─────────────────────────────────────────────────────────────
void setFan(bool on) {
    if (on == fanRunning) return;  // no change
    fanRunning = on;
    digitalWrite(RELAY_PIN, on ? HIGH : LOW);
}

// ─────────────────────────────────────────────────────────────
//  Helper: buzzer patterns
// ─────────────────────────────────────────────────────────────
void beepShort() {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);
    digitalWrite(BUZZER_PIN, LOW);
}

void beepAlarm() {
    // Three rapid pulses for danger
    for (int i = 0; i < 3; i++) {
        digitalWrite(BUZZER_PIN, HIGH);
        delay(100);
        digitalWrite(BUZZER_PIN, LOW);
        delay(100);
    }
}

// ─────────────────────────────────────────────────────────────
//  Helper: LED blink (non-blocking via millis)
// ─────────────────────────────────────────────────────────────
void updateLED(PollutionLevel level) {
    static unsigned long lastBlink = 0;
    static bool ledState = false;

    if (level == DANGER) {
        if (millis() - lastBlink >= 300) {
            lastBlink = millis();
            ledState = !ledState;
            digitalWrite(LED_PIN, ledState ? HIGH : LOW);
        }
    } else {
        // Solid on while fan is running, off when clean
        digitalWrite(LED_PIN, (level == MODERATE) ? HIGH : LOW);
    }
}

// ─────────────────────────────────────────────────────────────
//  SETUP
// ─────────────────────────────────────────────────────────────
void setup() {
    Serial.begin(9600);

    pinMode(RELAY_PIN,  OUTPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(LED_PIN,    OUTPUT);

    // Safe defaults
    digitalWrite(RELAY_PIN,  LOW);
    digitalWrite(BUZZER_PIN, LOW);
    digitalWrite(LED_PIN,    LOW);

    // Optional LCD init
    if (lcdPresent) {
        lcd.begin(16, 2);
        lcd.backlight();
        lcd.setCursor(0, 0);
        lcd.print("Gas Exchange v1 ");
        lcd.setCursor(0, 1);
        lcd.print("Warming up...   ");
    }

    // ── Sensor warm-up ──────────────────────────────────────
    Serial.println(F("=== GAS EXCHANGE SYSTEM v1.0 ==="));
    Serial.println(F("Warming up sensors (60 s)..."));

    unsigned long warmupStart = millis();
    while (millis() - warmupStart < WARMUP_TIME) {
        // Blink LED slowly during warm-up
        unsigned long elapsed = millis() - warmupStart;
        digitalWrite(LED_PIN, (elapsed / 500) % 2 == 0 ? HIGH : LOW);
        delay(100);

        // Print countdown every 10 s
        if (elapsed % 10000 < 100) {
            Serial.print(F("Warm-up: "));
            Serial.print((WARMUP_TIME - elapsed) / 1000);
            Serial.println(F(" s remaining"));
        }
    }

    digitalWrite(LED_PIN, LOW);
    Serial.println(F("Warm-up complete. System ready."));
    Serial.println(F("---------------------------------------"));
    Serial.println(F("Time(ms) | AQ_raw | CO_raw | Level"));
    Serial.println(F("---------------------------------------"));

    if (lcdPresent) {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("System Ready!   ");
    }
}

// ─────────────────────────────────────────────────────────────
//  MAIN LOOP
// ─────────────────────────────────────────────────────────────
void loop() {
    unsigned long now = millis();

    // ── Non-blocking LED update ──────────────────────────────
    updateLED(currentLevel);

    // ── Sample sensors every SAMPLE_INTERVAL ms ─────────────
    if (now - lastSampleTime >= SAMPLE_INTERVAL) {
        lastSampleTime = now;

        int aqRaw = analogRead(MQ135_PIN);
        int coRaw = analogRead(MQ7_PIN);

        currentLevel = computeLevel(aqRaw, coRaw);

        // ── Serial output ────────────────────────────────────
        Serial.print(now);
        Serial.print(F(" ms | AQ="));
        Serial.print(aqRaw);
        Serial.print(F(" (≈"));
        Serial.print(rawToPPM_MQ135(aqRaw));
        Serial.print(F(" ppm) | CO="));
        Serial.print(coRaw);
        Serial.print(F(" (≈"));
        Serial.print(rawToPPM_MQ7(coRaw));
        Serial.print(F(" ppm) | "));

        // ── Act on pollution level ───────────────────────────
        switch (currentLevel) {

            case CLEAN:
                Serial.println(F("CLEAN — fan OFF"));
                setFan(false);
                break;

            case MODERATE:
                Serial.println(F("MODERATE — fan ON"));
                setFan(true);
                beepShort();
                break;

            case DANGER:
                Serial.println(F("DANGER — fan ON, ALARM!"));
                setFan(true);
                beepAlarm();
                break;
        }

        // ── LCD update ───────────────────────────────────────
        updateLCD(aqRaw, coRaw, currentLevel);
    }
}
