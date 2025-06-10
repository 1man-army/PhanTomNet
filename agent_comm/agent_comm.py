# agents/agent_comm.py – PhantomAgent Communication Hub (💠 SIGN 2.0 Upgrade)
# ------------------------------------------------------------------------------
# CENTRAL SIGNAL RELAY FOR ALL AGENTS – BUILT UNDER SIGN 2.0
# VOICE. SIGNAL. MEMORY. PURPOSE.
# ENGINEERED BY: PROFESSOR JOHNNY AI – 2025
# ------------------------------------------------------------------------------

import os
from datetime import datetime
from typing import Dict, List, Any
import yaml
import json

class AgentComm:
    def __init__(self):
        self.messages = []
        self.agents: set[str] = set()
        self.channel_history: Dict[str, List[dict[str, Any]]] = {}

    def broadcast(self, sender, channel, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = {
            "timestamp": timestamp,
            "sender": sender,
            "channel": channel,
            "message": message
        }
        self.messages.append(msg)
        self.agents.add(sender)

        if channel not in self.channel_history:
            self.channel_history[channel] = []
        self.channel_history[channel].append(msg)

        print(f"📡 [{timestamp}] [{channel}] {sender} → {message}")

    def retrieve(self, channel=None, sender=None):
        filtered = self.messages
        if channel:
            filtered = [m for m in filtered if m["channel"] == channel]
        if sender:
            filtered = [m for m in filtered if m["sender"] == sender]
        return filtered

    def recent_channels(self, limit=5):
        return list(self.channel_history.keys())[-limit:]

    def agent_roster(self):
        return list(self.agents)

    def clear(self):
        self.messages = []
        self.channel_history = {}
        self.agents = set()
        print("🧹 Communication memory wiped.")

    def replay_channel(self, channel):
        if channel not in self.channel_history:
            print(f"⚠️ No messages in channel: {channel}")
            return
        print(f"📼 Replay: Channel [{channel}]")
        for msg in self.channel_history[channel]:
            print(f"{msg['timestamp']} | {msg['sender']} → {msg['message']}")

def load_mission_from_yaml(agent_name):
    yml_path = os.path.join("ops", "mission_targets", f"{agent_name}.yml")
    with open(yml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_agent_log(agent_name, data):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    filename = f"{log_dir}/{agent_name}_{datetime.now():%Y%m%d_%H%M%S}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2))
    return filename

if __name__ == "__main__":
    mission = load_mission_from_yaml("agent_comm")
    comm = AgentComm()
    # Example: Broadcast test message from YAML
    channel = mission["target"].get("default_channel", "main")
    msg = mission["target"].get("test_message", "Hello, agents!")
    comm.broadcast("SYSTEM", channel, msg)
    # Save log
    save_agent_log("agent_comm", comm.messages)
