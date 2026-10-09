import json
from pathlib import Path


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
        print(f"Increase: "f"{anomaly['increase_percent']}%")
        print(f"Severity: {anomaly['severity']}")
        print("-" * 50)


def main():
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "incidents.json"
    incident = load_incident(data_path)
    display_incident(incident)
    display_anomalies(incident)


if __name__ == "__main__":
    main()
