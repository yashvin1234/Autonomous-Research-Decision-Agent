import { useNavigate } from "react-router-dom";
import "../styles/home.css";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home">
      <div className="home-left">
        <h1>Autonomous Decision Agent</h1>
        <p>
          An AI system that researches, evaluates and recommends decisions
          automatically.
        </p>

        <button className="start-btn" onClick={() => navigate("/auth")}>
          Get Started
        </button>
      </div>

      <div className="home-right">
        <div className="blob"></div>
      </div>
    </div>
  );
}

export default Home;

