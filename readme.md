# Account Creator Automation Script

This project automates the signup process on the ECOX platform using **Selenium** and **undetected-chromedriver**.

---

## 🚀 Installation

### 1. Clone the project

```bash
git clone [<https://github.com/abbas4445/haider-automation.git>]
cd heaider-automation
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
# Activate the environment
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Script

Run the automation script with:

```bash
python main.py
```

When prompted, type the number of accounts you want to create, for example:

```
How many accounts do you want to create? 10
```

The script will:

* Open the ECOX registration page
* Click "Skip" if present
* Fill in name, email, password
* Submit the form
* Handle username selection if required
* Keep the browser open for 10 seconds before closing each account
* Save credentials to `accounts.txt`

---

## 📂 Project Structure

```
.
├── main.py              # Main automation script
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## ⚠ Notes

* Ensure Chrome is installed and updated.
* The script uses **undetected-chromedriver** to bypass Cloudflare challenges.
* Generated accounts are saved in `accounts.txt` in the format:

  ```
  email | username | password
  ```

---

## 📝 License

This project is for educational and testing purposes only. Use responsibly.
