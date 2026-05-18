import pytest
from pathlib import Path
from src.ci_cd.rule_validator import validate_rule

def test_all_detection_rules_valid():
    """Dynamically test all detection rules against the schema."""
    rules_dir = Path('src/detections')
    rule_files = list(rules_dir.glob('*.yml'))
    
    assert len(rule_files) > 0, "No detection rules found to test"
    
    for rule_file in rule_files:
        is_valid = validate_rule(str(rule_file))
        assert is_valid, f"Rule {rule_file.name} failed validation"
