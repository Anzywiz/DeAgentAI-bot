# DeAgentAI-bot

Python-based script to automate daily tasks (Alpha X, Twitter, and Discord) on the DeAgent quest website.

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
    "proxies": null,
    "maximum_number_of_threads": 5
}
```

- **Proxies**: Set this to `null` or an empty string (`""`) if not using proxies. For rotating proxies, use the format `http://username:password@host:port`.

---

## Running the Bot

1. Ensure the virtual environment is activated.
2. Run the script:
   ```bash
   python main.py
   ```

---

## Notes

- Ensure `private_keys` are properly configured.
- **Proxies**: If using proxies, rotating proxies are preferable for better performance.

---

## Security

- **NEVER** share your `config.json` file publicly.
- Add `config.json` to `.gitignore` to avoid accidental uploads:
  ```plaintext
  config.json
  ```

---

## Warning

- Ensure your `config.json` file is correctly set up as described above to avoid runtime errors.

