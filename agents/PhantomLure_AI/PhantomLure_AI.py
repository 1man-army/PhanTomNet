# PhantomLure_AI – Lure/Phishing Deployment Agent for strategic bait operations.
# ------------------------------------------------------------------------------
# CENTRAL SIGNAL RELAY FOR ALL AGENTS – BUILT UNDER SIGN 2.0
# VOICE. SIGNAL. MEMORY. PURPOSE.
# Engineered by: Professor Johnny AI – 2025
# ------------------------------------------------------------------------------

from agents.PhantomAgentBase import PhantomAgentBase
import requests
from datetime import datetime
import random
import os
import json
import yaml
import httpagentparser  # Requires: pip install httpagentparser

class PhantomLureAI(PhantomAgentBase):
    def __init__(self):
        super().__init__("PhantomLure")
        self.lure_url = None
        self.deploy_log = []
        self.styles = ["clone", "spoof", "overlay", "geo-switch"]
        self.current_style = None
        self.fingerprint = f"PL-{random.randint(1000,9999)}"

    def deploy_lure(self, url=None, style=None):
        self.lure_url = url or self.mission.get("url")
        requested_style = style or self.mission.get("style")

        if not self.lure_url:
            msg = "❌ No URL provided for lure deployment."
            self.log(msg)
            return msg

        try:
            response = requests.get(self.lure_url, timeout=5)
            # Use a realistic User-Agent if not present
            ua_string = response.request.headers.get('User-Agent', 'Mozilla/5.0')
            device_info = httpagentparser.detect(ua_string)

            # Behavioral Style Decision (Smart Mapping)
            if "Mobile" in ua_string or "iPhone" in ua_string:
                self.current_style = "overlay"
            elif "Windows" in ua_string and "Chrome" in ua_string:
                self.current_style = "spoof"
            elif "Linux" in ua_string:
                self.current_style = "geo-switch"
            else:
                self.current_style = requested_style or random.choice(self.styles)

            result = {
                "fingerprint": self.fingerprint,
                "url": self.lure_url,
                "style": self.current_style,
                "status": response.status_code,
                "server": response.headers.get("Server", "unknown"),
                "user_agent": ua_string,
                "device_detected": device_info,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            self.deploy_log.append(result)
            self.log(f"🎯 Behavioral deploy [{self.current_style}] @ {self.lure_url} for UA: {ua_string}")
        except Exception as e:
            result = {
                "fingerprint": self.fingerprint,
                "url": self.lure_url,
                "style": "fail",
                "status": "fail",
                "error": str(e),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.deploy_log.append(result)
            self.log(f"⚠️ Lure failed at {self.lure_url}: {e}")

        self.save_agent_log("phish", result)
        return result

    def auto_execute(self):
        mission_url = self.mission.get("url")
        if mission_url:
            self.log("🔁 Auto-triggering deploy_lure from mission URL.")
            return self.deploy_lure(url=mission_url)
        else:
            self.log("🚫 No URL found in mission. Auto-execute skipped.")
            return "No mission URL available."

    def recent_deploys(self, count=5):
        return self.deploy_log[-count:] if self.deploy_log else ["🌀 No deployments yet."]

    def lure_summary(self):
        active = [d for d in self.deploy_log if d["status"] != "fail"]
        failed = [d for d in self.deploy_log if d["status"] == "fail"]
        return {
            "total_deploys": len(self.deploy_log),
            "success_count": len(active),
            "fail_count": len(failed),
            "last_style": self.current_style,
            "fingerprint": self.fingerprint
        }

    def execute(self):
        self.log("🕵️ PhantomLureAI active – executing lure deployment.")
        if not self.mission:
            self.log("❌ No mission assigned.")
            return
        self.auto_execute()

    def save_agent_log(self, agent_name, data):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        filename = f"{log_dir}/{agent_name}_{datetime.now():%Y%m%d_%H%M%S}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=2))
        return filename

    def load_mission_from_yaml(agent_name):
        yml_path = os.path.join("ops", "mission_targets", f"{agent_name}.yml")
        with open(yml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

if __name__ == "__main__":
    mission = PhantomLureAI.load_mission_from_yaml("PhantomLure_AI")
    agent = PhantomLureAI()
    agent.mission = mission
    agent.execute()
    agent.save_agent_log("PhantomLure_AI", agent.deploy_log)
