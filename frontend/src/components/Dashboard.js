import React from "react";
import { useEffect, useState } from "react";
import { useHistory, Link } from "react-router-dom";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import "@fullcalendar/daygrid/index.js";
import { Modal, Button } from "react-bootstrap";
import interactionPlugin from "@fullcalendar/interaction";


function Dashboard() {
  const history = useHistory();
  const apiBaseUrl = process.env.REACT_APP_API_URL;

  const [events, setEvents] = useState([]);
  const [error, setError] = useState("");
  const [filteredEvents, setFilteredEvents] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedDate, setSelectedDate] = useState("");

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
        const formattedEvents = data.map(event => ({
            title: event.summary || "Untiteled",
            start: event.start?.dateTime || event.start?.date,
            fullEvent: event 
          }));


          setEvents(formattedEvents);
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

  const handleDateClick = (info) => {
    const selectedDate = info.dateStr
    const selected = events.filter((event) => {
      const eventDate = event.start?.substring(0,10);
      return eventDate === selectedDate;
    });
    
    setSelectedDate(selectedDate);
    setFilteredEvents(selected);
    console.log(filteredEvents);
    setShowModal(true);
  };

  return (
    <div className="container mt-5">
      <h2>Welcome to your Dashboard</h2>
      <p>This is a protected area after login.</p>

      <button className="btn btn-success mt-3 mb-3" onClick={fetchCalendarEvents}>
        Load Google Calendar Events
      </button>

      {error && <div className="alert alert-danger">{error}</div>}

      <FullCalendar
        plugins={[dayGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        events={events}
        dateClick={(info) => handleDateClick(info)}
      />

      {/* Step 5: Modal goes here */}
      {showModal && (
        <div className="modal show d-block" tabIndex="-1" role="dialog">
          <div className="modal-dialog" role="document">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Events on {selectedDate}</h5>
                <button
                  type="button"
                  className="btn-close"
                  aria-label="Close"
                  onClick={() => setShowModal(false)}
                ></button>
              </div>
              <div className="modal-body">
                {filteredEvents.length === 0 ? (
                  <p>No events for this day.</p>
                ) : (
                  <ul>
                    {filteredEvents.map((event, idx) => {
                      const meetLink =
                        event.fullEvent?.hangoutLink ||
                        event.fullEvent?.conferenceData?.entryPoints?.find(
                          (ep) => ep.entryPointType === "video"
                        )?.uri;
                      
                      const formattedTime = event.start.includes("T") ? event.start.split("T")[1].split(":").slice(0, 2).join(":") + "pm" : "All day";  
                      const utc = event.start.slice(-6);                    
                      return (
                        <li key={idx}>
                          <strong>{formattedTime} UTC: {utc} - {event.fullEvent?.summary || event.title}</strong>
                          {meetLink && (
                            <>
                              <br />
                              <a href={meetLink} target="_blank" rel="noopener noreferrer">
                                Join Google Meet
                              </a>
                            </>
                          )}
                        </li>
                      );
                    })}
                  </ul>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;