# Gas Exchange System — Circuit Wiring Guide (Prototype v1.0)

## Components

| Qty | Component              | Notes                              |
|-----|------------------------|------------------------------------|
| 1   | Arduino Uno R3         | Microcontroller                    |
| 1   | MQ-135 Gas Sensor      | Air quality (CO₂, NH₃, smoke)      |
| 1   | MQ-7 Gas Sensor        | Carbon Monoxide                    |
| 1   | 5 V Relay Module       | Single-channel, active-HIGH        |
| 1   | 5 V DC Fan             | Purification / propulsion          |
| 1   | Buzzer (active, 5 V)   | Audible alarm                      |
| 1   | LED + 220 Ω resistor   | Status indicator (or use D13 LED)  |
| 1   | LCD 16×2 I²C (opt.)    | Real-time display                  |
| 1   | Breadboard             | Prototyping                        |
| —   | Jumper wires           |                                    |
| 1   | 9 V battery / adapter  | Arduino power source               |

---

## Wiring Table

### MQ-135 (Air Quality Sensor) → A0

| MQ-135 Pin | Arduino Pin |
|------------|-------------|
| VCC        | 5V          |
| GND        | GND         |
| AOUT       | A0          |
| DOUT       | *(not used in this sketch)* |

### MQ-7 (CO Sensor) → A1

| MQ-7 Pin | Arduino Pin |
|----------|-------------|
| VCC      | 5V          |
| GND      | GND         |
| AOUT     | A1          |
| DOUT     | *(not used in this sketch)* |

### Relay Module → D7

| Relay Pin | Arduino Pin |
|-----------|-------------|
| VCC       | 5V          |
| GND       | GND         |
| IN        | D7          |
| COM       | Fan+ (power rail) |
| NO        | Fan power wire    |

> **Fan wiring:** Connect the fan's positive lead through the relay's NO–COM contacts.  
> The fan's negative lead goes to GND of the power supply.  
> Use a separate 5 V supply for the fan if the fan draws more than 500 mA.

### Buzzer → D8

| Buzzer Pin | Arduino Pin |
|------------|-------------|
| +          | D8          |
| −          | GND         |

### Status LED → D13

Built-in LED on Arduino Uno is on D13. No external LED needed unless preferred.  
If adding an external LED: connect **Anode → 220 Ω resistor → D13**, **Cathode → GND**.

### LCD 16×2 (I²C, optional) → A4 / A5

| LCD I²C Pin | Arduino Pin |
|-------------|-------------|
| VCC         | 5V          |
| GND         | GND         |
| SDA         | A4          |
| SCL         | A5          |

---

## ASCII Circuit Overview

```
                          ┌────────────────────────┐
                          │      Arduino Uno R3     │
                          │                         │
  MQ-135 ──── AOUT ──────►│ A0                      │
  MQ-7   ──── AOUT ──────►│ A1                      │
                          │                         │
                          │ D7 ──────────────────── ► Relay IN
                          │ D8 ──────────────────── ► Buzzer +
                          │ D13 ─────────────────── ► LED (built-in)
                          │                         │
                          │ A4 (SDA) ───────────── ► LCD SDA
                          │ A5 (SCL) ───────────── ► LCD SCL
                          │                         │
                          │ 5V ──── VCC (all)        │
                          │ GND ─── GND (all)        │
                          └────────────────────────┘

  Relay:   COM ──► Fan(+) ──► Fan motor ──► GND(power supply)
           NO  ──► (open until relay triggers)
```

---

## Power Notes

- Arduino can power both MQ sensors and the relay module coil from its 5 V rail.
- The fan motor should ideally be powered from a **separate 5 V / 1 A supply** to avoid
  brown-outs on the Arduino. Share a common GND.
- Use a 9 V barrel adapter (or USB) to power the Arduino.

---

## Breadboard Layout Tips

1. Use the breadboard's power rails (+/−) for distributing 5 V and GND.
2. Place MQ-135 and MQ-7 at opposite ends to minimise cross-contamination of heat.
3. Keep the relay module away from the sensor area to reduce electrical noise.
4. Add a 100 nF ceramic capacitor across each sensor's VCC–GND pins to filter noise.

---

## Calibration

Both MQ sensors need a **60-second warm-up** (handled in `setup()`).  
For accurate PPM readings, perform a clean-air calibration:

1. Power the system in clean outdoor air for 10 minutes.
2. Note the ADC values (`AQ_raw`, `CO_raw`) printed on Serial Monitor.
3. Those values become your **baseline (R0)**.
4. Adjust `AQ_MODERATE_THRESHOLD`, `AQ_DANGER_THRESHOLD`,
   `CO_MODERATE_THRESHOLD`, `CO_DANGER_THRESHOLD` in `gas_exchange.ino`
   relative to that baseline.

---

## System Flow

```
Air IN
  │
  ▼
[Pre-filter: dust/moisture]
  │
  ▼
[MQ-135 + MQ-7 Sensors]  ──► Arduino reads analog values
  │                              │
  │                              ▼
  │                     Compute pollution level
  │                     CLEAN / MODERATE / DANGER
  │                              │
  │              ┌───────────────┼──────────────────┐
  │           CLEAN           MODERATE            DANGER
  │          Fan OFF          Fan ON            Fan ON
  │                           Beep              Alarm
  │                           LED ON            LED blink
  ▼
[Fan / Relay]
  │
  ▼
Processed / filtered air OUT  →  (future: propulsion thrust)
```

---

## Library Dependencies (Arduino IDE)

Install via **Sketch → Include Library → Manage Libraries**:

| Library                  | Purpose          |
|--------------------------|------------------|
| `LiquidCrystal_I2C`      | LCD via I²C bus  |
| `Wire` (built-in)        | I²C communication|

If you are **not** using the LCD, remove the `#include` lines at the top of
`gas_exchange.ino` and set `lcdPresent = false`.
