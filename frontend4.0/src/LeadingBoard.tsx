import { styled } from "@mui/material";
import img from "./leading_page_back.png";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import React from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";
import { useLocation } from "react-router-dom";
import { BACKEND } from "./backend";

interface Data {
  rank: number;
  name: string;
  time: string; // duration
  distance: string;
}

type Contestant = {
  name: string;
  distance: number;
  duration: string;
};

const createData = (rank: number, name: string, time: string, distance: string): Data => {
  return { rank, name, time, distance };
};

const rows = [
  createData(1, "Lital", "0:18:15", "3.904"),
  createData(2, "Gony", "0:20:00", "5.15"),
  createData(3, "Niv", "0:21:00", "5.5"),
  createData(4, "Nir", "0:21:00", "5.5"),
  createData(5, "Barel", "0:21:00", "5.5"),
  createData(6, "Noa", "0:22:00", "5.7"),
];

const Container = styled("div")({
  backgroundImage: `url(${img})`,
  backgroundSize: "100% 100%",
  height: "100vh",
  width: "100vw",
});

function LeadingBoard() {
  let location = useLocation();
  const [gameState, setGameState] = useState({} as any);
  const [leaderBoard, setLeaderBoard] = useState<Data[]>([]);
  useEffect(() => {
    const poll = () => {
      fetch(`${BACKEND}/game/${location.state.code}`, {
        method: "GET",
      }).then(async response => {
        const newGameState = await response.json();
        console.log("game state", newGameState);
        setGameState(newGameState);
        const sorted = Object.values(newGameState.contestants).sort((a: Contestant, b: Contestant) => {
          return a.distance - b.distance;
        });
        setLeaderBoard(
          Object.values(newGameState.contestants).map((c: Contestant, i) => {
            return createData(i, c.name, c.duration, c.distance.toString());
          })
        );
      });
    };
    setInterval(poll, 5000);
  }, [location.state.code]);

  return (
    <Container>
      <TableContainer component={Paper}>
        <Table aria-label='simple table'>
          <TableHead>
            <TableRow>
              <TableCell>#</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Time</TableCell>
              <TableCell>Distance</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {leaderBoard.map(row => (
              <TableRow key={row.rank}>
                <TableCell component='th' scope='row'>
                  {row.rank}
                </TableCell>
                <TableCell>{row.name}</TableCell>
                <TableCell>{row.time}</TableCell>
                <TableCell>{row.distance}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
}

export default LeadingBoard;
