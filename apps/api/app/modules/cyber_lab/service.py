import time

from app.modules.cyber_lab.schemas import CVEItem, ScanResult, ToolInfo

TOOL_REGISTRY: list[ToolInfo] = [
    ToolInfo(id="nmap", name="Nmap", description="Network port scanner", category="recon"),
    ToolInfo(id="sqlmap", name="SQLMap", description="SQL injection tester", category="web"),
    ToolInfo(id="ffuf", name="FFUF", description="Web fuzzer", category="web"),
    ToolInfo(id="subfinder", name="Subfinder", description="Subdomain discovery", category="recon"),
]

_MOCK_OUTPUTS: dict[str, str] = {
    "nmap": """\
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for {target}
Host is up (0.021s latency).
Not shown: 995 closed tcp ports (conn-refused)
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.9p1 Ubuntu 3ubuntu0.6
80/tcp   open  http     Apache httpd 2.4.52
443/tcp  open  https    nginx 1.18.0
3306/tcp open  mysql    MySQL 8.0.35
8080/tcp open  http     Werkzeug/2.3.7 Python/3.11.5

Service detection performed.
Nmap done: 1 IP address (1 host up) scanned in 3.21 seconds""",

    "sqlmap": """\
[*] starting @ 12:34:56 /2026-06-18/
[*] testing connection to the target URL
[*] testing if the target URL content is stable
[*] testing if GET parameter 'id' is dynamic
[*] heuristic (basic) test shows that GET parameter 'id' might be injectable
    possible DBMS: 'MySQL'
[*] testing for SQL injection on GET parameter 'id'
[INFO] GET parameter 'id' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable
[INFO] target URL appears to be injectable with MySQL backend
[INFO] fetching banner
back-end DBMS: MySQL >= 8.0.0
banner: '8.0.35-0ubuntu0.22.04.1'

[!] legal disclaimer: usage of sqlmap against unauthorized targets is illegal.""",

    "ffuf": """\
/'___\\  /'___\\           /'___\\
/\\ \\__/ /\\ \\__/  __  __  /\\ \\__/
\\ \\ ,__\\\\ \\ ,__\\/\\ \\/\\ \\ \\ \\ ,__\\
 \\ \\ \\_/ \\ \\ \\_/\\ \\ \\_\\ \\ \\ \\ \\_/
  \\ \\_\\   \\ \\_\\  \\ \\____/  \\ \\_\\
   \\/_/    \\/_/   \\/___/    \\/_/  v2.1.0

 :: Method           : GET
 :: URL              : http://{target}/FUZZ
 :: Wordlist         : /usr/share/wordlists/dirb/common.txt
________________________________________________

admin                   [Status: 301, Size: 318, Words: 20]
api                     [Status: 200, Size: 1024, Words: 104]
login                   [Status: 200, Size: 4096, Words: 512]
uploads                 [Status: 403, Size: 285, Words: 22]
.git                    [Status: 200, Size: 234, Words: 18]
backup                  [Status: 200, Size: 51200, Words: 3400]
config                  [Status: 200, Size: 890, Words: 67]

:: Progress: [4614/4614] :: Job [1/1] :: 234 req/sec :: Duration: [0:00:19] ::""",

    "subfinder": """\
               __    _____           __
   _______  __/ /_  / __(_)___  ____/ /__  _____
  / ___/ / / / __ \\/ /_/ / __ \\/ __  / _ \\/ ___/
 (__  ) /_/ / /_/ / __/ / / / / /_/ /  __/ /
/____/\\__,_/_.___/_/ /_/_/ /_/\\__,_/\\___/_/

               projectdiscovery.io

[INF] Enumerating subdomains for {target}

api.{target}
mail.{target}
dev.{target}
staging.{target}
admin.{target}
vpn.{target}
cdn.{target}
assets.{target}
status.{target}

[INF] Found 9 subdomains for {target} in 4.2 seconds""",
}


def get_tools() -> list[ToolInfo]:
    return TOOL_REGISTRY


def get_mock_result(tool_id: str, target: str) -> ScanResult:
    template = _MOCK_OUTPUTS.get(tool_id)
    if template is None:
        output = f"[ERROR] Unknown tool: {tool_id}"
    else:
        output = template.replace("{target}", target or "unknown")

    return ScanResult(
        tool=tool_id,
        target=target,
        output=output,
        duration_ms=int(time.time() * 1000) % 5000 + 800,
    )
