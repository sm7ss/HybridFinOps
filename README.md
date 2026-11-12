# HybridFinOps 🐥🌵

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20S3%20%7C%20CloudWatch-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![boto3](https://img.shields.io/badge/boto3-SDK-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.0%2B-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 🌵 **A local-first data pipeline and AWS cost-monitoring bot inspired by Pablo the Cactus.**
> Prevents cloud billing surprises by automating server shutdowns.

> ⚠️ **PROJECT IN ACTIVE DEVELOPMENT (WIP)**
> This repository documents the design and architecture of a local-first FinOps bot that monitors AWS costs, detects idle servers, and automates shutdown decisions via Telegram.

---

## 🎯 The Problem

AWS bills can surprise you. An idle EC2 instance running 24/7 costs money for nothing.

HybridFinOps solves this by:
- Detecting idle servers (via CloudWatch metrics)
- Notifying you through Telegram
- Letting you decide: **shutdown**, **postpone**, or **keep running**
- Automatically shutting down if you don't respond in time
- Tracking budget usage in real time
- Running a hybrid ML pipeline (S3 -> local -> cloud training)

✅ **Local-first**: your data and credentials stay on your machine.
✅ **Minimal IAM permissions**: the bot can only start/stop EC2 and read/write S3.
✅ **Traceable**: every decision is logged.

---

## 📍 Project Status

| Component                          | Status           | What it does                                                     |
|------------------------------------|------------------|------------------------------------------------------------------|
| **Config (YAML + Pydantic)**       | ✅ Completed     | Budget limits, inactivity thresholds, postpone rules             |
| **Telegram Bot**                   | 🚧 In development| TBD (aiogram or python-telegram-bot)                             |
| **AWS Connection (boto3)**         | 🚧 In development| EC2 start/stop, S3 read/write                                    |
| **CloudWatch Integration**         | 📝 Planned       | Idle detection (CPU, Network In/Out)                             |
| **Lambda Auto-Check**              | 📝 Planned       | Runs every X minutes without needing your PC on 24/7             |
| **Auto-Shutdown**                  | 🚧 In development| Shutdown on budget hit or no response                            |
| **Budget Monitoring**              | 🚧 In development| Alerts and cost calculations                                     |
| **Logging**                        | 🚧 In development| Full activity traceability                                       |
| **Hybrid ML Pipeline**             | 📝 Planned       | S3 sample -> local processing -> cloud training -> saved model      |
| **IAM Minimal Permissions**        | 🚧 In development       | Least-privilege role (EC2 + S3 only)                             |

> 🐥 **Currently:** config + validation are ready. Bot and AWS integration are in progress.

---

## 🔄 Bot Flows

### Flow A — Idle Server Detected

When CloudWatch/Lambda detects inactivity for X minutes (configured in `config.yaml`), the bot sends a notification with 3 options:

| Option         | Action                                                                 |
|----------------|------------------------------------------------------------------------|
| **Shutdown**   | Stops the EC2 instance                                                 |
| **Postpone**   | Postpones X minutes, calculates cost for that time, asks for confirmation |
| **Keep**       | Shows cost estimates (1h, 4h, 8h, 12h, 24h) and asks for confirmation  |
| *(No response)*| Automatically shuts down after X minutes                               |

### Flow B — Budget Limit Reached

When the budget limit is hit, the bot sends a notification with 3 options:

| Option               | Action                                                        |
|----------------------|---------------------------------------------------------------|
| **Shutdown**         | Stops the server and saves ongoing operations                 |
| **Postpone**         | Same logic as Flow A (with cost calculation + confirmation)   |
| **Keep until done**  | Waits for the operation to finish, then reports total cost    |

> 🐥 Every decision is logged for traceability.

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                          USER (Telegram)                        │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TELEGRAM BOT (Python)                        │
│           (aiogram or python-telegram-bot — TBD)                │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AWS (via boto3)                            │
│  ┌──────────┐  ┌──────────┐  ┌─────────────┐  ┌────────────┐    │
│  │   EC2    │  │    S3    │  │  CloudWatch │  │    IAM     │    │
│  │ (server) │  │ (data)   │  │  (metrics)  │  │ (min perms)│    │
│  └──────────┘  └──────────┘  └─────────────┘  └────────────┘    │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   HYBRID ML PIPELINE                            │
│  S3 sample -> local processing -> cloud training -> saved model    │
└─────────────────────────────────────────────────────────────────┘
```

### 🧩 Why "Hybrid"?

- **Data lives in S3** (cheap, scalable)
- **Processing happens locally** (privacy, control)
- **Training happens in the cloud** (compute power)
- **The trained model is saved** for later use

---

## ⚙️ Configuration

### [config.yaml](/config/config.yaml)

```yaml
budget: # USD
  limit_budget: 1.0
  minimum_budget: 1.0

times: # Minutes
  time_limit_of_inactive_server: 1
  minimum_time_to_postpone: 1
  maximum_time_to_postpone: 1
```

| Field                           | Description                                         |
|---------------------------------|-----------------------------------------------------|
| `limit_budget`                  | Maximum budget in USD before triggering alerts      |
| `minimum_budget`                | Minimum budget to keep the server running           |
| `time_limit_of_inactive_server` | Minutes of inactivity before the bot sends an alert |
| `minimum_time_to_postpone`      | Minimum minutes to postpone shutdown                |
| `maximum_time_to_postpone`      | Maximum minutes to postpone shutdown                |

> 🐥 All values are validated with Pydantic.

---

## 🛠️ Tech Stack

| Tool / Library	                | Purpose                                                      |
|-----------------------------------|--------------------------------------------------------------|
| **Python 3.10+**                  | Base language                                                |
| **Telegram BotFather** 	        | Bot creation and token generation                            |
| **aiogram / python-telegram-bot** |	Telegram bot framework (TBD — aiogram preferred for async) |
| **AWS EC2**	                    | ML training server (start/stop target)                       |
| **AWS S3**	                    | Data storage (cheap, scalable)                               |
| **AWS CloudWatch**	            | Idle detection (CPU, Network In/Out)                         |
| **AWS IAM**	                    | Least-privilege role (EC2 + S3 only)                         |
| **boto3**                  	    | AWS SDK for Python                                           |
| **AWS Lambda (opt)**	            | Scheduled inactivity checks without needing a PC on 24/7     |
| **Pydantic**	                    | Config validation                                            |
| **PyYAML**	                    | YAML parsing                                                 |

--- 

## 🔒 Security First

This project is designed with **security and privacy** in mind:

- No credentials in code -> use environment variables or AWS profiles
- **IAM role with minimal permissions**:
    - ec2:StartInstances, ec2:StopInstances, ec2:DescribeInstances
    - s3:GetObject, s3:PutObject (restricted to specific buckets)
    - cloudwatch:GetMetricData
- **Local-first**: your data never leaves your machine unless you explicitly send it to S3
- **Full audit log**: every action is logged with timestamps

> 🐥⚠️ **Never commit your** .env **file or AWS credentials**.

---

## 🖥️ Usage

### 🚀 Quick Install

```bash 
git clone https://github.com/sm7ss/HybridFinOps
cd HybridFinOps

poetry install   # or pip install -r requirements.txt
poetry shell     # or activate your venv
```

### ⚙️ Configure

1. Create a *.env* file with:

```env
TELEGRAM_BOT_TOKEN=your_token_here
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
```

2. Edit [config/config.yaml](/config/config.yaml) with your budget and time thresholds.

### ▶️ Run

```bash
python main.py
```

> 🐥🚧 Bot and AWS integration are still in development. Expect rough edges.

---

## 📁 Project Structure

```text 
📂 hybrid_finOps/
├── 📂 config/
│   └── config.yaml
├── 📂 src/
│   ├── read_validation.py
│   ├── validation.py
│   └── logic.py
├── .gitignore
├── LICENSE
├── main.py
├── pyproject.toml
├── README-ESP.md
└── README.md
```

> 🐥 Structure will grow as the bot and AWS integration mature.

---

## 🚧 Roadmap

- Implement Telegram bot (aiogram / python-telegram-bot — TBD)
- Connect to AWS via boto3 (EC2 + S3)
- Integrate CloudWatch for idle detection
- Add Lambda for scheduled inactivity checks
- Full auto-shutdown logic (budget + no response)
- Cost calculations per action (postpone, keep, etc.)
- Hybrid ML pipeline (S3 → local → cloud training)
- IAM minimal-permission role
- Comprehensive logging system
- Add tests

---

## 🤝 Contributing

Fork the project
Create your branch (`git checkout -b feature/new-feature`)
Commit your changes (`git commit -m 'Add new feature'`)
Push to the branch (`git push origin feature/new-feature`)
Open a Pull Request

> 💡🐥 Ideas, suggestions, or war stories about AWS bills? Open to feedback!

---

## 📄 License

This project is licensed under the **MIT License**.
You are free to use, modify, and share it.

---

## 📬 Contact

🌵 **HybridFinOps** — Inspired by Pablo the Cactus.

