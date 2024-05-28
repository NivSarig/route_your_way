import React from "react";
// import logo from "./logo.svg";
import "./App.css";
import MapWithPolyline from "./MapWithPolyline";
import {
  BrowserRouter as Router,
  Navigate,
  Route,
  Routes,
  useRoutes,
} from "react-router-dom";
import LandingPage from "./LandingPage";
import LeadingBoard from "./LeadingBoard";
import CreateGamePage from "./CreateGamePage";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/map" element={<MapWithPolyline />}></Route>
          <Route path="/" element={<LandingPage />}></Route>
          <Route path="/LeadingBoard" element={<LeadingBoard />}></Route>
          <Route path="/create" element={<CreateGamePage />}></Route>
          <Route path="/join" element={<CreateGamePage />}></Route>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
