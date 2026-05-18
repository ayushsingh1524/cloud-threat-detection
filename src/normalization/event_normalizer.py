from typing import Dict, Any

class EventNormalizer:
    @staticmethod
    def normalize_cloudtrail_event(event: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a raw CloudTrail event into a standard schema."""
        
        # Handle user identity which can have different formats
        user_identity = event.get('userIdentity', {})
        principal_id = user_identity.get('principalId', 'unknown')
        if ':' in principal_id:
            user = principal_id.split(':')[-1]
        else:
            user = user_identity.get('userName', principal_id)

        # Extract resource safely
        resources = event.get('resources', [])
        resource_name = resources[0].get('ARN', 'unknown') if resources else 'unknown'

        return {
            'event_time': event.get('eventTime'),
            'source_ip': event.get('sourceIPAddress', 'unknown'),
            'user_identity': user,
            'aws_region': event.get('awsRegion', 'unknown'),
            'event_name': event.get('eventName', 'unknown'),
            'resource': resource_name,
            'severity': 'low', # Base severity, can be overridden by detections
            'raw_event': event
        }
