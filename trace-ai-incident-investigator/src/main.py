import json
from pathlib import Path
from metrics_analyzer import detect_metric_anomalies
from correlator import build_timeline, correlate_events
from investigator import investigate_incident


def load_incident(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        incident = json.load(file)
    return incident


def display_incident(incident):
    print("=" * 50)
    print("TRACE — AI INCIDENT INVESTIGATOR")
    print("=" * 50)

    print(f"Incident ID: {incident['incident_id']}")
    print(f"Service: {incident['service']}")
    print(f"Description: {incident['description']}")

    print("\nINCIDENT EVENTS")
    print("-" * 50)

    events = sorted(
        incident["events"],
        key=lambda event: event["timestamp"]
    )
    for event in events:
        print(
            f"{event['timestamp']} | "
            f"{event['type']} | "
            f"{event['name']} | "
            f"{event['value']}"
        )


def display_anomalies(incident):
    anomalies = detect_metric_anomalies(incident["events"])
    print("\nDETECTED ANOMALIES")
    print("-" * 50)
    if not anomalies:
        print("No anomalies detected.")
        return
    for anomaly in anomalies:
        print(f"Metric: {anomaly['metric']}")
        print(f"Time: {anomaly['timestamp']}")
        print(f"Baseline: {anomaly['baseline']}")
        print(f"Observed: {anomaly['observed']}")
        print(f"Increase: {anomaly['increase_percent']}%")
        print(f"Severity: {anomaly['severity']}")
        print("-" * 50)


def diaplay_timeline(incident):
    timeline = build_timeline(incident["events"])
    print("\nINCIDENT TIMELINE")
    print("-" * 60)
    for event in timeline:
        print(f"{event['timestamp']} | "
            f"{event['type'].upper():10} | "
            f"{event['name']} | "
            f"{event['value']}")


def display_correlations(incident):
    correlations = correlate_events(incident["events"])
    print("\nEVENT CORRELATIONS")
    print("-" * 60)
    if not correlations:
        print("No deployment-related events found.")
        return
    for correlation in correlations:
        deployment = correlation["deployment"]
        print(f"Deployment: {deployment['value']} "
            f"at {deployment['timestamp']}")
        if not correlation["related_events"]:
            print("No events found within the correlation window.")
        for event in correlation["related_events"]:
            print(f"  +{event['minutes_after_deployment']} min | "
                f"{event['type']} | "
                f"{event['name']} | "
                f"{event['value']}")
        print("-" * 60)


def display_investigation(incident):
    result = investigate_incident(incident)
    print("\nINVESTIGATION RESULTS")
    print("=" * 60)
    print(f"Incident ID: {result['incident_id']}")
    for index, hypothesis in enumerate(result["hypotheses"], start=1):
        print(f"\n{index}. {hypothesis['title']}")
        print(f"   Rule-based score: {hypothesis['score']}")
        if hypothesis["supporting_evidence"]:
            print("   Supporting evidence:")
            for evidence in hypothesis["supporting_evidence"]:
                print(f"   - {evidence}")
        else:
            print("   No supporting evidence identified.")
    print("\nIMPORTANT:")
    print("These are preliminary hypotheses, not confirmed causes.")
        
        
def main():
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "incidents.json"
    incident = load_incident(data_path)
    display_incident(incident)
    display_anomalies(incident)
    display_timeline(incident)
    display_correlations(incident)
    display_investigation(incident)


if __name__ == "__main__":
    main()
