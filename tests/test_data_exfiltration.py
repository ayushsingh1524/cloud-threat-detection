import pytest
import yaml
from pathlib import Path
from src.analytics.sql_detection_engine import SQLDetectionEngine
from src.alerting.alert_generator import AlertGenerator

def test_data_exfiltration_rule_structure():
    rule_path = Path('src/detections/data_exfiltration.yml')
    with open(rule_path, 'r') as f:
        rule = yaml.safe_load(f)
        
    assert rule['title'] == 'Suspicious Data Exfiltration from S3'
    assert 'GetObject' in rule['detection']['selection']['eventName']
    assert 'attack.t1530' in rule['tags']

def test_data_exfiltration_detection_logic(mocker):
    engine = SQLDetectionEngine()
    engine.client = mocker.MagicMock()
    # Mocking that a user downloaded > 100 objects
    engine.client.execute_query.return_value = [
        {
            "event_time": "2023-01-01T12:00:00Z",
            "user_identity": "compromised_user",
            "source_ip": "1.2.3.4",
            "resource": "arn:aws:s3:::sensitive-bucket",
            "event_count": 500
        }
    ]
    
    mocker.patch.object(AlertGenerator, 'generate_alert')
    
    rule_path = Path('src/detections/data_exfiltration.yml')
    with open(rule_path, 'r') as f:
        mock_rule = yaml.safe_load(f)
    
    mocker.patch.object(engine, 'load_rules', return_value=[mock_rule])
    
    engine.run_detections()
    
    # Verify alert was generated
    assert AlertGenerator.generate_alert.call_count == 1
    call_args = AlertGenerator.generate_alert.call_args[0]
    assert call_args[0]['title'] == 'Suspicious Data Exfiltration from S3'
    assert call_args[1]['event_count'] == 500
