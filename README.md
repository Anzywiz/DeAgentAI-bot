
# DeAgentAI-bot

Python-based script to automate daily tasks (Alpha X, Twitter, and Discord) on the DeAgent quest website.

---

## ⚠️ Warning
Using this script may be against the Terms and Conditions of [DeAgent](https://deagent.ai/). Proceed at your own discretion. The author of this script is not responsible for any consequences arising from its use.

---

## Prerequisites
- **Python**: Version 3.9 or above.
- **Git**: Installed on your system.

---

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/Anzywiz/DeAgentAI-bot.git
cd DeAgentAI-bot
```

### Step 2: Create and Activate a Virtual Environment

#### For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### For Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Configuration

### Step 4: Create a `config.json` File
Create a `config.json` file in the project directory with the following structure:

```json
{
    "private_keys": [
        "private_key1",
        "private_key2"
    ],
    "discord_auth_tokens": [
        "auth1",
        "auth2"
    ],
    "proxies": "",
    "maximum_number_of_threads": 5
}
```

---

## Running the Bot
1. Ensure the virtual environment is activated.
2. Run the script:
   ```bash
   python main.py
   ```

---

## Notes
- Ensure `private_keys` and `discord_auth_tokens` have matching indices where required. If the number of Discord tokens is fewer than private keys, the missing tokens will default to `None`.
- **Proxies**: Leave as an empty string (`""`) if not using proxies, or provide a valid proxy string.

---

## Security
- **NEVER** share your `config.json` file publicly.
- Add `config.json` to `.gitignore` to avoid accidental uploads:
   ```plaintext
   config.json
   ```

---
