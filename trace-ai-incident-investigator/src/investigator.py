from correlator import correlate_events
from metrics_analyzer import detect_metric_anomalies


def investigate_incident(incident):
    """
    Evaluate possible causes of an incident using
    anomalies and events recorded in the incident data.
    """

    events = incident["events"]

    # Step 1: Collect relevant evidence.
    anomalies = detect_metric_anomalies(events)
    correlations = correlate_events(events)

    # Step 2: Initialize the hypotheses.
    hypotheses = {
        "deployment_regression": {
            "title": "A recent deployment introduced a problem",
            "score": 0,
            "supporting_evidence": [],
        },
        "database_problem": {
            "title": "The database experienced a problem",
            "score": 0,
            "supporting_evidence": [],
        },
        "external_dependency_problem": {
            "title": "An external dependency caused failures",
            "score": 0,
            "supporting_evidence": [],
        },
    }

    # Step 3: Examine the anomalies.
    for anomaly in anomalies:
        metric_name = anomaly["metric"]

        if metric_name == "database_latency_ms":
            hypotheses["database_problem"]["score"] += 3

            hypotheses["database_problem"][
                "supporting_evidence"
            ].append(
                f"Database latency increased from "
                f"{anomaly['baseline']} ms to "
                f"{anomaly['observed']} ms."
            )

    # Step 4: Examine events correlated with deployments.
    for correlation in correlations:
        for event in correlation["related_events"]:

            if event["type"] == "metric":
                if event["name"] == "database_latency_ms":

                    hypotheses["deployment_regression"][
                        "score"
                    ] += 2

                    hypotheses["deployment_regression"][
                        "supporting_evidence"
                    ].append(
                        "Database latency increased "
                        "after a deployment."
                    )

            if event["type"] == "log":
                if event["name"] == "DatabaseTimeout":

                    hypotheses["database_problem"][
                        "score"
                    ] += 2

                    hypotheses["database_problem"][
                        "supporting_evidence"
                    ].append(
                        "A database timeout was recorded."
                    )

    # Step 5: Rank the hypotheses.
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
