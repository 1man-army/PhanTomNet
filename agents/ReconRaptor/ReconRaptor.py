# ReconRaptor – Deep Reconnaissance Agent for port scanning, OS detection, and banner grabbing.
# ------------------------------------------------------------------------------
# CENTRAL SIGNAL RELAY FOR ALL AGENTS – BUILT UNDER SIGN 2.0
# VOICE. SIGNAL. MEMORY. PURPOSE.
# Engineered by: Professor Johnny AI – 2025
# ------------------------------------------------------------------------------

import socket, os, threading, platform, subprocess, json
from datetime import datetime
from agents.PhantomAgentBase import PhantomAgentBase

class ReconRaptor(PhantomAgentBase):
    def __init__(self):
        super().__init__("ReconRaptor")
        self.open_ports = []
        self.banners = {}
        self.lock = threading.Lock()

    def execute(self):
        print("🦅 FINAL FORM: ReconRaptor – DOMINATING NETWORK PERCEPTION")
        if not self.mission:
            print("❌ No mission file loaded.")
            return

        target_ip = self.mission.get("ip")
        scan_depth = int(self.mission.get("scan_depth", 3))
        ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 8080][:scan_depth * 5]

        if not target_ip:
            print("❌ No IP target found.")
            return

        # Clear previous results for repeatable runs
        self.open_ports.clear()
        self.banners.clear()

        threads = [threading.Thread(target=self.scan_port, args=(target_ip, p)) for p in ports]
        for t in threads: t.start()
        for t in threads: t.join()

        os_guess = self.os_fingerprint(target_ip)

        log = {
            "target_ip": target_ip,
            "open_ports": sorted(self.open_ports),
            "banners": self.banners,
            "os_guess": os_guess,
            "status": "Recon Completed",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.logs.append(log)
        self.generate_terminal_report(log)
        self.generate_html_report(log)
        self.save_agent_log("ReconRaptor", log)

    def scan_port(self, ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    with self.lock:
                        self.open_ports.append(port)
                    try:
                        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                        banner = sock.recv(1024).decode(errors="ignore").strip()
                    except Exception:
                        banner = "No banner"
                    service = self.guess_service(port, banner)
                    with self.lock:
                        self.banners[port] = f"{service} | {banner}"
        except Exception:
            pass

    def guess_service(self, port, banner):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 139: "NetBIOS", 143: "IMAP",
            443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP", 8080: "Proxy/HTTP"
        }
        if "Apache" in banner: return "Apache"
        if "nginx" in banner: return "Nginx"
        if "IIS" in banner: return "Microsoft IIS"
        return services.get(port, "Unknown")

    def os_fingerprint(self, ip):
        try:
            cmd = ["ping", "-c", "1", ip] if platform.system() != "Windows" else ["ping", "-n", "1", ip]
            result = subprocess.run(cmd, capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if "TTL=" in line or "ttl=" in line:
                    ttl = int([s for s in line.split() if "ttl=" in s.lower()][0].split('=')[1])
                    if ttl >= 128:
                        return "Windows (TTL ~128)"
                    elif ttl >= 64:
                        return "Linux/Unix (TTL ~64)"
                    else:
                        return f"Unknown TTL={ttl}"
        except Exception:
            return "OS Detection Failed"
        return "OS Detection Failed"

    def generate_terminal_report(self, data):
        try:
            from colorama import Fore, Style, init
            init(autoreset=True)
            print(f"\n{Fore.RED}🚨 Recon Summary for {data['target_ip']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}🧬 OS Guess: {data['os_guess']}{Style.RESET_ALL}")
            for port in data['open_ports']:
                banner = data['banners'].get(port, "N/A")
                print(f"{Fore.YELLOW}🔓 Port {port}: {banner}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}📦 Recon Complete at {data['timestamp']}{Style.RESET_ALL}\n")
        except ImportError:
            print("\nRecon Summary (colorama not installed):")
            print(f"OS Guess: {data['os_guess']}")
            for port in data['open_ports']:
                banner = data['banners'].get(port, "N/A")
                print(f"Port {port}: {banner}")
            print(f"Recon Complete at {data['timestamp']}\n")

    def generate_html_report(self, data):
        html = f"""
        <html><head><title>ReconRaptor Report</title></head><body>
        <h1 style='color:red;'>🦅 Recon Report – {data['target_ip']}</h1>
        <p><strong>OS Fingerprint:</strong> {data['os_guess']}</p>
        <h2>Open Ports</h2><ul>
        {''.join([f"<li><strong>{port}</strong>: {data['banners'][port]}</li>" for port in data['open_ports']])}
        </ul>
        <p><em>Scan Timestamp:</em> {data['timestamp']}</p>
        </body></html>
        """
        filename = f"logs/ReconRaptor_HTML_{datetime.now():%Y%m%d_%H%M%S}.html"
        os.makedirs("logs", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"🧾 HTML report saved → {filename}")

    def save_agent_log(self, agent_name, data):
        os.makedirs("logs", exist_ok=True)
        filename = f"logs/{agent_name}_{datetime.now():%Y%m%d_%H%M%S}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return filename

def load_mission_from_yaml(agent_name):
    yml_path = os.path.join("ops", "mission_targets", f"{agent_name}.yml")
    with open(yml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    mission = load_mission_from_yaml("ReconRaptor")
    agent = ReconRaptor()
    agent.mission = mission
    agent.execute()
    save_agent_log("ReconRaptor", agent.logs)