import React, { useState } from "react";
import { useHistory  } from "react-router-dom";


function Login() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const history = useHistory ();
    const apiUrl = process.env.REACT_APP_API_URL

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch(`${apiUrl}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        
        if (response.ok) {
            history.push("/dashboard");
        } else {
            alert(data.detail || "Login failed");
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <label>Username</label>
                <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                />
                <br />

                <label>Password</label>
                <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                />
                <br />

                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default Login;