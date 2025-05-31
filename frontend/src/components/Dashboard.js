import React from "react";
import { useEffect } from "react";
import { useHistory, Link } from "react-router-dom"

function Dashboard() {
  const history = useHistory();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const tokenFromURL = params.get("token");

    if (tokenFromURL) {
      localStorage.setItem("userToken", tokenFromURL);
    }

    const storedToken = localStorage.getItem("userToken");

    if (!storedToken) {
      history.push("/login");
      return;
    }

    // Optional: Validate token with your backend
    fetch(`http://localhost:8000/auth/verify-token?token=${storedToken}`)
      .then(res => res.json())
      .then(data => {
        if (!data.valid) {
          localStorage.removeItem("userToken");
          history.push("/login");
        }
      })
      .catch(() => {
        localStorage.removeItem("userToken");
        history.push("/login");
      });
  }, [history]);

  return (
    <div>
      <h2>Welcome to your Dashboard</h2>
      <p>This is a protected area after login.</p>
    </div>
  );
}

export default Dashboard;