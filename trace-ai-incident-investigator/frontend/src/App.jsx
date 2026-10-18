import { useState } from "react";
import { investigateIncident } from "./api";
import "./app.css";

function SectionHeading({ eyebrow, title, right }) {
  return (
    <div className="section-heading">
      <div>
        <div className="eyebrow">{eyebrow}</div>
        <h2>{title}</h2>
      </div>
      {right && <span className="muted small">{right}</span>}
    </div>
  );
}

function formatTime(timestamp) {
  if (!timestamp) return "Unknown time";

  return timestamp.includes("T")
    ? timestamp.split("T")[1]
    : timestamp;
}

function formatDate(timestamp) {
  if (!timestamp || !timestamp.includes("T")) {
    return timestamp || "";
  }

  return timestamp.split("T")[0];
}

function getEventStyle(event) {
  if (event.type === "deployment") {
    return { color: "purple", label: "DEPLOY" };
  }

  if (event.type === "log") {
    return {
      color: "red",
      label: event.severity || "LOG",
    };
  }

  if (event.type === "metric") {
    return { color: "blue", label: "METRIC" };
  }

  return {
    color: "amber",
    label: event.type?.toUpperCase() || "EVENT",
  };
}

function getEventTitle(event) {
  if (event.type === "deployment") {
    return `Version ${event.value} deployed`;
  }

  return event.name || event.message || "Incident event";
}

function getEventDetail(event) {
  if (event.type === "metric") {
    return `Value: ${event.value}`;
  }

  if (event.type === "log") {
    return event.message || event.value || "";
  }

  return String(event.value ?? "");
}

function getHypothesisTitle(hypothesis) {
  return (
    hypothesis.title ||
    hypothesis.name ||
    hypothesis.hypothesis ||
    "Untitled hypothesis"
  );
}

function App() {
  const [incident, setIncident] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleInvestigate() {
    setLoading(true);
    setError("");

    try {
      const result = await investigateIncident("INC-001");
      setIncident(result);
    } catch (err) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  }

  // Data returned by FastAPI
  const technology = incident?.technology || {};
  const anomalies = incident?.anomalies || [];
  const events = incident?.timeline || [];
  const correlations = incident?.correlations || [];
  const hypotheses = incident?.hypotheses || [];

  const research = incident?.external_research;
  const sources = research?.sources || [];

  const paymentErrorAnomaly = anomalies.some(
    (anomaly) =>
      anomaly.metric === "payment_error_rate"
  );

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">T</div>

          <div>
            <strong>TRACE</strong>
            <span>Incident Intelligence</span>
          </div>
        </div>

        <div className="nav-label">WORKSPACE</div>

        <div className="nav-item active">
          <span>◈</span> Incident overview
        </div>

        <div className="nav-item">
          <span>⌁</span> Anomaly detection
        </div>

        <div className="nav-item">
          <span>◷</span> Incident timeline
        </div>

        <div className="nav-item">
          <span>◎</span> Hypotheses
        </div>

        <div className="nav-item">
          <span>↗</span> External research
        </div>

        <div className="sidebar-bottom">
          <div className="status-dot" />

          <div>
            <strong>Investigation engine</strong>
            <span>
              {incident
                ? "Backend connected"
                : "Awaiting investigation"}
            </span>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">
            Workspace <span>/</span> Incidents <span>/</span>{" "}
            {incident?.incident_id || "INC-001"}
          </div>

          <div className="sample-badge">
            <span />
            {incident
              ? "LIVE BACKEND RESULTS"
              : "READY TO INVESTIGATE"}
          </div>
        </header>

        <div className="page-content">
          <div className="page-title-row">
            <div>
              <div className="eyebrow">
                INCIDENT INVESTIGATION
              </div>

              <h1>
                {incident?.description ||
                  "Investigate payment-service failures"}
              </h1>

              <p className="muted">
                Review signals, correlate events and evaluate
                possible causes.
              </p>
            </div>

            <span className="incident-id">
              {incident?.incident_id || "INC-001"}
            </span>
          </div>

          <div style={{ marginBottom: "24px" }}>
            <button
              className="investigate-button"
              onClick={handleInvestigate}
              disabled={loading}
            >
              {loading
                ? "Investigating..."
                : "Investigate INC-001"}
            </button>
          </div>

          {error && (
            <div
              role="alert"
              className="note"
              style={{
                marginTop: 0,
                marginBottom: "22px",
              }}
            >
              <strong>Investigation failed.</strong> {error}

              <p style={{ marginBottom: 0, marginTop: "6px" }}>
                Confirm that FastAPI is running and that
                POST /investigate works at
                http://127.0.0.1:8000/docs.
              </p>
            </div>
          )}

          {!incident && !loading && !error && (
            <div
              className="note"
              style={{
                marginTop: 0,
                marginBottom: "22px",
              }}
            >
              Click Investigate INC-001 to load results from
              your Python backend and run external research.
            </div>
          )}

          {/* OVERVIEW */}
          <section className="overview-grid">
            <article className="panel overview-card">
              <span className="muted small">
                AFFECTED SERVICE
              </span>

              <h3>{incident?.service || "—"}</h3>

              <p>
                {technology.database ||
                  technology.name ||
                  "Database not provided"}
              </p>
            </article>

            <article className="panel overview-card">
              <span className="muted small">
                CURRENT VERSION
              </span>

              <h3>
                {technology.current_version || "—"}
              </h3>

              <p>Version recorded in incident data</p>
            </article>

            <article className="panel overview-card">
              <span className="muted small">
                INCIDENT STATUS
              </span>

              <h3>
                <span className="status-pill neutral">
                  {incident
                    ? "Under investigation"
                    : "Not started"}
                </span>
              </h3>

              <p>Root cause not confirmed</p>
            </article>

            <article className="panel overview-card">
              <span className="muted small">
                DETECTED ANOMALIES
              </span>

              <h3 className="metric-number">
                {String(anomalies.length).padStart(2, "0")}
              </h3>

              <p>Returned by the Python metric analyzer</p>
            </article>
          </section>

          {/* ANOMALIES */}
          <section className="panel anomaly-panel">
            <SectionHeading
              eyebrow="SIGNAL ANALYSIS"
              title="Anomaly detection"
              right={`${anomalies.length} detected`}
            />

            {!incident ? (
              <p className="muted">
                Run an investigation to retrieve anomaly results.
              </p>
            ) : anomalies.length === 0 ? (
              <p className="muted">
                No anomalies were returned by the metric analyzer.
              </p>
            ) : (
              anomalies.map((anomaly, index) => (
                <div
                  className="anomaly-content"
                  key={`${anomaly.metric}-${anomaly.timestamp}-${index}`}
                  style={{ marginBottom: "22px" }}
                >
                  <div className="anomaly-icon">↗</div>

                  <div className="anomaly-details">
                    <div className="anomaly-name">
                      {anomaly.metric}
                    </div>

                    <p className="muted">
                      Observed at {formatTime(anomaly.timestamp)}
                      {" · "}
                      {formatDate(anomaly.timestamp)}
                    </p>

                    <div className="metric-pair">
                      <div>
                        <span>BASELINE</span>

                        <strong>
                          {anomaly.baseline}
                          <small>
                            {anomaly.metric?.includes("_ms")
                              ? " ms"
                              : ""}
                          </small>
                        </strong>
                      </div>

                      <div>
                        <span>OBSERVED</span>

                        <strong>
                          {anomaly.observed}
                          <small>
                            {anomaly.metric?.includes("_ms")
                              ? " ms"
                              : ""}
                          </small>
                        </strong>
                      </div>
                    </div>
                  </div>

                  <div className="anomaly-result">
                    <span className="severity-pill">
                      {anomaly.severity || "UNSPECIFIED"}
                    </span>

                    <strong>
                      {anomaly.increase_percent > 0 ? "+" : ""}
                      {anomaly.increase_percent}%
                    </strong>

                    <span className="muted small">
                      Increase over baseline
                    </span>
                  </div>
                </div>
              ))
            )}

            {incident && !paymentErrorAnomaly && (
              <div className="note">
                Payment error rate:{" "}
                {events.find(
                  (event) =>
                    event.type === "metric" &&
                    event.name === "payment_error_rate"
                )?.value ?? "No measurement available"}
                . An increase cannot be calculated unless
                the metric analyzer has sufficient baseline
                measurements.
              </div>
            )}
          </section>

          {/* TIMELINE AND HYPOTHESES */}
          <div className="content-grid">
            <section className="panel timeline-panel">
              <SectionHeading
                eyebrow="EVENT CORRELATION"
                title="Incident timeline"
                right={`${events.length} events`}
              />

              {!incident ? (
                <p className="muted">
                  Run an investigation to retrieve the incident
                  timeline.
                </p>
              ) : events.length === 0 ? (
                <p className="muted">
                  No timeline events were returned.
                </p>
              ) : (
                <>
                  <div className="timeline">
                    {events.map((event, index) => {
                      const style = getEventStyle(event);

                      return (
                        <div
                          className="timeline-event"
                          key={`${event.timestamp}-${event.name}-${index}`}
                        >
                          <div className="timeline-time">
                            {formatTime(event.timestamp)}
                          </div>

                          <div
                            className={`timeline-marker ${style.color}`}
                          />

                          <div className="timeline-copy">
                            <span
                              className={`event-type ${style.color}`}
                            >
                              {style.label}
                            </span>

                            <h4>{getEventTitle(event)}</h4>

                            <p>{getEventDetail(event)}</p>
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  <p className="timeline-footnote">
                    Source timestamps are displayed as supplied.
                  </p>
                </>
              )}

              {incident && correlations.length > 0 && (
                <div className="evidence-block">
                  <span className="evidence-label">
                    EVENT CORRELATIONS
                  </span>

                  {correlations.map((correlation, index) => (
                    <p key={index}>
                      {typeof correlation === "string"
                        ? correlation
                        : correlation.description ||
                          JSON.stringify(correlation)}
                    </p>
                  ))}
                </div>
              )}
            </section>

            <section className="panel hypotheses-panel">
              <SectionHeading
                eyebrow="RULE-BASED INVESTIGATION"
                title="Ranked hypotheses"
                right="Preliminary"
              />

              <p className="muted small intro">
                Scores represent investigation rules, not
                probabilities.
              </p>

              {!incident ? (
                <p className="muted">
                  Run an investigation to retrieve ranked
                  hypotheses.
                </p>
              ) : hypotheses.length === 0 ? (
                <p className="muted">
                  No hypotheses were returned by the investigator.
                </p>
              ) : (
                hypotheses.map((hypothesis, index) => {
                  const evidence =
                    hypothesis.supporting_evidence || [];

                  const missing =
                    hypothesis.missing_evidence || [];

                  return (
                    <article
                      className="hypothesis"
                      key={`${getHypothesisTitle(hypothesis)}-${index}`}
                    >
                      <div className="hypothesis-top">
                        <div className="rank">
                          {String(index + 1).padStart(2, "0")}
                        </div>

                        <div className="hypothesis-title">
                          <h4>
                            {getHypothesisTitle(hypothesis)}
                          </h4>

                          <span
                            className={`status-pill ${
                              hypothesis.status === "plausible"
                                ? "plausible"
                                : "neutral"
                            }`}
                          >
                            {hypothesis.status || "untested"}
                          </span>
                        </div>

                        <div className="score">
                          <strong>
                            {hypothesis.score ?? 0}
                          </strong>

                          <span>score</span>
                        </div>
                      </div>

                      <div className="evidence-block">
                        <span className="evidence-label">
                          SUPPORTING EVIDENCE
                        </span>

                        {evidence.length ? (
                          evidence.map((item, evidenceIndex) => (
                            <p key={evidenceIndex}>
                              +{" "}
                              {typeof item === "string"
                                ? item
                                : item.description ||
                                  JSON.stringify(item)}
                            </p>
                          ))
                        ) : (
                          <p className="muted">
                            No supporting evidence identified.
                          </p>
                        )}
                      </div>

                      <div className="evidence-block missing">
                        <span className="evidence-label">
                          MISSING EVIDENCE
                        </span>

                        {missing.length ? (
                          missing.map((item, missingIndex) => (
                            <p key={missingIndex}>
                              –{" "}
                              {typeof item === "string"
                                ? item
                                : item.description ||
                                  JSON.stringify(item)}
                            </p>
                          ))
                        ) : (
                          <p className="muted">
                            No missing evidence listed.
                          </p>
                        )}
                      </div>
                    </article>
                  );
                })
              )}

              <p className="timeline-footnote">
                These hypotheses are preliminary, not confirmed
                root causes.
              </p>
            </section>
          </div>

          {/* EXTERNAL RESEARCH */}
          <section className="panel research-panel">
            <SectionHeading
              eyebrow="EXTERNAL KNOWLEDGE"
              title="External research"
              right={
                !research
                  ? "Not run"
                  : research.status === "completed"
                    ? `${sources.length} sources`
                    : research.status.replace("_", " ")
              }
            />

            {!research ? (
              <div className="research-empty">
                <div className="research-icon">↗</div>

                <div>
                  <h4>No research results available</h4>

                  <p className="muted">
                    Click Investigate to retrieve external
                    technical information through TinyFish.
                  </p>
                </div>

                <span className="status-pill neutral">
                  NOT RUN
                </span>
              </div>
            ) : (
              <>
                <div className="research-status">
                  <strong>
                    Research status: {research.status}
                  </strong>

                  {research.message && (
                    <p className="muted">
                      {research.message}
                    </p>
                  )}

                  {research.query && (
                    <p className="muted">
                      <strong>Search query:</strong>{" "}
                      {research.query}
                    </p>
                  )}
                </div>

                {sources.length === 0 ? (
                  <p className="muted">
                    No external sources are available for this
                    investigation.
                  </p>
                ) : (
                  <div className="research-sources">
                    {sources.map((source, index) => (
                      <article
                        className="research-source"
                        key={
                          source.url ||
                          `${source.title || "source"}-${index}`
                        }
                      >
                        <div className="research-source-header">
                          <span className="source-number">
                            SOURCE {index + 1}
                          </span>

                          <span className="status-pill neutral">
                            Retrieved
                          </span>
                        </div>

                        <h4>
                          {source.title || "Untitled source"}
                        </h4>

                        {source.snippet && (
                          <p className="muted">
                            {source.snippet}
                          </p>
                        )}

                        {source.url && (
                          <a
                            href={source.url}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            Open original source ↗
                          </a>
                        )}

                        {source.content && (
                          <details>
                            <summary>
                              View retrieved content
                            </summary>

                            <p className="source-content">
                              {source.content.slice(0, 3000)}
                            </p>
                          </details>
                        )}
                      </article>
                    ))}
                  </div>
                )}
              </>
            )}
          </section>

          <footer className="footer">
            <span>TRACE · AI Incident Investigator</span>

            <span>
              {incident
                ? "Results returned by the Python backend"
                : "Waiting for backend results"}
            </span>
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;