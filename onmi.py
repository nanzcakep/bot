import requests
import re
import json


def get_email():
    endpoint = 'https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1'
    return requests.get(endpoint).json()[0]


def register_user(email, nickname, invite_code):
    url = 'https://onmi-waitlist.rand.wtf/api/register'
    
    headers = {
        'Host': 'onmi-waitlist.rand.wtf',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Accept': '*/*',
        'Accept-Language': 'id,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://onmi.io/',
        'Content-Type': 'application/json',
        'Content-Length': '142',
        'Origin': 'https://onmi.io',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Te': 'trailers'
    }
    
    payload = {
        'email': email,
        'nickname': nickname,
        'password': 'Helloworld123',
        'password_confirmation': 'Helloworld123',
        'invite_code': invite_code
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    try:
        data = response.json()
        return data
    except json.decoder.JSONDecodeError:
        print(f"Waiting for email ...")


def get_inbox(login, domain):
    endpoint = f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}'
    return requests.get(endpoint).json()


def get_message(login, domain, id):
    endpoint = f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={id}'
    message_data = requests.get(endpoint).json()
    if 'body' in message_data:
        return message_data['body']
    return None


def extract_links_from_html(html_content):
    href_links = re.findall(r'href="([^"]+)"', html_content)
    unique_href_links = list(set(href_links))
    return unique_href_links


def extract_verify_link(links):
    for link in links:
        if re.search(r'https://onmi.io/\?verify_code=[\w-]+', link):
            return link.split('=')[1]
    return None


def activate_account(code):
    url = 'https://onmi-waitlist.rand.wtf/api/activate'
    
    headers = {
        'Host': 'onmi-waitlist.rand.wtf',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Accept': '*/*',
        'Accept-Language': 'id,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://onmi.io/',
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': '23',
        'Origin': 'https://onmi.io',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Te': 'trailers'
    }
    
    payload = {
        'code': code
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    try:
        data = response.json()
        return data
    except json.decoder.JSONDecodeError:
        return "Success verify Account"


reff = input("Enter your reff code: ")
n = int(input("Enter the number of accounts you want to create: "))

for _ in range(n):
    x = get_email().split('@')

    login = x[0]
    domain = x[1]

    print(f'successfully created email: {login}@{domain}')

    response = register_user(f'{login}@{domain}', '', reff)

    print(response)

    while True:
        inbox = get_inbox(login, domain)
        if inbox != []:
            break

    id = get_inbox(login, domain)[0]['id']

    message_body = get_message(login, domain, id)

    if message_body:
        links = extract_links_from_html(message_body)
        verify_code = extract_verify_link(links)
        if verify_code:
            print(f'Success get verify code : {verify_code}')
            print(activate_account(verify_code))
            print('==================')
        else:
            print("Failed to find the verification code.")
    else:
        print("Failed to retrieve message body.")
