import React, { useState } from "react"; // ✅ Import React!
import { useHistory } from "react-router-dom";
import { Link } from "react-router-dom";

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const history = useHistory();
    const apiUrl = process.env.REACT_APP_API_URL;

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch(`${apiUrl}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("userToken", data.token); // optional: store token
            history.push("/dashboard");
        } else {
            alert(data.detail || "Login failed");
        }
    };

    const handleGoogleLogin = () => {
        const googleLoginWindow = window.open(
            `${apiUrl}/auth/google`,
            "_blank",
            "width=500,height=600"
        );

        function handleMessage(event) {
            const token = event.data?.token;
            if (token) {
                localStorage.setItem("userToken", token);
                if (googleLoginWindow) {
                    googleLoginWindow.close(); // ✅ Avoid floating line
                }
                history.push("/dashboard");
                window.removeEventListener("message", handleMessage);
            }
        }

        window.addEventListener("message", handleMessage);
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-4">
                    <h2 className="text-center mb-4">Login</h2>
                    <form onSubmit={handleSubmit} className="border p-4 shadow rounded bg-white">
                        <div className="mb-3">
                            <label className="form-label">Username</label>
                            <input
                                type="text"
                                className="form-control"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                required
                            />
                        </div>

                        <div className="mb-3">
                            <label className="form-label">Password</label>
                            <input
                                type="password"
                                className="form-control"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </div>

                        <div className="d-grid">
                            <button type="submit" className="btn btn-primary">
                                Login
                            </button>
                        </div>
                    </form>
                    <p className="text-center mt-3">
                        Don’t have an account? <Link to="/register">Register here</Link>
                    </p>
                    <hr />
                    <button
                        onClick={handleGoogleLogin}
                        style={{
                            marginTop: "1em",
                            backgroundColor: "#4285F4",
                            color: "white",
                            padding: "10px",
                            border: "none",
                            borderRadius: "4px",
                        }}
                    >
                        Login with Google
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Login;
