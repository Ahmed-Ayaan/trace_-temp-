<div align="center">

# TRACE
### AI Incident Investigator

**From scattered incident signals to evidence-backed root-cause hypotheses.**

TRACE is an AI-assisted incident investigation system designed to help
developers understand application failures by analyzing incident data,
detecting metric anomalies, correlating events, researching external
technical information, and presenting investigation results through an
interactive dashboard.

Built with Python, FastAPI, React, Vite, and TinyFish.

</div>

---

## Table of Contents

- [Overview](#overview)
- [The Problem](#the-problem)
- [Our Approach](#our-approach)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Investigation Workflow](#investigation-workflow)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Running TRACE](#running-trace)
- [API](#api)
- [External Research with TinyFish](#external-research-with-tinyfish)
- [Current Implementation](#current-implementation)
- [Limitations and Future Improvements](#limitations-and-future-improvements)
- [Security](#security)
- [Project Vision](#project-vision)

---

## Overview

Modern applications generate large amounts of operational data.
When an application fails, engineers must investigate logs, metrics,
deployment events, configuration changes, and technical documentation
to determine what happened.

TRACE aims to make this process faster and more structured.

It brings incident information together, identifies unusual metric
behavior, correlates relevant events, retrieves external technical
context, and organizes the findings into an investigation report.

Instead of presenting an unexplained root-cause conclusion, TRACE
emphasizes the relationship between observed evidence, candidate
hypotheses, and the additional checks needed to verify them.

The current implementation includes a Python investigation engine,
a FastAPI backend, a React-based dashboard, and TinyFish-powered
external research.

Incident data currently comes from local JSON fixtures.

### Core Objective

Transform fragmented incident information into a structured,
evidence-oriented investigation that helps developers identify
plausible causes and determine what to investigate next.

---

## The Problem

When a production service fails, the available evidence is often
distributed across multiple systems.

### 1. Logs

Logs describe errors and application behavior, but individual error
messages do not necessarily reveal the underlying cause.

### 2. Metrics

Metrics reveal changes in latency, error rates, resource utilization,
and other operational measurements.

However, an unusual metric does not automatically explain why the
system failed.

### 3. Deployments and Configuration Changes

A deployment or configuration change occurring near an incident
may be relevant, but temporal proximity alone does not establish
causation.

### 4. External Technical Information

Documentation, release notes, known issues, and technical discussions
can provide useful context.

However, a similar issue found online is not proof that it caused
the current incident.

### 5. Investigation Complexity

Engineers must connect these signals, compare competing explanations,
identify missing evidence, and decide which diagnostic action to
perform next.

TRACE is designed to organize these activities into a more
transparent investigation workflow.

---

## Our Approach

TRACE separates the investigation into several stages.

| Stage | Responsibility |
|---|---|
| Analyze | Examine available incident metrics and identify unusual behavior. |
| Correlate | Organize incident events chronologically and identify potentially relevant relationships. |
| Investigate | Combine available evidence and evaluate candidate explanations. |
| Research | Retrieve relevant external technical information using TinyFish. |
| Present | Display investigation findings through the dashboard and backend response. |

The goal is not simply to produce a root-cause label.

The goal is to make the investigation understandable and actionable.

### Design Principles

- Evidence before conclusions.
- Distinguish observed facts from inferred explanations.
- Treat correlation as a lead, not proof of causation.
- Preserve external source context wherever available.
- Make uncertainty and missing evidence explicit.
- Recommend diagnostic checks that can help verify or reject a hypothesis.

---

## Key Features

### 1. Incident Data Processing

TRACE processes structured incident information containing relevant
events, timestamps, metric measurements, and deployment information.

The current implementation uses local JSON incident fixtures.

This provides a controlled environment for developing and testing
the investigation engine.

### 2. Metric Anomaly Analysis

The metric analyzer examines available measurements to identify
unusual behavior.

Depending on the available data and configured rules, this can help
identify changes in metrics such as:

- Database latency.
- Application response time.
- Error rates.
- Resource utilization.
- Other numerical operational measurements.

An anomaly indicates behavior worth investigating. It does not
necessarily identify the root cause.

### 3. Event Correlation

TRACE organizes relevant events around the incident timeline.

This allows the investigation to examine relationships between:

- Application errors.
- Metric changes.
- Deployment events.
- Other recorded incident signals.

Temporal relationships help identify candidate explanations that
require further verification.

### 4. Investigation Engine

The investigation engine combines the available analysis and
correlation results into a structured investigation.

It helps organize the evidence and candidate explanations so that
the incident can be examined systematically.

Current hypothesis generation and scoring remain preliminary and
should not be interpreted as a fully autonomous root-cause reasoning
system.

### 5. External Technical Research

TRACE integrates TinyFish-based research to retrieve relevant
external technical information.

Research can help identify documentation, release notes, known
issues, and other technical material related to an incident.

External information provides additional context. It must still be
evaluated against the incident's actual evidence.

### 6. FastAPI Backend

The backend exposes investigation functionality through an HTTP API.

The React frontend communicates with the Python backend to request
investigations and display the resulting information.

### 7. Interactive Web Dashboard

TRACE includes a React and Vite frontend.

The dashboard provides a graphical interface for interacting with
the investigation system and examining the available investigation
results.

### 8. Modular Architecture

The project separates the API, investigation logic, metric analysis,
event correlation, and external research into different modules.

This separation makes individual components easier to understand,
debug, test, and extend.

---

## System Architecture

The current system is organized into three primary layers.

### Architecture Diagram

```mermaid
flowchart TB

    subgraph FRONTEND["Frontend Layer"]
        UI["React Dashboard"]
        VITE["Vite Development Server"]
        CLIENT["API Client"]
        UI --> CLIENT
        VITE --- UI
    end

    subgraph BACKEND["Backend Layer"]
        API["FastAPI Application"]
        ENGINE["Investigation Engine"]
        METRICS["Metric Analyzer"]
        CORR["Event Correlator"]
        DATA["Incident JSON Data"]

        API --> ENGINE
        ENGINE --> METRICS
        ENGINE --> CORR
        ENGINE --> DATA
    end

    subgraph RESEARCH["External Research Layer"]
        WEB["TinyFish Research"]
        SOURCES["External Technical Sources"]

        WEB --> SOURCES
    end

    CLIENT <-->|HTTP / JSON| API
    ENGINE --> WEB

    API --> RESPONSE["Structured Investigation Response"]
    RESPONSE --> CLIENT
    CLIENT --> UI
