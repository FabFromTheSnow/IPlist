import json
import urllib.request

URL = "https://endpoints.office.com/endpoints/worldwide?clientrequestid=00000000-0000-0000-0000-000000000000"

with urllib.request.urlopen(URL) as response:
    data = json.load(response)

ips = set()

for entry in data:
    for ip in entry.get("ips", []):
        ips.add(ip)

with open("output/microsoft365-ips.txt", "w", encoding="utf-8") as f:
    for ip in sorted(ips):
        f.write(ip + "\n")

print(f"{len(ips)} IP ranges written")
