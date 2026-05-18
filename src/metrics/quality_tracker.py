import json
from datetime import datetime

class QualityTracker:
    def __init__(self, output_file='detection_metrics.json'):
        self.metrics_file = output_file
        self.metrics = self._load_metrics()

    def _load_metrics(self) -> dict:
        try:
            with open(self.metrics_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_metrics(self):
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)

    def record_performance(self, detection_id: str, true_positives: int, false_positives: int, false_negatives: int, latency_seconds: int):
        """Record the performance of a specific detection rule."""
        
        # Calculate Precision and Recall safely
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        false_positive_rate = false_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0

        if detection_id not in self.metrics:
            self.metrics[detection_id] = []

        self.metrics[detection_id].append({
            "timestamp": datetime.utcnow().isoformat(),
            "precision": round(precision, 2),
            "recall": round(recall, 2),
            "false_positive_rate": round(false_positive_rate, 2),
            "mttd": f"{latency_seconds}s",
            "raw_counts": {
                "tp": true_positives,
                "fp": false_positives,
                "fn": false_negatives
            }
        })
        self._save_metrics()

    def get_latest_metrics(self, detection_id: str) -> dict:
        if detection_id in self.metrics and self.metrics[detection_id]:
            return self.metrics[detection_id][-1]
        return {}
