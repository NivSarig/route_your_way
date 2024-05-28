import { styled } from "@mui/material";
import img from "./leading_page_back.png";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";

interface Data {
  rank: number;
  name: string;
  time: string; // duration
  distance: string;
}

const createData = (
  rank: number,
  name: string,
  time: string,
  distance: string
): Data => {
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

const BACKEND = process.env.BACKEND || "http://localhost:8000";

function LeadingBoard() {
  const [name, setName] = useState<string>("");
  const [code, setCode] = useState<string>("");

  const navigate = useNavigate();

  const onCreate = () => {
    fetch(
      `${BACKEND}/game?` +
        new URLSearchParams({
          location: "Tel Aviv",
        }),
      {
        method: "PUT",
      }
    ).then(async (response) => {
      const newGameState = await response.json();
      console.log("newly created game", newGameState);
      navigate("/map", { state: { name: name, code: newGameState.game_id } });
    });
  };

  return (
    <Container>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>#</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Time</TableCell>
              <TableCell>Distance</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row) => (
              <TableRow key={row.rank}>
                <TableCell component="th" scope="row">
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
