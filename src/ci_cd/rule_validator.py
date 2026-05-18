import yamale
import sys
import yaml

# Basic schema for our Sigma-style rules
SCHEMA_YAML = """
title: str(required=True)
id: str(required=True)
status: str(required=False)
description: str(required=True)
author: str(required=False)
logsource: map(required=True)
detection: map(required=True)
level: str(required=True)
tags: list(str(), required=False)
falsepositives: list(str(), required=False)
sql_mapping: map(required=True)
"""

def validate_rule(file_path: str) -> bool:
    print(f"Validating {file_path}...")
    try:
        schema = yamale.make_schema(content=SCHEMA_YAML)
        data = yamale.make_data(file_path)
        yamale.validate(schema, data)
        
        # Additional custom validation
        with open(file_path, 'r') as f:
            rule_data = yaml.safe_load(f)
            if 'query' not in rule_data.get('sql_mapping', {}):
                print(f"Error: {file_path} missing 'query' in 'sql_mapping'")
                return False
                
        print(f"✅ {file_path} is valid.")
        return True
    except ValueError as e:
        print(f"❌ Validation failed for {file_path}:\n{e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error validating {file_path}:\n{e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rule_validator.py <path_to_rule.yml>")
        sys.exit(1)
    
    success = True
    for file_path in sys.argv[1:]:
        if not validate_rule(file_path):
            success = False
            
    if not success:
        sys.exit(1)
