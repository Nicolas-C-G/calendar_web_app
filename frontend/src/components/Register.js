import React, { useState } from "react";
import { useHistory, Link } from "react-router-dom";

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
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                <h2 className="text-center mb-4">Create an Account</h2>
                <form onSubmit={handleSubmit} className="border p-4 shadow rounded bg-white">
                    {["name", "last_name", "email", "company", "username"].map((field) => (
                    <div className="mb-3" key={field}>
                        <label className="form-label text-capitalize">{field.replace("_", " ")}</label>
                        <input
                        type="text"
                        name={field}
                        className="form-control"
                        value={form[field]}
                        onChange={handleChange}
                        required
                        />
                    </div>
                    ))}

                    <div className="mb-3">
                    <label className="form-label">Password</label>
                    <input
                        type="password"
                        name="password"
                        className="form-control"
                        value={form.password}
                        onChange={handleChange}
                        required
                    />
                    </div>

                    <div className="mb-3">
                    <label className="form-label">Re-type Password</label>
                    <input
                        type="password"
                        name="re_password"
                        className={`form-control ${form.re_password && !passwordsMatch ? "is-invalid" : ""}`}
                        value={form.re_password}
                        onChange={handleChange}
                        required
                    />
                    {!passwordsMatch && form.re_password && (
                        <div className="invalid-feedback">Passwords do not match</div>
                    )}
                    </div>

                    <div className="d-grid">
                    <button type="submit" className="btn btn-success" disabled={!passwordsMatch}>
                        Create Account
                    </button>
                    </div>
                </form>

                <p className="text-center mt-3">
                    Already have an account? <Link to="/">Login here</Link>
                </p>
                </div>
            </div>
        </div>
    );
}

export default Register;