# TRACE — AI Incident Investigator

> **AZINHACK ’26 | Project submission: 18 October 2026**  
> TRACE aims to help engineers move from incident alerts to evidence-backed root-cause hypotheses by connecting operational signals, event timelines, and targeted external technical research.

**Status:** Working prototype. The current Python investigation pipeline is being developed and tested against the `INC-002` database-connection-timeout scenario. TinyFish, LLM reasoning, the web dashboard, API service, Docker packaging, and live telemetry ingestion must be marked as implemented only after they have been integrated and tested.

---

## 1. The problem

When a production service fails, useful clues may be scattered across:

- Application logs and error messages
- Metrics such as latency, request rate, and resource or connection utilization
- Deployment and configuration changes
- Technical documentation, release notes, and issue reports

Finding a plausible cause means connecting these signals and checking whether the evidence supports the explanation. A correlation in time is a clue, not proof of causation.

## 2. What TRACE is designed to do

TRACE is an AI-assisted incident-investigation workflow intended to:

1. **Analyze** incident metrics and identify unusual behavior.
2. **Correlate** logs, measurements, and events into an incident timeline.
3. **Research** relevant external technical sources using TinyFish.
4. **Evaluate** competing root-cause hypotheses against the available evidence.
5. **Report** observations, supporting and contradicting evidence, uncertainty, and useful next diagnostic checks.

The goal is to make the investigation trail inspectable—not to claim that an AI-generated explanation is automatically correct.

## 3. Current implementation status

Update this table immediately before submission so it matches the repository and demo.

| Component | Status |
|---|---|
| Python investigation pipeline for the current incident fixture | In progress / prototype |
| Metric analysis and anomaly checks | Implemented in the current prototype; validate with tests |
| Event timeline and correlation | Implemented in the current prototype; validate with tests |
| Candidate hypotheses and report output | Prototype; verify the exact output before claiming completion |
| TinyFish Search + Fetch integration | Planned until tested end-to-end |
| LLM-based hypothesis generation/ranking | Planned until tested end-to-end |
| FastAPI service | Planned until tested end-to-end |
| React + Vite dashboard | Planned until tested end-to-end |
| Docker packaging | Planned until tested end-to-end |
| Live telemetry from an instrumented application | Planned / in progress; describe only the working ingestion path |

**Important:** Do not present a planned feature as working. Replace the status labels above with precise, verifiable claims before submission.

## 4. Architecture

### Current prototype flow

```text
Incident input
     |
     v
Metric analysis
     |
     v
Timeline and event correlation
     |
     v
Candidate hypotheses
     |
     v
Investigation report
```

### Intended end-to-end flow

```text
Instrumented application / telemetry
     |
     v
Normalized logs, metrics and change events
     |
     v
Metric analysis + timeline/correlation
     |
     +-----------------------------+
     |                             |
     v                             v
Internal evidence             TinyFish research
                                   |
                              Search + Fetch
                                   |
                                   v
                         Source-grounded findings
     |                             |
     +-------------+---------------+
                   |
                   v
       Hypothesis generation and checks
                   |
                   v
 Evidence-linked report + next diagnostic actions
```

The intended design separates **observed facts**, **external context**, and **inferred explanations**. External search results should retain source URLs and relevant excerpts. A similar issue found online is not, by itself, proof of the incident's cause.

## 5. Repository structure

The current project structure is expected to resemble:

```text
TRACE-AI-INCIDENT-INVESTIGATOR/
├── data/
│   └── incidents.json
├── src/
│   ├── main.py
│   ├── metrics_analyzer.py
│   ├── correlator.py
│   ├──  investigator.py
|   └── web_research.py
|
├── tests/
├── .env                 # local secrets; do not commit
├── .gitignore
├── requirements.txt
└── README.md
```

This is a guide, not a guarantee that every path exists in the current checkout. Adjust it to match the actual repository. Add files such as `web_research.py`, `llm_analyzer.py`, `report_generator.py`, or `api.py` only when they exist.

## 6. Getting started

### Requirements

- Python 3.10+ (use the version tested by the project)
- Git
- API credentials only for integrations that are actually enabled

### Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd TRACE-AI-INCIDENT-INVESTIGATOR
```

### Create and activate a virtual environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not complete yet, install only the dependencies actually used by the current code and update the file before asking judges to run the project.

### Run the current prototype

From the repository root:

```bash
python3 src/main.py
```

On Windows, `python src/main.py` may be the appropriate command.

If the entry point or command differs in the current repository, replace this command with the verified one. A README should contain a command that has been tested from a clean environment.

## 7. Example investigation: database connection timeouts

The current project scenario, `INC-002`, concerns database connection acquisition timeouts.

Potential evidence may include:

- Application errors reporting connection acquisition timeouts
- Metric changes around the incident window
- A deployment or configuration event close to the start of failures
- Relevant external documentation or release notes, once research integration is implemented

A deployment-related regression is only one possible hypothesis. Other possibilities include connection-pool exhaustion, query latency, traffic changes, database saturation, or configuration issues.

TRACE should identify what was actually observed, explain why a hypothesis is plausible, and state which measurements or checks are needed to verify it. If there are too few samples, the result should say **insufficient data** rather than silently treating the metric as normal.

## 8. TinyFish integration plan

The intended external-research workflow is:

1. Build a targeted query from the error message, technology, version, and incident context.
2. Search for potentially relevant technical sources.
3. Select and fetch candidate pages.
4. Extract only relevant, source-supported information.
5. Preserve each source URL and relevant excerpt.
6. Link findings to the hypothesis they support, contradict, or merely contextualize.
7. Handle empty results, failed fetches, rate limits, and irrelevant pages.

Only describe this as implemented after the complete workflow has been run successfully. Do not commit API keys or place secrets in screenshots, logs, or the repository.

## 9. Testing and evaluation

Useful tests for the prototype include:

- The incident file loads correctly and malformed input is handled.
- Timestamps are parsed and events are ordered consistently.
- Metric analysis handles missing values and insufficient samples.
- Anomalies are reported with the baseline, observed value, and timestamp when available.
- Correlation logic does not treat timing alone as causal proof.
- Hypotheses distinguish supporting evidence from missing or contradictory evidence.
- External findings retain their source URLs and are not fabricated.
- Repeated runs on the same input produce reproducible output.

Before the submission, run the project from a clean environment and capture the actual output for the demo.

## 10. Limitations

- Static incident fixtures are useful for repeatable development tests but do not demonstrate performance on live production telemetry.
- Statistical anomalies and temporal correlation do not prove root cause.
- External pages can be stale, irrelevant, or describe a superficially similar issue.
- LLM-generated explanations can be wrong or overconfident.
- Diagnostic quality depends on the completeness and quality of available evidence.
- Any confidence or ranking score must have a clear basis; it should not be presented as a calibrated probability unless it has been validated.

## 11. Roadmap

1. Stabilize and test the Python investigation core.
2. Connect a running instrumented application and ingest real logs/metrics through a clear normalized-event interface.
3. Integrate TinyFish Search + Fetch and preserve source-grounded evidence.
4. Add LLM-assisted hypothesis generation and evidence-aware evaluation.
5. Expose the workflow through FastAPI.
6. Build a React + Vite incident dashboard.
7. Package the tested system with Docker and document a reproducible run.

The order may change as the hackathon deadline approaches. Prioritize a small, end-to-end workflow that can be run and demonstrated reliably.

## 12. Team

- **Team name:** [Team Name]
- **Members:** [Names and contributions]
- **Institution:** [College / University]
- **Demo:** [Demo URL, if available]
- **Repository:** [GitHub URL]

---

## Submission checklist

- [ ] Replace all placeholders.
- [ ] Confirm the setup and run commands work from a clean checkout.
- [ ] Ensure `requirements.txt` lists the dependencies required to run the project.
- [ ] Ensure `.env` and API keys are excluded from Git.
- [ ] Update implementation status to match tested code.
- [ ] Add real output and, once integrated, actual TinyFish search/fetch examples.
- [ ] Explain how to reproduce the `INC-002` investigation.
- [ ] Remove any claims that cannot be demonstrated from the repository.
