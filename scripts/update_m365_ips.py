import json
import urllib.request
import uuid
import ipaddress
from pathlib import Path

client_request_id = str(uuid.uuid4())

URL = (
    "https://endpoints.office.com/endpoints/Worldwide"
    f"?ClientRequestId={client_request_id}"
)

request = urllib.request.Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

with urllib.request.urlopen(request, timeout=30) as response:
    data = json.load(response)

ipv4 = set()
ipv6 = set()

for entry in data:
    for ip in entry.get("ips", []):
        network = ipaddress.ip_network(ip, strict=False)

        if network.version == 4:
            ipv4.add(str(network))
        else:
            ipv6.add(str(network))

Path("output").mkdir(exist_ok=True)

with open("output/microsoft365-ipv4.txt", "w", encoding="utf-8") as f:
    for ip in sorted(ipv4, key=lambda x: ipaddress.ip_network(x)):
        f.write(ip + "\n")

with open("output/microsoft365-ipv6.txt", "w", encoding="utf-8") as f:
    for ip in sorted(ipv6, key=lambda x: ipaddress.ip_network(x)):
        f.write(ip + "\n")

print(f"{len(ipv4)} IPv4 networks written")
print(f"{len(ipv6)} IPv6 networks written")
