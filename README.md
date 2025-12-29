````markdown
# Intelligent IoT Honeypot for Threat Analysis 🍯🛡️

A low-interaction honeypot designed to emulate vulnerable IoT devices (Telnet), capture attacker traffic, and analyze threats using Machine Learning. This system goes beyond simple logging by automatically classifying attack intent (e.g., **Malware Download**, **Reconnaissance**, **Destruction**) using a **Naive Bayes classifier**.

---

## 🚀 Features

- **Decoy Service**  
  Emulates a Telnet service on **Port 9999** to attract botnets.

- **Intelligent Logging**  
  Captures IP addresses, timestamps, credentials, and raw shell commands.

- **ML-Powered Analysis**  
  Uses **Scikit-Learn (Naive Bayes)** to classify attacks based on command patterns.

- **Interactive Dashboard**  
  A **Flask-based web interface** with real-time charts (Chart.js) and forensic details.

- **Simulation Suite**  
  Includes a script to simulate a **20-node botnet attack** for demonstration purposes.

---

## 🛠️ Prerequisites

Ensure you have **Python 3.10+** installed.  
You will need the following libraries:

```bash
pip install flask pandas scikit-learn
````

---

## 📂 Project Structure

```
Intelligent-IoT-Honeypot/
│
├── honeypot.py           # The "Sensor": Listens for connections
├── simulate_attack.py    # The "Attacker": Simulates a botnet
├── analyzer.py           # The "Brain": Processes logs & runs ML
├── ml_engine.py          # The "AI": Naive Bayes Classification logic
├── dashboard.py          # The "Face": Flask Web Server
├── run_project.bat       # Automation Script for Windows
│
├── templates/
│   └── index.html        # Dashboard HTML Template
│
└── dashboard_data/       # Generated JSON files (created at runtime)
```

---

## ⚡ How to Run (Two Methods)

### Method 1: The Automated Way (Recommended for Demos) 🌟

A Windows Batch script (`run_project.bat`) automatically launches all components in separate terminal windows with correct timing.

1. Double-click `run_project.bat`
2. It will:

   * Open the **Honeypot (Sensor)**
   * Wait 2 seconds, then launch the **Attack Simulation**
   * Wait for the attack to finish, then run the **Analyzer**
   * Finally, launch the **Web Dashboard**

A browser window should open automatically at:
**[http://127.0.0.1:8080](http://127.0.0.1:8080)**

---

### Method 2: The Manual Way (Step-by-Step)

If you are on Linux/Mac or want full visibility, run the following in separate terminals.

#### Step 1: Start the Honeypot

Starts the listener on **Port 9999**.

```bash
python honeypot.py
```

#### Step 2: Launch the Attack

Run the simulation in a new terminal. Connection logs will appear in the honeypot window.

```bash
python simulate_attack.py
```

#### Step 3: Analyze the Data

Processes `honeypot_log.json`, trains the ML model, and generates statistics.

```bash
python analyzer.py
```

#### Step 4: Start the Dashboard

Launch the web server.

```bash
python dashboard.py
```

Visit: **[http://127.0.0.1:8080](http://127.0.0.1:8080)**

---

## 🤖 About the ML Engine

The system uses a **Multinomial Naive Bayes classifier** trained on a dictionary of common IoT attack commands.

* **Reconnaissance**
  `cat /proc/cpuinfo`, `uname -a`, `whoami`

* **Malware Download**
  `wget`, `curl`, `tftp`

* **Destruction**
  `rm -rf`, `mkfs.ext4`

The `ml_engine.py` vectorizes these commands using **Bag of Words** to predict the intent of new, unseen commands during an attack.

---

## 👥 Contributors

* **Atharv Bhosale** (Roll No. 74)
* **Girish Desai** (Roll No. 66)

**Department of Computer Science & Engineering (AIML)**
**KIT's College of Engineering, Kolhapur**

```
```
