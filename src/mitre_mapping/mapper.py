class MITREMapper:
    TACTICS = {
        "t1098": "Account Manipulation",
        "t1078": "Valid Accounts",
        "t1530": "Data from Cloud Storage",
        "t1485": "Data Destruction",
        "t1562": "Defense Evasion"
    }

    @classmethod
    def get_tactic_name(cls, technique_id: str) -> str:
        """Map a MITRE technique ID to its human-readable name."""
        clean_id = technique_id.lower().replace("attack.", "")
        return cls.TACTICS.get(clean_id, "Unknown Tactic")

    @classmethod
    def enrich_alert_with_mitre(cls, alert: dict, tags: list[str]) -> dict:
        """Enrich an alert dict with MITRE ATT&CK information."""
        mitre_info = []
        for tag in tags:
            if tag.startswith('attack.t'):
                technique_id = tag.split('.')[-1]
                tactic_name = cls.get_tactic_name(technique_id)
                mitre_info.append({
                    "technique_id": technique_id.upper(),
                    "tactic": tactic_name
                })
        alert['mitre_attack'] = mitre_info
        return alert
