TRACE — AI Incident Investigator

TRACE is a prototype AI-assisted incident investigation system designed to help developers investigate application failures by analyzing incident events, detecting metric anomalies, correlating events with deployments, ranking preliminary root-cause hypotheses, and retrieving relevant external information.

Features

* Incident ingestion: Loads incident data from a JSON file.
* Metric anomaly detection: Flags significant metric increases using a configurable threshold.
* Incident timeline: Arranges events chronologically.
* Deployment correlation: Identifies events occurring within a specified time window after deployments.
* Hypothesis ranking: Ranks predefined root-cause hypotheses using rule-based evidence scoring.
* External research: Uses TinyFish Search and Fetch to retrieve relevant webpages for further investigation.

Project Structure

TRACE/
├── data/
│   └── incidents.json
├── src/
│   ├── main.py
│   ├── correlator.py
│   ├── metrics_analyzer.py
│   ├── investigator.py
│   └── web_research.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

Requirements

* Python 3.10 or later
* A TinyFish API key for external research
* Internet connectivity for TinyFish API requests

Installation

Clone the repository and navigate to the project directory.

Install the required dependencies:

python -m pip install -r requirements.txt

Configuration

Create a .env file in the project root.

Add your TinyFish API key:

TINYFISH_API_KEY=your_actual_api_key

Replace the placeholder with your own API key.

Never commit your .env file or expose your API key publicly.

External research requires a valid API key and working TinyFish API endpoints.

Running TRACE

From the project root, run:

python src/main.py

The program loads the incident from data/incidents.json and runs the local investigation workflow followed by external research.

Investigation Workflow

1. Incident Ingestion

TRACE loads incident metadata, technology information, symptoms, and recorded events from a JSON file.

2. Metric Anomaly Detection

The metric analyzer compares recorded measurements against the first observation for each metric.

An observation at least twice the baseline is flagged as an anomaly by default.

3. Timeline and Event Correlation

The correlator builds a chronological event timeline and identifies events occurring within a configurable time window after a deployment.

4. Hypothesis Ranking

The investigator uses predefined rules to assign scores to root-cause hypotheses based on detected anomalies and correlated events.

The hypotheses are ranked by their scores.

5. External Research

TRACE constructs a search query from incident details, searches for relevant webpages using TinyFish, and retrieves content from selected results.

Retrieved research is displayed separately from the local investigation results.

Current Limitations

* Incident data is supplied through static JSON rather than live operational telemetry.
* Anomaly detection uses a simple threshold rather than a statistically established baseline.
* Hypotheses are predefined and scored using hardcoded rules.
* Hypothesis scores are not probabilities.
* Temporal correlation does not establish causation.
* External research findings do not currently influence hypothesis ranking.
* Root-cause hypotheses are preliminary and require further verification.
* The current implementation does not include LLM-based reasoning or a frontend dashboard.

Prototype Scope

TRACE demonstrates the basic components of an incident investigation workflow using sample data and external web research.

It is a prototype, not a production incident-management system. Its findings should be treated as investigative leads rather than confirmed root causes.
