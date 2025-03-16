import os
import time
import random
import requests
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple

import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

BASE_URL = 'https://prod-api.pinai.tech'

class HiPinBot:
    def __init__(self):
        self.tokens = []
        self.proxies = []
        self.default_headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'lang': 'en-US',
            'content-type': 'application/json',
            'sec-ch-ua': '"Chromium";v="133", "Microsoft Edge WebView2";v="133", "Not(A:Brand";v="99", "Microsoft Edge";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'Referer': 'https://web.pinai.tech/',
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
        self.start_time = datetime.now()
        self.resource_types = ["Twitter", "Facebook", "Google", "Telegram",]
    
    def display_banner(self):
    print(f"{Fore.CYAN}       █████╗ ██████╗ ██████╗     ███╗   ██╗ ██████╗ ██████╗ ███████╗")
    print(f"{Fore.CYAN}      ██╔══██╗██╔══██╗██╔══██╗    ████╗  ██║██╔═══██╗██╔══██╗██╔════╝")
    print(f"{Fore.CYAN}      ███████║██║  ██║██████╔╝    ██╔██╗ ██║██║   ██║██║  ██║█████╗  ")
    print(f"{Fore.CYAN}      ██╔══██║██║  ██║██╔══██╗    ██║╚██╗██║██║   ██║██║  ██║██╔══╝  ")
    print(f"{Fore.CYAN}      ██║  ██║██████╔╝██████╔╝    ██║ ╚████║╚██████╔╝██████╔╝███████╗")
    print(f"{Fore.CYAN}      ╚═╝  ╚═╝╚═════╝ ╚═════╝     ╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝")
    print(f"{Fore.CYAN}        By : ADB NODE")
    
    def load_tokens(self):
        try:
            print(f"{Fore.YELLOW}[SYSTEM] {Fore.WHITE}Loading tokens...")
            with open('tokens.txt', 'r', encoding='utf-8') as f:
                tokens = [line.strip() for line in f.readlines() if line.strip()]
            
            if not tokens:
                print(f"{Fore.RED}[ERROR] No tokens found in tokens.txt")
                exit(1)
            
            self.tokens = [f"Bearer {token}" for token in tokens]
            print(f"{Fore.GREEN}[SYSTEM] {Fore.WHITE}Loaded {len(tokens)} tokens!")
            return self.tokens
        except FileNotFoundError:
            print(f"{Fore.RED}[ERROR] tokens.txt file not found")
            exit(1)
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Error reading tokens.txt: {str(e)}")
            exit(1)
    
    def load_proxies(self):
        try:
            if not os.path.exists('proxies.txt'):
                print(f"{Fore.YELLOW}[INFO] No proxies.txt found. Using direct connections.")
                return []
            
            with open('proxies.txt', 'r', encoding='utf-8') as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
            
            if not proxies:
                print(f"{Fore.YELLOW}[INFO] proxies.txt is empty. Using direct connections.")
                return []
            
            self.proxies = proxies
            print(f"{Fore.GREEN}[SYSTEM] {Fore.WHITE}Loaded {len(proxies)} proxies!")
            return proxies
        except Exception as e:
            print(f"{Fore.YELLOW}[WARN] Error reading proxies.txt: {str(e)}. Using direct connections.")
            return []
    
    def format_proxy(self, proxy_url):
        if not proxy_url:
            return {}
        
        if '://' in proxy_url:
            return {'http': proxy_url, 'https': proxy_url}
        
        if ':' in proxy_url:
            return {'http': f'http://{proxy_url}', 'https': f'http://{proxy_url}'}
        
        return {}
    
    def get_ip_address(self, session):
        try:
            response = session.get('http://ip-api.com/json', timeout=10)
            data = response.json()
            return data.get('query', 'Unknown')
        except Exception:
            return 'Unknown'
    
    def create_session(self, token, proxy=None):
        session = requests.Session()
        
        headers = self.default_headers.copy()
        headers['authorization'] = token
        session.headers.update(headers)
        
        if proxy:
            session.proxies.update(self.format_proxy(proxy))
        
        ip_address = self.get_ip_address(session)
        
        return session, ip_address
    
    def check_home(self, session, account_index):
        try:
            print(f"{Fore.CYAN}[ACCOUNT] {Fore.WHITE}Checking account status...")
            response = session.get(f"{BASE_URL}/home")
            response.raise_for_status()
            data = response.json()
            
            print(f"{Fore.BLUE}[PROFILE] Account: {data.get('user_info', {}).get('name', 'Unknown')}")
            print(f"{Fore.BLUE}[PROFILE] Level: {data.get('current_model', {}).get('current_level', 'N/A')}")
            pin_points = data.get('pin_points', '0')
            if isinstance(pin_points, str):
                pin_points = pin_points.replace('K', '000').replace('.', '')
                try:
                    pin_points = int(pin_points)
                except:
                    pin_points = 0
            
            print(f"{Fore.YELLOW}[STATS] Pin Points: {data.get('pin_points', '0')}")
            
            # Dynamically get available resources from the home data
            available_resources = []
            for resource_type in self.resource_types:
                if resource_type.lower() in str(data).lower():
                    available_resources.append(resource_type)
            
            if not available_resources:
                # Fallback to default resources if none detected
                available_resources = ["Twitter", "Facebook", "Google, Telegram"]
                
            # Check if AI Agent is available
            if "agent" in str(data).lower():
                print(f"{Fore.GREEN}[AI AGENT] AI Agent is available!")
                available_resources.append("AI Agent")
            else:
                print(f"{Fore.YELLOW}[AI AGENT] No AI Agent available. Please try again tomorrow!")
            
            print(f"{Fore.CYAN}[RESOURCES] Available: {', '.join(available_resources)}")
            
            return data, available_resources, pin_points
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to check home: {str(e)}")
            return None, [], 0
    
    def get_random_task(self, session, account_index):
        try:
            print(f"{Fore.CYAN}[RANDOM TASK] {Fore.WHITE}Checking for random task...")
            response = session.get(f"{BASE_URL}/task/random_task_list")
            response.raise_for_status()
            data = response.json()
            
            task_count = len(data.get('data', []))
            if task_count > 0:
                print(f"{Fore.GREEN}[RANDOM TASK] Found {task_count} random tasks available!")
                return True
            else:
                print(f"{Fore.YELLOW}[RANDOM TASK] No random tasks available. Try again tomorrow!")
                return False
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to check random tasks: {str(e)}")
            return False
    
    def claim_random_task(self, session, account_index):
        try:
            print(f"{Fore.CYAN}[RANDOM TASK] {Fore.WHITE}Claiming random task...")
            response = session.get(f"{BASE_URL}/task/claim_random_task")
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}[SUCCESS] Random task claimed successfully!")
                return response.json()
            else:
                print(f"{Fore.YELLOW}[INFO] Random task already claimed today. Try again tomorrow!")
                return None
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to claim random task: {str(e)}")
            return None
    
    def daily_checkin(self, session, account_index):
        try:
            print(f"{Fore.CYAN}[DAILY] {Fore.WHITE}Performing daily check-in...")
            # First get checkin data
            response = session.get(f"{BASE_URL}/task/checkin_data")
            response.raise_for_status()
            data = response.json()
            
            # Check if we can claim the daily check-in
            if data.get('can_checkin', False):
                claim_response = session.post(f"{BASE_URL}/task/checkin", json={})
                claim_response.raise_for_status()
                print(f"{Fore.GREEN}[SUCCESS] Daily check-in completed!")
                return claim_response.json()
            else:
                print(f"{Fore.YELLOW}[INFO] Daily check-in already claimed.")
                return data
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to perform daily check-in: {str(e)}")
            return None
    
    def check_and_upgrade_model(self, session, account_index, pin_points):
        try:
            print(f"{Fore.CYAN}[UPGRADE] {Fore.WHITE}Checking for available upgrades...")
            # Get home data which contains upgrade info
            response = session.get(f"{BASE_URL}/home")
            response.raise_for_status()
            data = response.json()
        
            current_level = data.get('current_model', {}).get('current_level', 0)
            next_level_points = data.get('current_model', {}).get('next_level_need_point', float('inf'))
        
            # Convert next_level_points to int if it's a string
            if isinstance(next_level_points, str):
                try:
                    next_level_points = int(next_level_points.replace('K', '000').replace('.', ''))
                except:
                    next_level_points = float('inf')
        
            if next_level_points and pin_points >= next_level_points:
                print(f"{Fore.GREEN}[UPGRADE] Enough points to upgrade! (Level {current_level} → {current_level + 1})")
                # Try the upgrade - using an empty body with the POST request
                try:
                    upgrade_response = session.post(f"{BASE_URL}/model/upgrade", json={})
                    upgrade_response.raise_for_status()
                    print(f"{Fore.GREEN}[SUCCESS] Model upgraded to level {current_level + 1}!")
                    return upgrade_response.json()
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 400:
                        print(f"{Fore.YELLOW}[UPGRADE] Upgrade not available. You may need to wait until tomorrow.")
                    else:
                        print(f"{Fore.RED}[ERROR] Failed to upgrade model: {str(e)}")
            else:
                points_needed = next_level_points - pin_points
                print(f"{Fore.YELLOW}[UPGRADE] Not enough points for upgrade. Need {points_needed} more points.")
                return data
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to check model upgrade: {str(e)}")
            return None
    
    def collect_resources(self, session, resource_types, account_index):
        """Collect resources in a randomized manner"""
        try:
            # Shuffle the resource types
            random.shuffle(resource_types)
            
            print(f"{Fore.CYAN}[RESOURCES] {Fore.WHITE}Collecting resources randomly...")
            
            # Collect resources in a randomized order
            for resource_type in resource_types:
                # Add a small random chance to skip a resource occasionally
                if random.random() < 0.05:  # 5% chance to skip
                    print(f"{Fore.YELLOW}[RESOURCE] Skipping {resource_type} this time...")
                    continue
                    
                print(f"{Fore.CYAN}[RESOURCE] {Fore.WHITE}Collecting {resource_type}...")
                body = [{"type": resource_type, "count": 1}]
                response = session.post(f"{BASE_URL}/home/collect", json=body)
                response.raise_for_status()
                print(f"{Fore.GREEN}[SUCCESS] {resource_type} collected!")
                
                # Add random delay between resource collections
                sleep_time = random.uniform(1.5, 4.5)
                print(f"{Fore.YELLOW}[WAIT] Waiting {sleep_time:.2f} seconds before next action...")
                time.sleep(sleep_time)
                
            return True
        except requests.HTTPError as e:
            print(f"{Fore.RED}[ERROR] Failed to collect resources: {e}")
            return None
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to collect resources: {str(e)}")
            return None
    
    def perform_crypto_news(self, session, account_index):
        try:
            print(f"{Fore.CYAN}[CRYPTO] {Fore.WHITE}Performing Crypto News action...")
            # Use GET for crypto news
            response = session.get(f"{BASE_URL}/action/cryptonews")
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}[SUCCESS] Crypto News action completed!")
                return response.json()
            elif response.status_code == 400:
                print(f"{Fore.YELLOW}[CRYPTO] Crypto News already completed for today. Come back tomorrow!")
                return None
            else:
                response.raise_for_status()
                return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                print(f"{Fore.YELLOW}[CRYPTO] Crypto News already completed for today. Come back tomorrow!")
            else:
                print(f"{Fore.RED}[ERROR] Failed to perform Crypto News action: {str(e)}")
            return None
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to perform Crypto News action: {str(e)}")
            return None
    
    def run_account(self, token, proxy, account_index, total_accounts):
        session, ip_address = self.create_session(token, proxy)
        
        print(f"\n{Fore.CYAN}===== Account #{account_index + 1}/{total_accounts} =====")
        print(f"{Fore.YELLOW}[INFO] IP used: {ip_address}")
        print(f"{Fore.YELLOW}[INFO] Proxy: {proxy or 'Direct connection'}")
        
        try:
            cycle_count = 1
            while True:  # Run indefinitely
                print(f"\n{Fore.CYAN}[CYCLE] {Fore.WHITE}Starting cycle #{cycle_count} for Account #{account_index + 1}")
                
                # Daily check-in
                self.daily_checkin(session, account_index)
                
                # Check home and get available resources
                home_data, available_resources, pin_points = self.check_home(session, account_index)
                
                # Check for model upgrade
                self.check_and_upgrade_model(session, account_index, pin_points)
                
                # Check and claim random task
                if self.get_random_task(session, account_index):
                    self.claim_random_task(session, account_index)
                
                # Try Crypto News action
                crypto_result = self.perform_crypto_news(session, account_index)
               # Only try again if not a 400 error (which means already completed for today)
                if crypto_result is not None:
                   for _ in range(3):  # Try 3 more times if successful
                       time.sleep(1)
                       self.perform_crypto_news(session, account_index)
               
               # Collect resources randomly
                if available_resources:
                   self.collect_resources(session, available_resources, account_index)
               
               # Check updated balance after collecting resources
                print(f"{Fore.CYAN}[UPDATE] {Fore.WHITE}Checking updated balance...")
                home_data, _, pin_points = self.check_home(session, account_index)
                print(f"{Fore.YELLOW}[UPDATED STATS] Pin Points: {home_data.get('pin_points', '0')}")
               
               # Random wait time between 7-10 seconds
                wait_time = random.randint(7, 10)
                print(f"{Fore.GREEN}[CYCLE] Cycle #{cycle_count} completed! Waiting {wait_time} seconds...")
                time.sleep(wait_time)
               
                cycle_count += 1
               
               # We don't want this function to loop indefinitely
               # After a number of cycles, we'll return to let the next account run
                if cycle_count > 5:  # Run 5 cycles per account before moving to next
                   print(f"{Fore.YELLOW}[Account] {Fore.WHITE}Completed 5 cycles for Account #{account_index + 1}, switching to next account")
                   break
           
        except KeyboardInterrupt:
           print(f"{Fore.YELLOW}[Account] {Fore.WHITE}Account #{account_index + 1} stopped by user")
           raise  # Re-raise to stop the entire program
        except Exception as e:
           print(f"{Fore.RED}[ERROR] Account #{account_index + 1} failed: {str(e)}")
   
    def start(self):
       """Start the HiPin bot"""
       os.system('cls' if os.name == 'nt' else 'clear')
       
       self.display_banner()
       time.sleep(1)
       
       tokens = self.load_tokens()
       proxies = self.load_proxies()
       
       print(f"{Fore.GREEN}[SYSTEM] {Fore.WHITE}Loaded {len(tokens)} accounts and {len(proxies)} proxies")
       
       # Main bot loop
       while True:  # This makes the entire bot run indefinitely
           for i, token in enumerate(tokens):
               proxy = proxies[i % len(proxies)] if proxies else None
               try:
                   self.run_account(token, proxy, i, len(tokens))
               except KeyboardInterrupt:
                   print(f"\n{Fore.YELLOW}[SYSTEM] {Fore.WHITE}Bot stopped by user")
                   return  # Exit the program
               except Exception as e:
                   print(f"{Fore.RED}[ERROR] Account #{i+1} failed: {str(e)}")
               
               if i < len(tokens) - 1:
                   print(f"{Fore.YELLOW}[SYSTEM] {Fore.WHITE}Waiting 5 seconds before starting next account...")
                   time.sleep(5)
           
           print(f"\n{Fore.GREEN}[SYSTEM] {Fore.WHITE}All accounts processed. Starting from the beginning again...")
           time.sleep(10)  # Wait 10 seconds before starting the cycle again

# Main execution
if __name__ == "__main__":
   try:
       bot = HiPinBot()
       bot.start()
   except KeyboardInterrupt:
       print(f"\n{Fore.YELLOW}[SYSTEM] {Fore.WHITE}Bot stopped by user")
   except Exception as e:
       print(f"\n{Fore.RED}[CRITICAL ERROR] {Fore.WHITE}The digital realm collapsed: {str(e)}")
       print(f"{Fore.YELLOW}[RECOVERY] {Fore.WHITE}Emergency evacuation protocol initiated!")
