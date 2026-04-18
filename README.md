# Charan-Kande — Gas Exchange System

> **Author:** KANDE BALA GURU CHARAN  
> **Goal:** A closed-loop intelligent system that detects harmful gases, neutralises them, and reuses part of the processed gas stream for propulsion.

---

## 🔷 Core Concept

| Stage | What happens |
|-------|-------------|
| **Intake** | Air is drawn in through a fan/compressor and a pre-filter (dust + moisture) |
| **Detection** | MQ-135 (air quality) and MQ-7 (CO) sensors feed real-time data to an Arduino |
| **Processing** | CO → CO₂ (oxidation catalyst); NOx → N₂ + O₂; SOx captured as solids |
| **CO₂ handling** | Compressed storage → future: algae/chemical conversion |
| **Propulsion** | Processed gases used as compressed thrust (first target: drone) |
| **Output** | Filtered cleaner air released; system receives feedback for next cycle |

---

## 🔷 Development Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| 1 | ✅ **Current** | Gas detection + basic fan purification |
| 2 | 🔲 | Catalytic processing, improved filtering |
| 3 | 🔲 | Drone integration, lightweight build |
| 4 | 🔲 | AI decision-making, pollution prediction (TensorFlow / PyTorch) |
| 5 | 🔲 | Flying suit (long-term / advanced) |

---

## 🔷 Prototype v1.0

### Hardware

| Component | Role |
|-----------|------|
| Arduino Uno R3 | Main controller |
| MQ-135 → A0 | Air quality (CO₂, NH₃, smoke) |
| MQ-7   → A1 | Carbon Monoxide |
| Relay module → D7 | Switches the purification fan |
| 5 V DC Fan | Purification / future propulsion |
| Active Buzzer → D8 | Audible alarm |
| LED → D13 | Visual status |
| LCD 16×2 I²C (optional) → A4/A5 | Real-time display |

### System Flow

```
Air → [Pre-filter] → [MQ-135 / MQ-7] → Arduino
                                           │
                          ┌────────────────┼──────────────────┐
                       CLEAN           MODERATE            DANGER
                      Fan OFF          Fan ON            Fan ON
                                        Beep            Alarm + LED blink
                           └────────────────┼──────────────────┘
                                         Relay
                                           │
                                    Filtered Air OUT
                               (future: propulsion thrust)
```

### Pollution Thresholds (default, tune after calibration)

| Level    | MQ-135 raw | MQ-7 raw |
|----------|-----------|----------|
| MODERATE | ≥ 400     | ≥ 300    |
| DANGER   | ≥ 700     | ≥ 600    |

---

## 🔷 Repository Structure

```
gas_exchange/
├── gas_exchange.ino   ← Full Arduino sketch
└── CIRCUIT.md         ← Wiring guide, ASCII diagram, calibration steps
README.md
```

---

## 🔷 Quick Start

1. Wire components per [`gas_exchange/CIRCUIT.md`](gas_exchange/CIRCUIT.md).
2. Install the `LiquidCrystal_I2C` library in the Arduino IDE  
   *(Sketch → Include Library → Manage Libraries → search "LiquidCrystal I2C")*.
3. Open `gas_exchange/gas_exchange.ino` in the Arduino IDE.
4. If you are **not** using an LCD, set `bool lcdPresent = false;` near the top.
5. Upload to Arduino Uno R3.
6. Open Serial Monitor at **9600 baud** — readings appear after the 60-second warm-up.

---

## 🔷 Future AI Integration

Phase 4 will replace threshold-based logic with a trained model:

- **TensorFlow Lite** running on a Raspberry Pi / ESP32-S3 alongside the sensors.
- Time-series sensor data → multi-class classifier (Clean / Moderate / Danger / Gas type).
- Pollution prediction → proactive fan activation before threshold is crossed.