# HiPin Auto Bot

A Python automation tool for interacting with the HiPin platform to collect resources, complete daily check-ins, claim random tasks, and upgrade models automatically.

## Register
- [HIPin Bot](https://t.me/hi_PIN_bot/app?startapp=p9yt75P)

  
## Features

- Multi-account support
- Proxy support for distributing requests
- Automatic daily check-ins
- Random task claiming
- Resource collection with randomized timing
- Model upgrading when sufficient points are available
- Crypto News action automation
- Colorful console output for better readability

## Requirements

- Python 3.6+
- Required Python packages:
  - `requests`
  - `colorama`

## Installation

1. Clone the repository:
```
git clone https://github.com/airdropbomb/HiPin-AutoBot
cd HiPin-AutoBot
```

2. Install the required packages:
```
pip install -r requirements.txt
```

## Setup

1. Open `tokens.txt` file in the same directory as the script with one token per line:
```
token1
token2
token3
```
## How to get token?
- Play the game and then F12 or inspect element and go to Console Tab
- Paste this `localStorage.getItem('authToken')` and if you got a warning just type `allow pasting` and then paste it again
- right click into this one and then copy object. If there's something like this ` remove it
![image](https://github.com/user-attachments/assets/8ca54f44-e554-4b33-8742-db90f599115e)


2. (Optional) Open `proxies.txt` file with one proxy per line in the format `ip:port` or `protocol://ip:port`:
```
127.0.0.1:8080
http://proxy.example.com:8080
socks5://127.0.0.1:1080
```

## Usage

Run the bot:
```
python main.py
```

The bot will:
1. Load tokens and proxies
2. Process each account in sequence
3. For each account:
   - Perform daily check-in
   - Check available resources
   - Attempt model upgrades when possible
   - Claim random tasks
   - Perform Crypto News actions
   - Collect resources with random delays
4. Cycle through all accounts continuously

To stop the bot, press `Ctrl+C`.

## Customization

You can modify the following parameters in the script:
- `self.resource_types`: Types of resources to collect
- Number of cycles per account (default: 5)
- Wait times between actions and cycles

## Notes

- The bot uses random delays between actions to mimic human behavior
- Errors for individual accounts will not stop the bot from processing other accounts
- After processing all accounts, the bot will restart from the beginning

## Disclaimer

This tool is for educational purposes only. Use at your own risk.
