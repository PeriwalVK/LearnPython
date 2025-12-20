import requests
from requests.exceptions import Timeout, HTTPError, RequestException
import json  # For pretty-printing JSON in some examples

"""
kwargs can be figured from below method
request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    )
"""

def separator(msg: str, l: int = 100):
    n = len(msg)
    hash_len = (l - n - 2) // 2
    print(" ")
    print("=" * l)
    print(f"{'#'*hash_len} {msg} {'#'*hash_len}")
    print("=" * l)


##############################################################################################
##############################################################################################



# SECTION 1: Simple GET Request
def simple_get_request():
    separator("1. SIMPLE GET REQUEST")
    response = requests.get('https://httpbin.org/get')
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Text (first 200 chars): {response.text[:200]}...\n")


##############################################################################################
##############################################################################################



# SECTION 2: GET with Query Parameters
def get_with_query_parameters():
    separator("2. GET WITH QUERY PARAMETERS")
    params = {'key1': 'value1', 'key2': ['value2a', 'value2b'], 'key3': 42}
    response = requests.get('https://httpbin.org/get', params=params)
    print(f"JSON Response: {json.dumps(response.json(), indent=2)}\n")



##############################################################################################
##############################################################################################


# SECTION 3: POST Request with Form Data
def post_with_form_data():
    separator("3. POST WITH FORM DATA")
    data = {'username': 'user', 'password': 'pass123'}
    response = requests.post('https://httpbin.org/post', data=data)
    print(f"Status: {response.status_code}")
    print(f"response.json(): {response.json()}\n")
    print(f"Form Data Echoed: {response.json()['form']}\n")



##############################################################################################
##############################################################################################



# SECTION 4: POST with JSON Data
def post_with_json_data():
    separator("4. POST WITH JSON DATA")
    json_data = {'name': 'Alice', 'age': 30, 'skills': ['Python', 'HTTP']}
    response = requests.post('https://httpbin.org/post', json=json_data)  # auto-sets Content-Type
    print(f"JSON Echoed: {json.dumps(response.json()['json'], indent=2)}\n")


##############################################################################################
##############################################################################################


# SECTION 5: Custom Headers
def custom_headers():
    separator("5. CUSTOM HEADERS")
    headers = {
        'User-Agent': 'MyCustomApp/1.0',
        'Accept': 'application/json',
        'Custom-Header': 'Hello World'
    }
    response = requests.get('https://httpbin.org/headers', headers=headers)
    print(f"Received Headers: {json.dumps(response.json()['headers'], indent=2)}\n")



##############################################################################################
##############################################################################################



# SECTION 6: Basic Authentication
def basic_authentication():
    separator("6. BASIC AUTH")
    # httpbin.org/basic-auth/user/pass returns 200 only if auth succeeds
    response = requests.get('https://httpbin.org/basic-auth/grok/secret', auth=('grok', 'secret'))
    print(f"Auth Success: {response.status_code == 200}\n")



##############################################################################################
##############################################################################################



# SECTION 7: Sessions (for reusing connections/cookies/headers)
def Sessions_for_reusing_connections_cookies_headers():
    separator("7. SESSIONS")
    session = requests.Session()
    session.headers.update({'User-Agent': 'SessionApp/1.0'})
    r1 = session.get('https://httpbin.org/cookies/set/sessioncookie/abc123')
    r2 = session.get('https://httpbin.org/cookies')
    print(f"Cookie from r2: {r2.json()['cookies']}\n")



##############################################################################################
##############################################################################################



# SECTION 8: Response Object Methods
def response_object_methods():
    separator("8. EXPLORING RESPONSE OBJECT")
    response = requests.get('https://httpbin.org/json')
    print(f"Status: {response.status_code}, OK: {response.ok}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"Text (first 100): {response.text[:100]}")
    print(f"JSON: {json.dumps(response.json(), indent=2)}")
    print(f"Raw Bytes (first 50): {response.content[:50]}")
    print(f"URL: {response.url}\n")



##############################################################################################
##############################################################################################



# SECTION 9: Timeouts
def timeouts():
    separator("9. TIMEOUTS")
    try:
        response = requests.get('https://httpbin.org/delay/5', timeout=2.5)
    except Timeout as e:
        print(f"Timeout caught: {e}")
    else:
        print("No timeout!\n")



##############################################################################################
##############################################################################################



# SECTION 10: Error Handling and raise_for_status()
def error_handling_and_raise_for_status():
    separator("10. ERROR HANDLING")
    try:
        response = requests.get('https://httpbin.org/status/404')
        response.raise_for_status()  # Raises HTTPError for 4xx/5xx
    except HTTPError as e:
        print(f"HTTP Error: {e}")
    except RequestException as e:
        print(f"Request Error: {e}\n")



##############################################################################################
##############################################################################################



# SECTION 11: Streaming Large Responses
def streaming_large_responses():
    separator("11. STREAMING")
    response = requests.get('https://httpbin.org/stream/5', stream=True)
    for i, line in enumerate(response.iter_lines(decode_unicode=True)):
        if line:
            print(f"Stream Line {i+1}: {line}")
        if i >= 2:  # Limit output
            print("... (truncated)")
            break
    print()



##############################################################################################
##############################################################################################



# SECTION 12: Uploading Files (multipart form)
def uploading_files():
    separator("12. FILE UPLOAD")
    files = {
        'file': ('test.txt', b'Hello, Requests! This is file content.', 'text/plain')
    }
    response = requests.post('https://httpbin.org/post', files=files)
    print(f"Uploaded File Info: {response.json()['files']}\n")



##############################################################################################
##############################################################################################



# SECTION 13: Cookies
def cookies():
    separator("13. COOKIES")
    response1 = requests.get('https://httpbin.org/cookies/set?hello=world')
    cookies = response1.cookies
    response2 = requests.get('https://httpbin.org/cookies', cookies=cookies)
    print(f"Cookie Echo: {response2.json()['cookies']}\n")



##############################################################################################
##############################################################################################



# SECTION 14: Redirects
def redirects():
    separator("14. REDIRECTS")
    # Follow redirects by default
    response = requests.get('https://httpbin.org/redirect/2')
    print(f"Final Status: {response.status_code}, Redirects: {len(response.history)}")
    for r in response.history:
        print(f"Redirect: {r.status_code} -> {r.url}")
    print(f"Final URL: {response.url}\n")



##############################################################################################
##############################################################################################



# SECTION 15: Proxies (basic example)
def proxies():
    separator("15. PROXIES")
    proxies = {
        'http': 'http://10.10.1.10:3128',
        'https': 'http://10.10.1.10:3128',
    }
    # Note: Use a real proxy or comment out. httpbin doesn't need it, but demos syntax.
    # response = requests.get('https://httpbin.org/ip', proxies=proxies)
    print("Proxies syntax shown (uncomment with real proxy).\n")




if __name__ == "__main__":

    # simple_get_request()
    # get_with_query_parameters()
    post_with_form_data()
    # post_with_json_data()
    # custom_headers()
    # basic_authentication()
    # Sessions_for_reusing_connections_cookies_headers()
    # response_object_methods()
    # timeouts()
    # error_handling_and_raise_for_status()
    # streaming_large_responses()
    # uploading_files()
    # cookies()
    # redirects()
    # proxies()


    separator("Tutorial complete!")