import os
import yaml
from pathlib import Path
from src.analytics.snowflake_client import SnowflakeClient
from src.alerting.alert_generator import AlertGenerator

class SQLDetectionEngine:
    def __init__(self):
        # Allow running without Snowflake for local testing
        if os.environ.get('SNOWFLAKE_ACCOUNT'):
            self.client = SnowflakeClient()
        else:
            self.client = None
        self.alert_gen = AlertGenerator()

    def load_rules(self, rules_dir: str) -> list[dict]:
        """Load YAML detection rules from directory."""
        rules = []
        path = Path(rules_dir)
        for rule_file in path.glob('*.yml'):
            with open(rule_file, 'r') as f:
                rules.append(yaml.safe_load(f))
        return rules

    def run_detections(self, rules_dir: str = 'src/detections'):
        """Execute all SQL-based detections against Snowflake."""
        if not self.client:
            print("Snowflake credentials not found. Skipping execution.")
            return

        rules = self.load_rules(rules_dir)
        for rule in rules:
            query = rule.get('sql_mapping', {}).get('query')
            if not query:
                continue
                
            print(f"Running detection: {rule['title']}")
            results = self.client.execute_query(query)
            
            if results:
                print(f"Found {len(results)} matches for {rule['title']}")
                for match in results:
                    self.alert_gen.generate_alert(rule, match)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--deploy-all', action='store_true', help='Deploy all rules (mock action for CI)')
    args = parser.parse_args()

    engine = SQLDetectionEngine()
    if args.deploy_all:
        # Deploy step requires Snowflake credentials; skip if not provided
        if not (os.getenv('SNOWFLAKE_ACCOUNT') and os.getenv('SNOWFLAKE_USER') and os.getenv('SNOWFLAKE_PASSWORD')):
            print("⚠️ Skipping deployment: Snowflake credentials not set in environment.")
        else:
            print("Deploying rules to Snowflake scheduled tasks...")
            # Real deployment logic would go here
    else:
        engine.run_detections()
