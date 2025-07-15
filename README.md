# Algorand Wallet Vanity Address Generation

This is a collection of Python scripts I've written while exploring the Algorand blockchain. It includes:

- 🔍 A Vanity Address Generator for finding meaningful patterns in wallet addresses
- 📊 An address analysis tool that led me to a critical insight about how Algorand addresses end
- 🧪 A JSON file to easily enter in repeatable search terms
- NOTE: the larger the search space, the more addresses that need to be generated to search. Searching for terms 5 letters long or longer will require at least millions of addresses to be generated.

> ⚡️ This repo is an archive of learning, hacking, and real-world debugging. 
Inspired by https://algovanity.com/

---

# Installation
pip install -r requirements.txt

---

# Project list

### 🧢 `vanity_generator/`
Generates vanity Algorand addresses based on patterns (front, back, anywhere, or both).

### 📈 `vanity_generator/analysis/`
A small script used to analyze generated address patterns and discover something odd — Algorand wallet addresses **can only end in 8 specific characters**.

---

# 🧢 `vanity_generator/`

This is a flexible and interactive **Vanity Address Generator** for the Algorand blockchain.

---

#### 🚀 What it does

- Generates Algorand addresses using the official `algosdk`
- Searches those addresses for **custom string patterns**
- Allows patterns at the:
  - **Front**
  - **Back**
  - **Anywhere**
  - Or a combination of **Front & Back**
- Supports **manual input** or **automated JSON-based config files**
- Enforces Algorand's **valid end character constraints**
- Displays **matches with visual alignment** in the 58-character address

---

#### 🧠 Why I built it

Originally, I just wanted to find Algorand wallet addresses that started with my name.  
Then I thought:

- “Why not search the end too?”  
- “What about the middle?”  
- “What if I want both front and back?”  
- “What if I want to automate 10 search terms?”

So I added all of it — one idea at a time — until this became a full-blown tool I could reuse, tweak, and expand.

---

#### 🔤 Input Types

- **Manual mode**: Enter search terms interactively
- **JSON config mode**: Load from a `searchAlgo.json` file

---

# 📈 `vanity_generator/analysis/`

This script helped me uncover something I couldn’t find documented anywhere:

> Algorand wallet addresses can only end in **I, Y, Q, U, A, 4, M, E**

## Why?

While building a vanity address generator, I kept failing to find addresses ending in patterns like `"AB"`. Frustrated, I wrote this script to brute force the data.

It turns out, due to how **Algorand Base32 encoding and checksums** work, **only 8 characters** can appear at the end of a valid public address.

Later, I even confirmed this with John Woods, CTO of the Algorand Foundation:

> *"Base32 encoding of the checksum"* — @JohnAlanWoods

---

## Usage

> python3 algorandWalletStats.py

It analyzes 100,000 addresses and shows stats on last character frequency.
Most common last character:
I: 12.660%
Y: 12.659%
These were my results, yours will be different!

---

### 📃 3. `.gitignore`

#### File: `.gitignore`

__pycache__/
*.pyc
*.bak
*.log
*.DS_Store
.env
bak/
