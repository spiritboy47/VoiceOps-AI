# 🎙️ VoiceOps AI – Voice Enabled Infrastructure Monitoring

VoiceOps AI is a **voice-controlled DevOps monitoring dashboard** that allows users to query infrastructure metrics using **natural language or voice commands**.

The system integrates with **Prometheus** to retrieve real-time server metrics such as **CPU, Memory, and Disk usage**, and presents them in an interactive dashboard with chat-style responses and voice feedback.

---

## 🚀 Features

* 🎙️ Voice commands for querying infrastructure metrics
* 💬 Chat-style DevOps interaction interface
* 📊 Real-time CPU, Memory, and Disk monitoring
* 🧠 Intent-based command processing
* 🔐 Session-based authentication
* ⚠️ Built-in alert monitoring with cooldown suppression
* 🔊 Text-to-speech responses
* 🌐 Web dashboard interface

---

## 🏗️ Architecture

```
User (Voice / Text Command)
            │
            ▼
VoiceOps Dashboard (HTML + JS)
            │
            ▼
FastAPI Backend
            │
 ┌──────────┼──────────┐
 ▼          ▼          ▼
Auth      Intent     Alert
System    Engine     Engine
            │
            ▼
     Prometheus Client
            │
            ▼
        Prometheus
            │
            ▼
     Server Exporters
   (node_exporter / windows_exporter)
```

---

## 🔄 Request Flow

1. User sends a **voice or text command** from the dashboard.

Example:

```
qa cpu
prod memory
dev disk
```

2. The frontend sends a request to the API:

```
POST /api/chat
```

3. The **Intent Engine** processes the command and determines:

* Target Server (DEV / QA / UAT / PROD)
* Requested Metric (CPU / Memory / Disk)

4. The system selects the appropriate **PromQL query**.

5. The **Prometheus Client** queries Prometheus:

```
/api/v1/query
```

6. The metric value is returned to the dashboard and displayed.

7. The system also speaks the response using **Text-to-Speech**.

---

## ⚠️ Alert Monitoring

VoiceOps AI includes a lightweight alert monitoring system.

The alert engine:

* Periodically checks server metrics
* Detects high resource usage
* Sends alerts to the dashboard

Example alerts:

```
⚠️ QA-SERVER CPU usage is 86%
⚠️ PROD-SERVER Memory usage is 92%
```

### Alert Suppression

To prevent alert spam, alerts use a **cooldown mechanism**:

```
Cooldown: 180 seconds
```

If an alert is triggered, it will not trigger again for 3 minutes.

---

## 📁 Project Structure

```
VoiceOps-AI
│
├── app
│   ├── routers
│   │   └── api.py
│   │
│   ├── static
│   │   ├── style.css
│   │   └── voice.js
│   │
│   ├── templates
│   │   ├── dashboard.html
│   │   └── login.html
│   │
│   ├── auth.py
│   ├── intent_engine.py
│   ├── alert_engine.py
│   ├── prometheus_client.py
│   └── config.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## 📄 File Responsibilities

### `main.py`

Initializes the **FastAPI application**, handles:

* Authentication routes
* Dashboard rendering
* Middleware for session protection
* API router mounting

---

### `auth.py`

Authentication module responsible for:

* Creating session cookies
* Verifying user sessions
* Handling login authentication

Uses signed cookies via `itsdangerous`.

---

### `routers/api.py`

API endpoints used by the frontend.

Endpoints:

```
POST /api/chat
GET  /api/alerts
```

---

### `intent_engine.py`

Processes user commands and converts them into monitoring queries.

Responsibilities:

* Detect server environment
* Detect requested metric
* Select correct Prometheus query
* Return formatted response

---

### `prometheus_client.py`

Handles communication with **Prometheus**.

Responsibilities:

* Send PromQL queries
* Parse API responses
* Return metric values

---

### `alert_engine.py`

Implements the alert monitoring system.

Responsibilities:

* Check server metrics
* Detect threshold breaches
* Generate alerts
* Suppress repeated alerts

---

### `voice.js`

Frontend logic responsible for:

* Voice recognition
* Sending API requests
* Updating dashboard metrics
* Speaking responses
* Displaying alerts

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```
git clone https://github.com/yourusername/voiceops-ai.git
cd voiceops-ai
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv venv
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment

Update `config.py`:

```
SECRET_KEY = "your-secret-key"

USERNAME = "admin"
PASSWORD = "admin123"

SERVER_PROMETHEUS_MAPPING = {
    "DEV-SERVER": "http://dev-prometheus:9090",
    "QA-SERVER": "http://qa-prometheus:9090",
    "UAT-SERVER": "http://uat-prometheus:9090",
    "PROD-SERVER": "http://prod-prometheus:9090"
}
```

---

### 5️⃣ Run Application

```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Application will run at:

```
http://localhost:8000
```

---

## 🖥️ Dashboard Example

Commands supported:

```
dev cpu
qa memory
prod disk
```

Dashboard shows:

* Live metric values
* Chat conversation
* Voice responses
* Alert notifications

---

## 🛠️ Technologies Used

* Python
* FastAPI
* Prometheus
* HTML / CSS / JavaScript
* Web Speech API
* Text-to-Speech API

---

## 🎯 Use Cases

* DevOps infrastructure monitoring
* Voice-driven operational dashboards
* Learning Prometheus integration
* Demonstrating AI-assisted DevOps tools

---

## 📌 Future Improvements

Possible enhancements:

* WebSocket-based real-time alerts
* Historical metric graphs
* Kubernetes cluster monitoring
* Natural language processing for complex queries
* Multi-user authentication system

---

## 👨‍💻 Author

**Nikhil Kumar**

DevOps / Cloud / Infrastructure Monitoring Enthusiast

---

## 📜 License

This project is open-source and available under the MIT License.
