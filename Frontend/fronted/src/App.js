import React from "react";
import "./App.css";
import api from "./services/api";

import logo from "./assets/logo.png";

function App() {
  function handleSubmit(event) {
    event.preventDefault();
    console.log("Teste");
  }

  return (
    <div className="container">
      <form className="login-container" onSubmit={handleSubmit}>
        <img src={logo} alt="It a match" />
        <input placeholder="Email" />
        <input placeholder="Password" type="password" />

        <button type="submit" className="glow-on-hover">
          Login
        </button>
        <button type="" className="glow-on-hover">
          Register
        </button>
      </form>
    </div>
  );
}

export default App;
