const API_BASE_URL = "http://127.0.0.1:8000";

export async function investigateIncident(incidentId) {
  const response = await fetch(
    `${API_BASE_URL}/investigate`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        incident_id: incidentId,
      }),
    }
  );

  if (!response.ok) {
    const message = await response.text();

    throw new Error(
      `Investigation failed: ${message}`
    );
  }

  return response.json();
}