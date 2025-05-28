import React, { useState } from "react";
import { useHistory } from "react-router-dom";

function Register() {
    const [form, setForm] = useState({
        name: "",
        last_name: "",
        username: "",
        password: "",
        re_password: "",
        email: "",
        company: ""
    });

    const history = useHistory();

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const res = await fetch(`${process.env.REACT_APP_API_URL}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(form)
        });

        if (res.ok) {
            alert ("User registered!");
            history.push("/");
        } else {
            const data = await res.json();
            alert(data.detail || "Registration faild");
        }

    };

    const passwordsMatch = form.password && form.re_password && form.password === form.re_password;

    return (
        <div>
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                {["name", "last_name", "email", "company", "username"].map((field) => (
                    <div key={field}>
                        <label>{field.replace("_", " ")}</label>
                        <input 
                            type="text"
                            name={field}
                            value={form[field]}
                            onChange={handleChange}
                            required
                        />
                    </div>
                ))}
                <div>
                    <label>Password</label>
                    <input
                        type="password"
                        name="password"
                        value={form.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Re-type Password</label>
                    <input
                        type="password"
                        name="re_password"
                        value={form.re_password}
                        onChange={handleChange}
                        required
                    />
                </div>
                {!passwordsMatch && form.re_password && (
                    <p style={{ color: "red" }}>Passwords do not match</p>
                )}
                <button type="submit" disabled={!passwordsMatch}>
                    Create Account
                </button>
            </form>
        </div>
    );
}

export default Register;