# agents/state_manager.py – Real-time Agent State Tracker (SIGN 2.0 Upgrade)
# ------------------------------------------------------------------------------
# CORE MEMORY MAP FOR ALL SIGN 2.0 AI AGENTS
# ENGINEERED BY: PROFESSOR JOHNNY AI | YEAR: 2025
# ------------------------------------------------------------------------------

from agents.PhantomAgentBase import PhantomAgentBase
from datetime import datetime
import json
import os
import yaml

class StateManager:
    def __init__(self, retention_limit=100, heartbeat_threshold=60):
        self.state = {}
        self.heartbeat = {}
        self.retention_limit = retention_limit
        self.heartbeat_threshold = heartbeat_threshold
        self.event_listeners = []

    # --- Event System ---
    def add_event_listener(self, event_type, callback):
        self.event_listeners.append({"event": event_type, "callback": callback})

    def notify_listeners(self, event_type, data):
        for listener in self.event_listeners:
            if listener["event"] == event_type:
                listener["callback"](data)

    # --- State Management ---
    def validate_state_transition(self, agent, key, new_value):
        current_value = self.state.get(agent, {}).get(key, None)
        if key == "status" and current_value == "inactive" and new_value != "active":
            print(f"⚠️ Invalid state transition for {agent}: {current_value} → {new_value}")
            return False
        return True

    def prune_old_versions(self, agent):
        versions = self.state.get(agent, {}).get("_versions", [])
        if len(versions) > self.retention_limit:
            self.state[agent]["_versions"] = versions[-self.retention_limit:]
            print(f"🧹 Pruned old versions for {agent} to retain the latest {self.retention_limit} versions.")

    def update_state(self, agent, key, value):
        if not self.validate_state_transition(agent, key, value):
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if agent not in self.state:
            self.state[agent] = {"_log": [], "_versions": []}

        self.prune_old_versions(agent)

        self.state[agent][key] = value
        self.state[agent]["_log"].append(f"[{timestamp}] {key} → {value}")
        snapshot = {k: v for k, v in self.state[agent].items() if not k.startswith("_")}
        self.state[agent]["_versions"].append({
            "timestamp": timestamp,
            "snapshot": snapshot
        })

        self.heartbeat[agent] = timestamp
        print(f"🧬 {agent} updated → {key}: {value}")
        self.notify_listeners("state_update", {"agent": agent, "key": key, "value": value})

    def rollback_state(self, agent, timestamp):
        versions = self.state.get(agent, {}).get("_versions", [])
        for version in versions:
            if version["timestamp"] == timestamp:
                # Only restore non-log/version keys
                for k in list(self.state[agent].keys()):
                    if not k.startswith("_"):
                        del self.state[agent][k]
                self.state[agent].update(version["snapshot"])
                print(f"🌀 Rolled back {agent} to state at {timestamp}")
                return
        print(f"⚠️ No matching state found for {timestamp}!")

    def check_heartbeat(self, agent):
        last_heartbeat = self.heartbeat.get(agent, None)
        if last_heartbeat:
            delta = (datetime.now() - datetime.strptime(last_heartbeat, "%Y-%m-%d %H:%M:%S")).total_seconds()
            if delta > self.heartbeat_threshold:
                print(f"⚠️ {agent} has been inactive for {delta} seconds!")
            else:
                print(f"🧬 {agent} heartbeat is within threshold.")

    # --- State Accessors ---
    def get_state(self, agent):
        return self.state.get(agent, {})

    def get_log(self, agent):
        return self.state.get(agent, {}).get("_log", [])

    def get_versions(self, agent, limit=5):
        return self.state.get(agent, {}).get("_versions", [])[-limit:]

    def clear_agent(self, agent):
        if agent in self.state:
            del self.state[agent]
        if agent in self.heartbeat:
            del self.heartbeat[agent]
        print(f"🧹 State cleared for: {agent}")

    def global_state_dump(self):
        clean_state = {agent: {k: v for k, v in data.items() if not k.startswith("_")}
                       for agent, data in self.state.items()}
        return clean_state

    def export_as_json(self):
        return json.dumps(self.global_state_dump(), indent=2)

    def status_summary(self):
        print("📡 Agent Heartbeat Summary:")
        for agent, ts in self.heartbeat.items():
            print(f"🧠 {agent} → Last update: {ts}")

    # --- Mission Center Integration ---
    def execute(self, mission=None):
        print("🛰️ StateManager active – mission-based state update.")
        if not mission:
            print("❌ No mission assigned.")
            return
        agent = mission.get("agent", "UnknownAgent")
        key = mission.get("update_key", "status")
        value = mission.get("update_value", "active")
        self.update_state(agent, key, value)
        self.status_summary()

# --- Logging Utility ---
def save_agent_log(agent_name, data, format="json"):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    filename = f"{log_dir}/{agent_name}_{datetime.now():%Y%m%d_%H%M%S}.{format}"

    if format == "json":
        with open(filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=2))
    elif format == "html":
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"<html><body><pre>{json.dumps(data, indent=2)}</pre></body></html>")
    elif format == "md":
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Agent Log\n\n```json\n{json.dumps(data, indent=2)}\n```")
    else:
        print("Unsupported log format.")
        return None
    return filename

# --- Mission Loader ---
def load_mission_from_yaml(agent_name):
    yml_path = os.path.join("ops", "mission_targets", f"{agent_name}.yml")
    with open(yml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    mission = load_mission_from_yaml("state_manager")
    sm = StateManager()
    sm.execute(mission)
    print(sm.export_as_json())
    save_agent_log("state_manager", sm.global_state_dump())
