def detect_metric_anomalies(events, threshold = 2.0):
    """Detect significant increases in metrics
    
    threshold = 2.0 means a metric must be atleast twice its baseline to be flagged
    """
    metric_events = [ event for event in events if event["type"] == "metric" ]

    metrics = {}

    for event in metric_events:
        name = event["name"]

        metrics.setdefault(name, []).append(event)

    anomalies = []

    for name, measurements in metrics.items():
        measurements.sort(
            key = lambda event: event["timestamp"]
        )
        if len(measurements) < 2:
            continue

        baseline = measurements[0]["value"]

        for event in measurements[1:]:
            current_value = event["value"]
            if not isinstance(current_value, (int, float)):
                continue
            if not isinstance(baseline, (int, float)):
                continue
            if baseline <= 0:
                continue
            ratio = current_value / baseline

            if ratio >= threshold:
                increase_percent = (
                    (current_value - baseline) / baseline
                )*100

                anomalies.append({
                    "timestamp": event["timestamp"],
                    "metric": name,
                    "baseline": baseline,
                    "observed": current_value,
                    "increase_percent": round(increase_percent, 2),
                    "severity": "HIGH"
                })
    return anomalies