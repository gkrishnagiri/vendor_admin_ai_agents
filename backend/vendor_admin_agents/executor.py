import json
from tools.browser_tools import BrowserSession
from services.llm_interpreter import interpret_step


class Executor:
    def __init__(self):
        self.browser = BrowserSession()

    def execute(self, steps, base_url="http://localhost:5173"):
        print("\n[Executor] Starting execution...")

        results = []

        self.browser.start()
        self.browser.navigate(base_url)

        for i, step in enumerate(steps):
            print(f"\n[Executor] Step {i+1}: {step}")

            try:
                action_json = interpret_step(step)

                print("[Executor] Interpreted Action:", action_json)

                action = action_json.get("action")

                if action == "click":
                    self.browser.click(action_json.get("selector"))

                elif action == "fill":
                    self.browser.fill(
                        action_json.get("selector"),
                        action_json.get("value", "")
                    )

                elif action == "navigate":
                    self.browser.navigate(action_json.get("url"))

                elif action == "wait":
                    self.browser.wait_for(action_json.get("selector"))

                else:
                    print(f"[Executor] Unknown action: {action}")

                results.append({
                    "step": step,
                    "status": "success"
                })

            except Exception as e:
                print(f"[Executor] Error: {e}")

                results.append({
                    "step": step,
                    "status": "failed",
                    "error": str(e)
                })

        print("\n[Executor] Execution complete")
        return results