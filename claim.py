import requests
import time
import threading
import subprocess

def read_init_data_from_file(filename):
    with open(filename, 'r') as file:
        init_data_list = [line.strip() for line in file if line.strip()]
    return init_data_list

def authenticate(init_data):
    url = 'https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP'
    headers = {
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'referer': 'https://telegram.blum.codes/',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    }
    payload = {'query': init_data}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['token']['access']
    except requests.exceptions.RequestException as error:
        print(f'Error during authentication: {error}')
        raise

def get_claim(token):
    url = 'https://game-domain.blum.codes/api/v1/farming/claim'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    try:
        response = requests.post(url, headers=headers)
        print('Claim successful')
        start_farm(token)
    except requests.exceptions.RequestException as error:
        print('Claim not available:', error.response.json()['message'])
        start_farm(token)

def start_farm(token):
    url = 'https://game-domain.blum.codes/api/v1/farming/start'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    try:
        response = requests.post(url, headers=headers)
        print(response.json())
        get_balance(token)
    except requests.exceptions.RequestException as error:
        print('Error during start farming:', error.response)

def get_balance(token):
    url = 'https://game-domain.blum.codes/api/v1/user/balance'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
        'Authorization': f'Bearer {token}',
        'Origin': 'https://telegram.blum.codes',
        'Priority': 'u=1, i',
        'Referer': 'https://telegram.blum.codes/',
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers)
        print('Balance:', response.json()['availableBalance'])
    except requests.exceptions.RequestException as error:
        print('Error fetching balance:', error)


def process_init_data(init_data):
    while True:
        try:
            token = authenticate(init_data)
            get_claim(token)
        except Exception as e:
            print(f'An error occurred: {e}')
            print('Running claim.py...')
            subprocess.run(['python3.10', 'claim.py'])
            break
        print('Sleeping for 6 hours...')
        time.sleep(6 * 60 * 60)

def main():
    init_data_list = read_init_data_from_file('initdata.txt')
    threads = []
    for init_data in init_data_list:
        thread = threading.Thread(target=process_init_data, args=(init_data,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
