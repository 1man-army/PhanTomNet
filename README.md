# PhanTomNet

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-Restricted-red)
![Status](https://img.shields.io/badge/Project-Research%20Only-yellow)

PhanTomNet is a modular multi-agent AI framework designed for advanced cybersecurity research, red-team simulations, and educational training. It allows intelligent agents to interact through a centralized logic system, while maintaining isolation and control.

> ⚠️ **Disclaimer:**
> This project is intended strictly for **educational and testing purposes only**.
> Unauthorized deployment, misuse, or targeting of third-party systems is **prohibited** and may lead to legal consequences.
> Use responsibly and within your own controlled environment.

---

## 🎯 Purpose

PhanTomNet is built to simulate how autonomous agents can collaboratively execute a sequence of security or reconnaissance operations. It can be used to:

* Test how AI agents behave in chained operations
* Simulate real-world cyber scenarios in a lab
* Train or benchmark red-team tools in a safe sandbox
* Develop intelligent automation for offensive/defensive research

---

## 🤖 Agents and Components

| Name             | Type   | Description                                                      |
| ---------------- | ------ | ---------------------------------------------------------------- |
| `KeyLoggerX`     | Agent  | Captures keystrokes locally and forwards logs.                   |
| `PhantomLure_AI` | Agent  | Deploys lures/decoys to trap or detect user interactions.        |
| `ReconRaptor`    | Agent  | Scans the host/network and builds a footprint.                   |
| `agent_comm`     | Module | Handles communication (e.g., relay messaging, JSON over socket). |
| `agent_logic`    | Module | Controls execution order, task logic, and runtime policies.      |
| `state_manager`  | Module | Manages and shares runtime state across all agents.              |

---

## 📁 Project Structure

```bash
PhanTomNet/
├── agents/
│   ├── KeyLoggerX/
│   ├── PhantomLure_AI/
│   └── ReconRaptor/
├── agent_comm/
├── agent_logic/
├── state_manager/
├── utils/
├── data/
│   ├── logs/
│   ├── exfil/
│   └── captured/
├── tests/
├── config.yaml
├── requirements.txt
├── run.py
└── README.md
```

---

## ⚙️ Installation

Ensure Python 3.8 or higher is installed.

### 🔹 Install All Requirements (Globally)

```bash
pip install -r requirements.txt
```

### 🔹 Or Per-Agent (Modular Setup)

```bash
pip install -r agents/KeyLoggerX/requirements.txt
pip install -r agents/PhantomLure_AI/requirements.txt
pip install -r agents/ReconRaptor/requirements.txt
```

---

## 🧾 Configuration

Edit `config.yaml` to enable or disable agents, define communication protocols, and control execution logic.

```yaml
KeyLoggerX:
  enabled: true
  interval: 3
  log_path: data/logs/keylog.txt

agent_comm:
  protocol: json
  relay_port: 5555

agent_logic:
  run_order:
    - ReconRaptor
    - PhantomLure_AI
    - KeyLoggerX

state_manager:
  type: file
  path: data/state.json
```

---

## 🚀 Running the System

Start the orchestration engine:

```bash
python run.py
```

This will:

* Load `config.yaml`
* Initialize communication & state
* Execute agents in the defined order

---

## 🔍 Testing

Use provided unit tests:

```bash
pytest tests/
```

---

## 📌 Roadmap (Optional Enhancements)

* [ ] Docker-based deployment
* [ ] GUI-based status dashboard
* [ ] Remote API (Flask/FastAPI)
* [ ] Agent status monitoring + retry logic
* [ ] Plugin support for new agents

---

## 📄 License

This project is **restricted-use** and licensed only for private research, training, and non-commercial academic use.

---

## 🙏 Acknowledgements

Made with ❤️ by Adil Patras, 2025.
Special thanks to the global open-source and security community for inspiration and tools.
