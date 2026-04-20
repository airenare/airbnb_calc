# 🏡 Airbnb Profit Calculator

A simple interactive web application for exploring short‑term rental (Airbnb) profitability using adjustable input parameters.
This is an experiment for fun, not a professional financial tool.

It’s built with Python + Streamlit, and includes a one‑click setup script that automatically prepares the environment (including installing Python via pyenv, virtual environment, deps, etc.) so you can run the app on any machine.

## 🚀 Features

**Inputs (sidebar — infrequent parameters)**
- Mortgage rate and term
- Airbnb host fee rate (3% or 15.5%)
- Property management fee rate
- Property tax rate
- Utilities: electricity, water, gas, internet, garbage collection, HOA
- Insurance

**Inputs (main area — frequently adjusted)**
- Property price, down payment, and closing costs → auto-calculated monthly/annual mortgage payment
- Renovation & furnishing costs with separate loan rate and term → auto-calculated loan payment
- Nightly rate and occupancy rate → projected gross revenue

**Metrics (monthly and annual)**
- Total Expenses, Revenue, Profit
- Profit Margin
- ROI (based on down payment + renovation costs)

**Charts**
- Profit contour plot across nightly rate × occupancy combinations, with a break-even line and a "You are here" marker for the current strategy
- Break-even occupancy curves across multiple home price scenarios

**Other**
- Itemized expense breakdown table
- Automatic environment setup via `deploy.sh`

## 📦 Repository Contents
| File | Description |
| --- | --- |
| app.py | Main Streamlit application |
| default_values.py | Default model values |
| requirements.txt | Python dependencies |
| deploy.sh | Portable one‑click setup + run script |
| .python-version | pyenv Python version file |

## 🛠 Installation & Setup
### 🔹 Requirements
Before running the project, ensure:
- Git is installed
- You have a Unix‑compatible shell (bash / Linux / macOS)
- curl is available

The script handles Python installation via pyenv and sets up the environment automatically.

### ▶️ Local Setup (Single‑Command)

Clone the repository:

```bash
git clone https://github.com/airenare/airbnb_calc.git
cd airbnb_calc
```

Make the launcher script executable:

```bash
chmod +x deploy.sh
```

### ✅ Automatic Setup + Run (interactive)
```bash
./deploy.sh
```

The script will:
- Install pyenv if missing
- Install Python 3.12.2 via pyenv
- Create a virtual environment under ./.venv/3.12.2
- Install dependencies from requirements.txt
- Clone (or update) the project repository
- Start the app inside a tmux session

### ⚡ Fully Automated (No Prompts)

To skip all confirmations and run non‑interactively:

```bash
./deploy.sh --force
```

## 🔎 How to Access the App

After the script finishes:
Attach to the tmux session:
```bash
tmux attach -t streamlit
# or
tmux a
```
Streamlit will be running at:
http://localhost:8501

Open in your browser to interact with the calculator.

### 🧠 What the Script Does

The provided deploy.sh automates environment setup using pyenv, ensuring:
Correct Python version installed
- A stable virtual environment
- Dependencies installed
- Streamlit launched in a separate tmux session

This makes the project portable — you can run it on any machine with a shell, without needing manual setup.

## 📌 Notes

- This is a demo / experiment, not financial advice
- Requirements include Streamlit and other libraries listed in requirements.txt
- The script assumes a Unix‑like environment (Linux, macOS)
- For information on installing dependencies manually, refer to the Streamlit installation docs
.

## 📬 Feedback & Contributions

If you find bugs or want to suggest improvements, feel free to open an issue or submit a pull request on GitHub.
