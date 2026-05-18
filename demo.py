import yaml
from pathlib import Path
from src.analytics.sql_detection_engine import SQLDetectionEngine
from src.alerting.alert_generator import AlertGenerator

class MockSnowflakeClient:
    def execute_query(self, query: str) -> list[dict]:
        # Return mock malicious events for demonstration purposes
        if "AttachUserPolicy" in query:
            return [{
                "event_time": "2023-10-27T08:15:30Z",
                "user_identity": "compromised_admin_key",
                "event_name": "AttachUserPolicy",
                "source_ip": "185.15.22.4",
                "aws_region": "us-east-1",
                "resource": "arn:aws:iam::123456789012:user/target-user"
            }]
        elif "GetObject" in query:
            return [{
                "event_time": "2023-10-27T09:42:11Z",
                "user_identity": "data_extractor_role",
                "source_ip": "45.33.22.1",
                "resource": "arn:aws:s3:::customer-pii-data",
                "event_count": 850
            }]
        elif "ConsoleLogin" in query:
            return [{
                "event_time": "2023-10-27T10:05:00Z",
                "user_identity": "root",
                "source_ip": "112.55.22.11",
                "aws_region": "us-west-2"
            }]
        return []

def run_demo():
    print("=" * 60)
    print("🚀 STARTING CLOUD THREAT DETECTION PIPELINE DEMO 🚀")
    print("=" * 60)
    
    print("\n[INFO] Initializing SQL Detection Engine...")
    engine = SQLDetectionEngine()
    
    print("[INFO] Mocking Snowflake Client Connection...")
    engine.client = MockSnowflakeClient()
    
    print("[INFO] Loading Sigma-style YAML rules from src/detections/...")
    
    print("\n[INFO] Executing Detection Queries against Normalized CloudTrail Logs...\n")
    engine.run_detections()
    
    print("=" * 60)
    print("✅ DEMO COMPLETE ✅")
    print("=" * 60)

if __name__ == "__main__":
    run_demo()
