import json
import boto3
import os
from src.mitre_mapping.mapper import MITREMapper

class AlertGenerator:
    def __init__(self):
        # Allow local testing without SNS
        self.sns_topic_arn = os.environ.get('SNS_ALERT_TOPIC_ARN')
        if self.sns_topic_arn:
            self.sns_client = boto3.client('sns')
        else:
            self.sns_client = None

    def generate_alert(self, rule: dict, match_data: dict):
        """Format and send an alert based on a detection rule and Snowflake results."""
        
        tags = rule.get('tags', [])
        
        alert_payload = {
            "threat": rule.get('title', 'Unknown Threat'),
            "severity": rule.get('level', 'info').upper(),
            "timestamp": str(match_data.get('event_time', match_data.get('EVENT_TIME', 'unknown'))),
            "user": match_data.get('user_identity', match_data.get('USER_IDENTITY', 'unknown')),
            "source_ip": match_data.get('source_ip', match_data.get('SOURCE_IP', 'unknown')),
            "aws_region": match_data.get('aws_region', match_data.get('AWS_REGION', 'unknown')),
            "event_name": match_data.get('event_name', match_data.get('EVENT_NAME', 'unknown')),
            "resource": match_data.get('resource', match_data.get('RESOURCE', 'unknown')),
            "detection_id": rule.get('id', 'unknown')
        }

        # Enrich with MITRE ATT&CK
        alert_payload = MITREMapper.enrich_alert_with_mitre(alert_payload, tags)

        formatted_alert = (
            f"[THREAT ALERT]\n"
            f"Threat: {alert_payload['threat']}\n"
            f"Severity: {alert_payload['severity']}\n"
            f"User: {alert_payload['user']}\n"
            f"Event: {alert_payload['event_name']}\n"
            f"Region: {alert_payload['aws_region']}\n"
        )
        
        if alert_payload.get('mitre_attack'):
            mitre_str = ", ".join([f"{m['technique_id']} ({m['tactic']})" for m in alert_payload['mitre_attack']])
            formatted_alert += f"MITRE: {mitre_str}\n"

        print("-" * 40)
        print(formatted_alert)
        print("-" * 40)

        if self.sns_client and self.sns_topic_arn:
            self.sns_client.publish(
                TopicArn=self.sns_topic_arn,
                Subject=f"Threat Alert: {alert_payload['threat']}",
                Message=json.dumps(alert_payload, indent=2)
            )
