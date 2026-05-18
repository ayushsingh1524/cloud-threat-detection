import pytest
import yaml
from pathlib import Path
from src.analytics.sql_detection_engine import SQLDetectionEngine
from src.alerting.alert_generator import AlertGenerator

def test_privilege_escalation_rule_structure():
    rule_path = Path('src/detections/privilege_escalation.yml')
    with open(rule_path, 'r') as f:
        rule = yaml.safe_load(f)
        
    assert rule['title'] == 'Suspicious IAM Privilege Escalation'
    assert 'AttachUserPolicy' in rule['detection']['selection']['eventName']
    assert 'attack.t1098' in rule['tags']

def test_privilege_escalation_detection_logic(mocker):
    engine = SQLDetectionEngine()
    engine.client = mocker.MagicMock()
    engine.client.execute_query.return_value = [
        {
            "event_time": "2023-01-01T12:00:00Z",
            "user_identity": "attacker",
            "event_name": "AttachUserPolicy",
            "source_ip": "1.2.3.4",
            "aws_region": "us-east-1"
        }
    ]
    
    mocker.patch.object(AlertGenerator, 'generate_alert')
    
    # We mock load_rules to only load our specific rule to isolate the test
    rule_path = Path('src/detections/privilege_escalation.yml')
    with open(rule_path, 'r') as f:
        mock_rule = yaml.safe_load(f)
    
    mocker.patch.object(engine, 'load_rules', return_value=[mock_rule])
    
    engine.run_detections()
    
    # Verify alert was generated
    assert AlertGenerator.generate_alert.call_count == 1
    call_args = AlertGenerator.generate_alert.call_args[0]
    assert call_args[0]['title'] == 'Suspicious IAM Privilege Escalation'
    assert call_args[1]['event_name'] == 'AttachUserPolicy'
