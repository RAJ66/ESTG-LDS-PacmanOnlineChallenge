import React, { useState } from "react";
import "./styles.css";
import logo from "../../assets/logo.png";
import api from "../../services/api";
import Stats from "../../components/Stats";
import ImageLevel from "./../../components/ImageLevel/index";
import Challenges from "./../../components/Challenges/index";

import facebook from "../../assets/001-facebook.png";
import twitter from "../../assets/013-twitter-1.png";
import instagram from "../../assets/011-instagram.png";
import ranking from "../../assets/ranking.png";

export default function Dashboard({ history }) {
  const user_id = localStorage.getItem("userId");
  const token = localStorage.getItem("userToken");

  const [level, setLevel] = useState();
  const [score, setScore] = useState();
  const [rank, setRank] = useState();

  const [nameCha1, setNameCha1] = useState("");
  const [nameCha2, setNameCha2] = useState("");
  const [nameCha3, setNameCha3] = useState("");

  const [pointCha1, setPointCha1] = useState();
  const [pointCha2, setPointCha2] = useState();
  const [pointCha3, setPointCha3] = useState();

  const [valid1, setValid1] = useState("");
  const [valid2, setValid2] = useState("");
  const [valid3, setValid3] = useState("");

  async function load() {
    const response = await api.get("/api/ranks", {
      headers: { id: user_id, Authorization: `Bearer ${token}` }
    });

    setLevel(response.data.level);
    setScore(response.data.score);
    setRank(response.data.rank);

    setNameCha1(response.data.dailyChallenge[0].description);
    setNameCha2(response.data.dailyChallenge[1].description);
    setNameCha3(response.data.dailyChallenge[2].description);

    setPointCha1(response.data.dailyChallenge[0].points);
    setPointCha2(response.data.dailyChallenge[1].points);
    setPointCha3(response.data.dailyChallenge[2].points);

    setValid1(response.data.todayDoneChallenge[0]);
    setValid2(response.data.todayDoneChallenge[1]);
    setValid3(response.data.todayDoneChallenge[2]);

    console.log(response);
  }

  load();

  function handleClickExit(event) {
    event.preventDefault();
    history.push("/");
  }
  function handleClickLeaderboards(event) {
    event.preventDefault();
    history.push("/leaderboards");
  }

  return (
    <div className="container-dashboard">
      <div className="header-container">
        <div className="header">
          <h1>PacmanOnlineChallenge</h1>
          <img src={logo} alt="Logo" />
        </div>
      </div>
      <div className="stats-container">
        <div className="cashier">
          <ImageLevel nivel={level} />
          <h1>Stats</h1>
          <Stats nivel={level} score={score} rank={rank} />
        </div>
      </div>
      <div className="challenges-container">
        <div className="cashier">
          <h1>Challenges</h1>
          <Challenges
            nameCha1={nameCha1}
            nameCha2={nameCha2}
            nameCha3={nameCha3}
            pointCha1={pointCha1}
            pointCha2={pointCha2}
            pointCha3={pointCha3}
            valid1={valid1}
            valid2={valid2}
            valid3={valid3}
          />
        </div>
      </div>
      <div className="footer-container">
        <div className="social">
          <a href="https://pt.wikipedia.org/wiki/Pac-Man" className="icon">
            <img src={facebook} alt="Facebook" />
          </a>
          <a href="https://pt.wikipedia.org/wiki/Pac-Man" className="icon">
            <img src={instagram} alt="Instagram" />
          </a>
          <a href="https://pt.wikipedia.org/wiki/Pac-Man" className="icon">
            <img src={twitter} alt="Twitter" />
          </a>
        </div>
        <div className="actions">
          <button
            onClick={handleClickLeaderboards}
            className="link-button icon "
          >
            <img src={ranking} alt="leaderboards" />
          </button>
          <button onClick={handleClickExit} className="link-button icon">
            <img
              src="https://img.icons8.com/ios-filled/50/000000/exit.png"
              alt="Exit"
            />
          </button>
        </div>
      </div>
    </div>
  );
}
