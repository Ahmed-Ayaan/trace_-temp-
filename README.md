<div align="center">

# TRACE
### AI Incident Investigator

**From scattered incident signals to evidence-backed root-cause hypotheses.**

TRACE is an AI-assisted incident investigation prototype designed to help developers investigate application failures by analyzing metrics, correlating events, generating potential root-cause hypotheses, and retrieving relevant external technical information.

</div>

---

## Quick Start

TRACE provides a structured setup process for running the application locally.

### Prerequisites

Install the following:

- Python 3
- Node.js and npm
- Git
- A TinyFish API key for external research

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
```

Replace the placeholders with your actual GitHub repository URL and directory name.

### 2. Install Backend Dependencies

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a local `.env` file using `.env.example` as a reference.

**macOS / Linux**

```bash
cp .env.example .env
```

Add your TinyFish API key and any other required environment variables to `.env`.

Never commit your actual API key or other secrets to GitHub.

### 4. Install Frontend Dependencies

From the repository root:

```bash
cd frontend
npm install
cd ..
```

### 5. Start TRACE

You can start the application using the appropriate startup script or launch the backend and frontend manually.

#### Option A: Use the Startup Script

The following scripts are intended for their respective operating systems:

- **macOS:** Run `Start TRACE.command`.
- **Windows:** Run `start-trace.bat`.
- **Linux:** Run `./start-trace.sh`.

These scripts must be included in the repository and tested on their respective operating systems before use.

The Python environment and backend dependencies must be installed first.

#### Option B: Start the Application Manually

**Start the backend**

From the repository root, activate the Python virtual environment and run:

```bash
source .venv/bin/activate
python -m uvicorn src.api:app --reload
```

On Windows PowerShell, activate the environment using:

```powershell
.venv\Scripts\Activate.ps1
python -m uvicorn src.api:app --reload
```

The backend should be available at:

`http://127.0.0.1:8000`

**Start the frontend**

Open a second terminal and navigate to the frontend directory:

```bash
cd frontend
npm run dev
```

Open the local URL printed by Vite, usually:

`http://localhost:5173`

Keep both servers running while using TRACE.

---

## Overview

Application failures often produce multiple signals across logs, metrics, deployments, and external technical systems. Investigating these signals manually can be time-consuming and difficult.

TRACE brings these signals together into a unified investigation workflow.

The prototype analyzes incident data, detects metric anomalies, constructs an incident timeline, correlates events, ranks preliminary hypotheses, and uses TinyFish to retrieve relevant external technical information.

A React dashboard presents the investigation results through a centralized interface powered by a FastAPI backend.

## Features

### 1. Metric Anomaly Detection

TRACE analyzes incident metrics to identify unusual changes in observed values.

The metric analyzer compares measurements against a baseline and identifies significant increases using configurable thresholds.

Detected anomalies can include:

- Metric name
- Observation timestamp
- Baseline value
- Observed value
- Percentage increase
- Severity classification

The exact fields depend on the metric analyzer's implementation and the available incident data.

### 2. Incident Timeline

TRACE organizes incident events chronologically to help developers understand how a failure developed.

The timeline can include:

- Metric measurements
- Application log events
- Deployment events

### 3. Event Correlation

TRACE identifies relationships between incident events using their timestamps.

The correlation component helps highlight events occurring near deployments and other potentially significant incident signals.

Temporal proximity provides a starting point for investigation; it does not independently establish causation.

### 4. Hypothesis Generation and Ranking

The investigation engine evaluates internal incident evidence and generates preliminary explanations for the failure.

Potential causes are ranked using rule-based evidence scoring.

The investigation results can include:

- Candidate root causes
- Supporting evidence
- Missing evidence
- Preliminary investigation scores
- Hypothesis status

These scores represent rule-based rankings, not calibrated probabilities.

### 5. External Technical Research

TRACE integrates TinyFish to search for relevant external technical information.

The research workflow can:

1. Construct a search query from incident information.
2. Search for relevant technical sources.
3. Retrieve candidate webpages.
4. Return research results and source information.

External findings can provide additional context for investigating an incident.

Retrieved sources are supporting material, not proof that a particular issue caused the failure.

### 6. Interactive Investigation Dashboard

The React dashboard provides a centralized interface for reviewing investigation results.

It presents the information returned by the current implementation, which may include:

- Incident overview
- Affected service and technology information
- Detected anomalies
- Incident timeline
- Ranked hypotheses
- Supporting and missing evidence
- External research results
- Links to original research sources

### 7. FastAPI Backend

FastAPI exposes the investigation workflow through an HTTP API.

The frontend sends an incident identifier to the backend and receives a structured JSON response containing the available investigation results.

The exact response fields depend on the API implementation.

---

## Architecture

TRACE consists of three primary layers.

### Investigation Engine

The Python investigation engine processes incident data.

Responsibilities include:

- Metric anomaly detection
- Timeline construction
- Event correlation
- Hypothesis generation
- Preliminary hypothesis ranking

### External Research Layer

TinyFish provides web-search and webpage-retrieval capabilities.

The retrieved information can provide additional technical context for the investigation.

Further evidence-grounded verification is needed before external findings can reliably establish a root cause.

### API and Dashboard Layer

FastAPI exposes the investigation workflow through HTTP endpoints.

React and Vite provide the interactive dashboard used to initiate investigations and display the results.

### Investigation Workflow

```text
                 Incident Data
                 incidents.json
                       |
                       v
             Python Investigation Engine
                       |
          +------------+------------+
          |            |            |
          v            v            v
       Metrics       Timeline     Event
       Analysis      Creation   Correlation
          |            |            |
          +------------+------------+
                       |
                       v
              Hypothesis Generation
                       |
                       v
             Preliminary Hypothesis
                    Ranking
                       |
                       +-------------------+
                       |                   |
                       v                   v
                Internal Evidence   TinyFish Research
                       |                   |
                       +---------+---------+
                                 |
                                 v
                       Investigation Results
                                 |
                                 v
                              FastAPI
                                 |
                                 v
                         React Dashboard
```

The diagram represents the intended investigation flow. The actual integration between internal evidence, external research, and hypothesis ranking depends on the implemented code.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Investigation logic and data processing |
| FastAPI | Backend API |
| Pydantic | API request validation |
| Requests | HTTP communication with external services |
| TinyFish | External web research |
| React | Dashboard interface |
| Vite | Frontend development server and build tooling |
| JavaScript | Frontend application logic |
| CSS | Dashboard styling |
| JSON | Incident data representation |
| Git | Version control |
| GitHub | Source-code hosting |

---

## Project Structure

The repository is organized into backend, data, and frontend components.

```text
trace-ai-incident-investigator/
│
├── data/
│   └── incidents.json
│
├── src/
│   ├── api.py
│   ├── main.py
│   ├── metrics_analyzer.py
│   ├── correlator.py
│   ├── investigator.py
│   └── web_research.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── app.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

*The structure above represents the intended organization. Verify filenames against the actual repository before publishing.*

### Backend Modules

| File | Responsibility |
|---|---|
| `src/api.py` | FastAPI application and investigation endpoint |
| `src/main.py` | Command-line investigation entry point |
| `src/metrics_analyzer.py` | Metric anomaly detection |
| `src/correlator.py` | Timeline construction and event correlation |
| `src/investigator.py` | Investigation orchestration and preliminary hypothesis ranking |
| `src/web_research.py` | TinyFish search and webpage retrieval |

### Frontend Modules

| File | Responsibility |
|---|---|
| `frontend/src/App.jsx` | Main dashboard interface |
| `frontend/src/api.js` | Communication with the FastAPI backend |
| `frontend/src/app.css` | Dashboard component styling |
| `frontend/src/index.css` | Global styling |
| `frontend/src/main.jsx` | React application entry point |

---

## Prerequisites

Before running TRACE manually, ensure that you have:

- Python installed
- Node.js and npm installed
- Git installed
- A TinyFish API key for external research

The manual setup instructions below assume macOS or Linux unless otherwise specified.

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
```

Replace the placeholders with your actual repository URL and directory name.

### 2. Create a Python Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file in the project root using `.env.example` as a reference.

For macOS or Linux:

```bash
cp .env.example .env
```

Add your TinyFish API key:

```dotenv
TINYFISH_API_KEY=your_tinyfish_api_key_here
```

Replace the placeholder with your actual key.

**Security:** Never commit your actual `.env` file or API key to GitHub.

The repository's `.env.example` should document the environment variables required by the implementation without containing real credentials.

### 5. Start the Backend

From the project root, activate the virtual environment if necessary:

```bash
source .venv/bin/activate
```

Start FastAPI:

```bash
python -m uvicorn src.api:app --reload
```

The backend will normally be available at:

`http://127.0.0.1:8000`

### 6. Access the API Documentation

Open:

`http://127.0.0.1:8000/docs`

The interactive documentation allows you to inspect the available endpoints and test the investigation API.

### 7. Start the Frontend

Open a second terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies if you have not already done so:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

Open the local URL printed by Vite, usually:

`http://localhost:5173`

Keep both the backend and frontend servers running while using the local application.

---

## API

### `POST /investigate`

Initiates an investigation for the specified incident.

#### Example Request

```json
{
  "incident_id": "INC-001"
}
```

#### Response

The endpoint returns a structured JSON object containing the available incident information and investigation results.

Depending on the implementation, response fields may include:

- `incident_id`
- `service`
- `description`
- `technology`
- `anomalies`
- `timeline`
- `correlations`
- `hypotheses`
- `external_research`

The exact request schema, endpoint path, and response fields must match the implementation in `src/api.py`.

### API Documentation

While the backend is running, open:

`http://127.0.0.1:8000/docs`

Use the interactive documentation to inspect the available endpoints and test requests.

---

## Current Limitations

TRACE is a functional prototype and is not intended to replace a production incident-management system.

Current limitations include:

- Incident input uses static JSON rather than a production telemetry pipeline.
- Metric anomaly detection uses a simplified baseline comparison.
- Event correlation relies on temporal relationships.
- Hypothesis generation and ranking are preliminary and rule-based.
- External research retrieval does not, by itself, verify whether a source supports a particular hypothesis.
- Root-cause hypotheses should not be treated as confirmed diagnoses.
- Production authentication, authorization, monitoring, and deployment infrastructure are outside the current prototype scope.

---

## Future Development

Potential improvements include:

- Real-time telemetry ingestion
- More robust statistical anomaly detection
- LLM-assisted hypothesis generation
- Evidence-grounded reasoning over retrieved technical sources
- Hypothesis verification and contradictory-evidence analysis
- More sophisticated confidence estimation
- Investigation history and persistence
- Automated testing against diverse incident scenarios
- Docker-based packaging and deployment

These are future development directions, not claims about currently implemented features.

---

## Security

- Keep API keys in environment variables.
- Never commit `.env` or other secret files.
- Avoid placing credentials in source code.
- Treat external webpages as untrusted input.
- Validate data received by API endpoints.
- Exclude `.venv/`, `frontend/node_modules/`, and generated cache files from version control.

Production deployments require additional authentication, authorization, monitoring, and infrastructure security controls.

---

## Project Status

**Functional prototype — under development.**

TRACE demonstrates an integrated workflow for internal incident analysis, preliminary root-cause hypothesis generation, external technical research, and dashboard-based investigation.

The next stage is to improve evidence verification, investigation quality, and robustness.

---

<div align="center">

**TRACE — From incident signals to structured investigation.**

</div>
