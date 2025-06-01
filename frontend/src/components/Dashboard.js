import React from "react";
import { useEffect } from "react";
import { useHistory, Link } from "react-router-dom"

function Dashboard() {
  const history = useHistory();
  const apiBaseUrl = process.env.REACT_APP_API_URL;

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

  return (
    <div>
      <h2>Welcome to your Dashboard</h2>
      <p>This is a protected area after login.</p>
    </div>
  );
}

export default Dashboard;