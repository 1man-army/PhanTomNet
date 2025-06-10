# agents/agent_logic.py – Logic Matrix & Priority Executor (⚙️ SIGN 2.0 Upgrade)
# ------------------------------------------------------------------------------
# This file governs operational directives.
# Now optimized for layered rule logic, tactical memory, and live updates.
# Authored by: PROFESSOR JOHNNY AI – YEAR 2025
# ------------------------------------------------------------------------------

import yaml
import json
import os
from datetime import datetime
from agents.PhantomAgentBase import PhantomAgentBase

class AgentLogic:
    def __init__(self):
        self.rules = []
        self.log = []
        self.rule_id_seq = 1

    def load_rule(self, rule_text, priority=5, issued_by="SYSTEM"):
        rule = {
            "id": f"RL-{self.rule_id_seq:04}",
            "rule": rule_text,
            "priority": priority,
            "loaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "issuer": issued_by
        }
        self.rule_id_seq += 1
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r["priority"])
        print(f"📘 Rule loaded → [P{priority}] [{rule['id']}] by {issued_by}: {rule_text}")

    def execute(self):
        print("🧠 Executing rule matrix by priority...")
        if not self.rules:
            print("⚠️ No rules to execute.")
            return

        for rule in self.rules:
            log_entry = f"⚙️ {rule['loaded_at']} | [{rule['id']}] [P{rule['priority']}] → {rule['rule']} (by {rule['issuer']})"
            print(log_entry)
            self.log.append(log_entry)

    def clear_rules(self):
        self.rules = []
        self.rule_id_seq = 1
        print("🗑️ All logic rules purged.")

    def rule_digest(self, verbose=False):
        if not self.rules:
            return "⚠️ No rules active in matrix."
        digest = "📘 Logic Rule Digest:\n"
        for rule in self.rules:
            summary = f"[{rule['id']}] P{rule['priority']} – {rule['rule']}"
            if verbose:
                summary += f" (Loaded: {rule['loaded_at']} | Issuer: {rule['issuer']})"
            digest += summary + "\n"
        return digest.strip()

    def export_rules(self):
        return [r.copy() for r in self.rules]

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
    mission = load_mission_from_yaml("agent_logic")
    logic = AgentLogic()
    # Load rules from YAML
    for rule in mission.get("rules", []):
        logic.load_rule(
            rule_text=rule["rule"],
            priority=rule.get("priority", 5),
            issued_by=rule.get("issued_by", "SYSTEM")
        )
    logic.execute()
    # Save logs as JSON
    save_agent_log("agent_logic", logic.log)
