"""
Runs the combined detector against a labelled synthetic dataset
and computes precision, recall, and F1 per entity type.
"""

from collections import defaultdict
from data_generator import generate_dataset, LabelledExample
from combined_detector import CombinedDetector


def spans_overlap(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    """Two spans count as a match if they overlap at all."""
    return a_start < b_end and b_start < a_end


def evaluate(examples: list[LabelledExample], detector: CombinedDetector) -> dict:
    """
    For each entity type, count true positives, false positives,
    and false negatives, then compute precision, recall, F1.
    """
    stats = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})

    for example in examples:
        predicted = detector.detect(example.text)
        ground_truth = example.entities

        matched_gt = set()
        matched_pred = set()

        for i, pred in enumerate(predicted):
            for j, gt in enumerate(ground_truth):
                if j in matched_gt:
                    continue
                if pred.entity_type == gt.entity_type and spans_overlap(
                    pred.start, pred.end, gt.start, gt.end
                ):
                    stats[gt.entity_type]["tp"] += 1
                    matched_gt.add(j)
                    matched_pred.add(i)
                    break

        for i, pred in enumerate(predicted):
            if i not in matched_pred:
                stats[pred.entity_type]["fp"] += 1

        for j, gt in enumerate(ground_truth):
            if j not in matched_gt:
                stats[gt.entity_type]["fn"] += 1

    results = {}
    for entity_type, counts in stats.items():
        tp, fp, fn = counts["tp"], counts["fp"], counts["fn"]
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )
        results[entity_type] = {
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
            "tp": tp,
            "fp": fp,
            "fn": fn,
        }

    return results


if __name__ == "__main__":
    dataset = generate_dataset(50)
    
    detector = CombinedDetector()
    results = evaluate(dataset, detector)
    for example in dataset:
        for ent in example.entities:
            if ent.entity_type == "CREDIT_CARD":
                print(repr(ent.text))

    print(f"{'ENTITY TYPE':<15} {'PRECISION':<10} {'RECALL':<10} {'F1':<10} {'TP':<5} {'FP':<5} {'FN':<5}")
    for entity_type, metrics in results.items():
        print(f"{entity_type:<15} {metrics['precision']:<10} {metrics['recall']:<10} {metrics['f1']:<10} {metrics['tp']:<5} {metrics['fp']:<5} {metrics['fn']:<5}")