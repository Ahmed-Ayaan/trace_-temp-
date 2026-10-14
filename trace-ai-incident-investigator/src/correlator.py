from datetime import datetime


def parse_timestamp(timestamp):
    """Convert a timestamp string into a datetime object."""
    return datetime.fromisoformat(timestamp)


def build_timeline(events):
    """
    Sort all incident events chronologically
    and return the ordered timeline.
    """
    return sorted(
        events,
        key=lambda event: parse_timestamp(event["timestamp"])
    )


def correlate_events(events, window_minutes=10):
    """
    Find events that occur near a deployment.

    This identifies temporal relationships, not proven
    causal relationships.
    """
    timeline = build_timeline(events)

    deployments = [
        event for event in timeline
        if event["type"] == "deployment"
    ]

    correlations = []

    for deployment in deployments:
        deployment_time = parse_timestamp(
            deployment["timestamp"]
        )

        related_events = []

        for event in timeline:
            if event is deployment:
                continue

            event_time = parse_timestamp(
                event["timestamp"]
            )

            time_difference = (
                event_time - deployment_time
            ).total_seconds() / 60

            if 0 < time_difference <= window_minutes:
                related_events.append({
                    "timestamp": event["timestamp"],
                    "type": event["type"],
                    "name": event["name"],
                    "value": event["value"],
                    "minutes_after_deployment": round(
                        time_difference, 2
                    )
                })

        if related_events:
            correlations.append({
                "deployment": deployment,
                "related_events": related_events
            })

    return correlations