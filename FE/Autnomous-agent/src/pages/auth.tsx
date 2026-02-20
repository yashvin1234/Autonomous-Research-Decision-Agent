import { useNavigate, useLocation } from "react-router-dom";
import { useState } from "react";
import "../styles/auth.css";

const API = "http://127.0.0.1:5050";

function Auth() {
  const navigate = useNavigate();
  const location = useLocation();

  const isSignup = location.pathname === "/signup";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setError("");

    if (!email || !password) {
      setError("Please fill all fields");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`${API}/auth/${isSignup ? "signup" : "login"}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ 
            email:email, 
            password:password 
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Something went wrong");
        setLoading(false);
        return;
      }

      localStorage.setItem("token", data.access_token);
      navigate("/chat");

    } catch (e) {
      setError("Server not reachable");
    }

    setLoading(false);
  };

  return (
    <div className="auth">
      <div className="auth-card">

        <h2>{isSignup ? "Create Account" : "Login"}</h2>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && <div className="auth-error">{error}</div>}

        <button onClick={handleSubmit} disabled={loading}>
          {loading ? "Please wait..." : isSignup ? "Signup" : "Login"}
        </button>

        {!isSignup ? (
          <p onClick={() => navigate("/signup")} className="auth-switch">
            Don't have an account? Sign up
          </p>
        ) : (
          <p onClick={() => navigate("/auth")} className="auth-switch">
            Already have an account? Login
          </p>
        )}

      </div>
    </div>
  );
}

export default Auth;

