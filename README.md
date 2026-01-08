# 🚀 Nexira Autopilot Bot (SS1 & SS2)

An automated, stealth-focused Python script designed to handle **daily check-ins** for both:

- **Season 1 – Ruby Awakening**
- **Season 2 – New Year's Campaign**

on the **Nexira** platform.

> ⚠️ **IMPORTANT**
>
> Don’t have a Nexira account yet?
> Join here: https://www.nexira.ai/airdrops?refid=tSRI3QMA

---

## ✨ Features

### 🔄 Dual-Season Automation
- Automatically performs daily check-ins for **SS1 and SS2** in one run.

### 🕵️ Anti-Detection System
- **Dynamic Fingerprinting** – Generates a unique browser User-Agent for every account.
- **Randomized Jitter** – Human-like random delays between actions.
- **Account Shuffling** – Accounts are processed in a different order every day.

### 🌐 Proxy Support
- Optional proxy usage to hide your local IP.
- Supports **HTTP** and **SOCKS5** proxies.

### ⏰ 24/7 Autopilot
- After finishing daily tasks, the bot calculates the time until the next reset (midnight) and sleeps automatically.

---

## 🛠 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/mejri02/nexira-bot.git
cd nexira-bot
```

### 2️⃣ Install Requirements

Make sure you have **Python 3.8+** installed, then run:

```bash
pip install -r requirements.txt
```

### 3️⃣ Configuration Files

Create the following files in the project directory:

#### 📄 `token.txt`
- Add your **Nexira Bearer tokens**, one per line.
- You can obtain them from the **Network** tab in your browser's Developer Tools.

#### 📄 `proxies.txt` (Optional)
- Add one proxy per line if you want to use proxies.

Supported formats:
```
http://user:pass@host:port
socks5://host:port
```

---

## 🚀 How to Use

### 1️⃣ Run the Script

```bash
python main.py
```

### 2️⃣ Choose Connection Mode
- Select whether to use **Proxies** or your **Local IP** when prompted.

### 3️⃣ Bot Workflow
The bot will:
1. Process all accounts for **Season 1**
2. Process all accounts for **Season 2**
3. Start a countdown timer until the next daily reset

---

## 📦 requirements.txt

If you don’t have one yet, create a `requirements.txt` file with the following content:

```
aiohttp
aiohttp_socks
colorama
inquirer
```

---

## ⚠️ Disclaimer

This tool is provided **for educational purposes only**.

- Use it **at your own risk**
- The developer is **not responsible** for any bans, restrictions, or losses

---

### ❤️ Developed by MEJRI02
