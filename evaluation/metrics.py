def calculate_accuracy(correct, total):
    return (correct / total * 100) if total else 0.0

def calculate_success_rate(successes, attempts):
    return (successes / attempts * 100) if attempts else 0.0

def calculate_metrics(stats):
    return {
        "generated": stats.get("generated", 0),
        "unique": stats.get("unique", 0),
        "solved": stats.get("solved", 0),
        "hints": stats.get("hints", 0),
        "validated": stats.get("validated", 0),
    }
