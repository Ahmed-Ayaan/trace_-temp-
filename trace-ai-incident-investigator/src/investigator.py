from correlator import correlate_events
from metrics_analyzer import detect_metric_anomalies


def investigate_incident(incident):
    events = incident["events"]

    # Step 1: Analyze the incident.
    anomalies = detect_metric_anomalies(events)
    correlations = correlate_events(events)

    # Step 2: Create structured hypotheses.
    hypotheses = {
        "database_problem": {
            "title": "A database-related problem",
            "score": 0,
            "supporting_evidence": [],
            "contradicting_evidence": [],
            "missing_evidence": [
                "Database health and connection metrics",
                "Database logs around the incident",
            ],
            "status": "untested",
        },
        "deployment_regression": {
            "title": "The recent deployment introduced a problem",
            "score": 0,
            "supporting_evidence": [],
            "contradicting_evidence": [],
            "missing_evidence": [
                "Deployment change log",
                "Comparison with the previous version",
            ],
            "status": "untested",
        },
        "external_dependency_problem": {
            "title": "An external dependency caused failures",
            "score": 0,
            "supporting_evidence": [],
            "contradicting_evidence": [],
            "missing_evidence": [
                "External service health information",
                "Dependency error logs",
            ],
            "status": "untested",
        },
    }

    # Step 3: Examine metric anomalies.
    for anomaly in anomalies:
        if anomaly["metric"] == "database_latency_ms":
            hypothesis = hypotheses["database_problem"]

            hypothesis["score"] += 3

            hypothesis["supporting_evidence"].append(
                {
                    "type": "metric_anomaly",
                    "description": (
                        f"Database latency increased from "
                        f"{anomaly['baseline']} ms to "
                        f"{anomaly['observed']} ms."
                    ),
                    "timestamp": anomaly["timestamp"],
                }
            )

    # Step 4: Examine events associated with deployments.
    for correlation in correlations:
        deployment = correlation["deployment"]

        for event in correlation["related_events"]:

            if (
                event["type"] == "metric"
                and event["name"] == "database_latency_ms"
            ):
                hypothesis = hypotheses["deployment_regression"]

                hypothesis["score"] += 2

                hypothesis["supporting_evidence"].append(
                    {
                        "type": "temporal_relationship",
                        "description": (
                            "Database latency increased after "
                            f"deployment {deployment['value']}."
                        ),
                        "timestamp": event["timestamp"],
                    }
                )

            if (
                event["type"] == "log"
                and event["name"] == "DatabaseTimeout"
            ):
                hypothesis = hypotheses["database_problem"]

                hypothesis["score"] += 2

                hypothesis["supporting_evidence"].append(
                    {
                        "type": "error_log",
                        "description": (
                            "A database timeout was recorded."
                        ),
                        "timestamp": event["timestamp"],
                    }
                )

    # Step 5: Assign preliminary statuses.
    for hypothesis in hypotheses.values():
        if hypothesis["supporting_evidence"]:
            hypothesis["status"] = "plausible"

    # Step 6: Rank the hypotheses.
    ranked_hypotheses = sorted(
        hypotheses.values(),
        key=lambda hypothesis: hypothesis["score"],
        reverse=True,
    )

    return {
        "incident_id": incident["incident_id"],
        "anomalies": anomalies,
        "hypotheses": ranked_hypotheses,
    }