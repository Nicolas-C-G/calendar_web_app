import React from "react";
import { useEffect, useState } from "react";
import { useHistory, Link } from "react-router-dom"

function Dashboard() {
  const history = useHistory();
  const apiBaseUrl = process.env.REACT_APP_API_URL;

  const [events, setEvents] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const tokenFromURL = params.get("token");

    if (tokenFromURL) {
      localStorage.setItem("userToken", tokenFromURL);
    }

    const storedToken = localStorage.getItem("userToken");

    if (!storedToken) {
      history.push("");
      return;
    }

    fetch(`${apiBaseUrl}/auth/verify-token`, {
      method: "POST",
      headers: {
        "content-Type": "application/json",
      },
      body: JSON.stringify({ token: storedToken })
    })
      .then(res => res.json())
      .then(data => {
        if (!data.valid){
          localStorage.removeItem("userToken");
          history.push("");
        }
      })
      .catch(() => {
        localStorage.removeItem("userToken");
        history.push("");
      });
  }, 
  [history]);

  const fetchCalendarEvents = async () => {
    const token = localStorage.getItem("userToken");

    try {
      const response = await fetch(`${apiBaseUrl}/calendar/events`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ token })
      });

      const data = await response.json();

      if (response.ok) {
        setEvents(data);
        setError("");
      } else {
        setError(data.detail || "Failed to fetch events");
        setEvents([]);
      }
    } catch (err) {
      setError("Error connecting to the server");
      setEvents([]);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Welcome to your Dashboard</h2>
      <p>This is a protected area after login.</p>

      <button className="btn btn-success mt-3 mb-3" onClick={fetchCalendarEvents}>
        Load Google Calendar Events
      </button>

      {error && <div className="alert alert-danger">{error}</div>}

      {events.length > 0 && (
        <ul className="list-group">
          {events.map((event, idx) => (
            <li key={idx} className="list-group-item">
              {event.summary || "Untitled Event"} —{" "}
              {event.start?.dateTime || event.start?.date || "No start time"}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Dashboard;