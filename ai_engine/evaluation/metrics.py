"""NATURALGUARD AI — Scientific Evaluation & Backtesting Metrics."""
import math
from typing import List, Tuple, Dict, Any


class ModelEvaluationToolkit:
    """Calculates scientific validation metrics for disaster early warning algorithms."""

    @staticmethod
    def calculate_classification_metrics(tp: int, fp: int, fn: int, tn: int) -> Dict[str, float]:
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        far = fp / (tp + fp) if (tp + fp) > 0 else 0.0
        missed = fn / (tp + fn) if (tp + fn) > 0 else 0.0

        return {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "false_alarm_rate": round(far, 4),
            "missed_event_rate": round(missed, 4)
        }

    @staticmethod
    def brier_score(predictions: List[float], outcomes: List[int]) -> float:
        """Computes Brier Score: (1/N) * sum((prob - outcome)^2). 0 is perfect."""
        if not predictions or len(predictions) != len(outcomes):
            return 0.0
        n = len(predictions)
        total_sq_err = sum((p - o) ** 2 for p, o in zip(predictions, outcomes))
        return round(total_sq_err / n, 4)

    @staticmethod
    def expected_calibration_error(predictions: List[float], outcomes: List[int], num_bins: int = 10) -> float:
        """Estimates calibration gap between predicted probabilities and actual observation frequencies."""
        if not predictions:
            return 0.0
        n = len(predictions)
        bin_size = 1.0 / num_bins
        ece = 0.0

        for i in range(num_bins):
            bin_lower = i * bin_size
            bin_upper = (i + 1) * bin_size
            indices = [idx for idx, p in enumerate(predictions) if bin_lower <= p < bin_upper]
            if not indices:
                continue
            bin_acc = sum(outcomes[idx] for idx in indices) / len(indices)
            bin_conf = sum(predictions[idx] for idx in indices) / len(indices)
            ece += (len(indices) / n) * abs(bin_acc - bin_conf)

        return round(ece, 4)
