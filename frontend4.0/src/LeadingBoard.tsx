import { styled } from "@mui/material";
import img from "./leading_page_back.png";
import { ReactComponent as AvatarIcon } from "./algo_avatar.svg";
import { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import { useLocation } from "react-router-dom";
import { BACKEND } from "./backend";

interface Data {
  rank: number;
  name: string;
  time: string; // duration
  distance: string;
  link: string;
}

type Contestant = {
  name: string;
  distance: number;
  duration: string;
  coordinates: [number[]];
};

const coordinatesToLink = (coordinates: [number[]]) => {
  return (
    "https://www.google.com/maps/dir/" +
    coordinates.map((c) => c.join(",")).join("/") +
    "/data=!3m1!4b1!4m2!4m1!3e2"
  );
};

const createData = (
  rank: number,
  name: string,
  time: string,
  distance: string,
  coordinates: [number[]]
): Data => {
  const link = coordinatesToLink(coordinates);

  return { rank, name, time, distance, link };
};

const Container = styled("div")({
  backgroundImage: `url(${img})`,
  backgroundSize: "100% 100%",
  height: "100vh",
  width: "100vw",
  display: "flex",
  justifyContent: "center",
  alignItems: "flex-start",
  paddingTop: "1rem",
});

const HeaderTableCell = styled(TableCell)({
  fontWeight: "bold",
});

const AlgoAvatarTableCell = styled(TableCell)({
  fontWeight: "bold",
  color: "white",
});

function LeadingBoard() {
  let location = useLocation();
  const [gameState, setGameState] = useState({} as any);
  const [leaderBoard, setLeaderBoard] = useState<Data[]>([]);
  useEffect(() => {
    const poll = () => {
      fetch(`${BACKEND}/game/${location.state.code}`, {
        method: "GET",
      }).then(async (response) => {
        const newGameState = await response.json();
        console.log("game state", newGameState);
        setGameState(newGameState);
        const sorted = Object.values(newGameState.contestants).sort(
          (a: Contestant, b: Contestant) => {
            return a.distance - b.distance;
          }
        );
        setLeaderBoard(
          sorted
            .filter((c: Contestant) => c.distance !== undefined)
            .map((c: Contestant, i) => {
              return createData(
                i + 1,
                c.name,
                c.duration,
                c.distance?.toString(),
                c.coordinates
              );
            })
        );
      })
      .catch(error => {
        console.log("failed to get response", error);
        alert("Lost connection with the server");
      });
    };
    poll();
    setInterval(poll, 3000);
  }, [location.state.code]);

  const algoTime = gameState?.solution?.duration;
  const algoDistance = gameState?.solution?.distance;
  const algoLink = coordinatesToLink(gameState?.solution?.coordinates || []);

  return (
    <Container>
      <TableContainer sx={{ width: "80%", maxHeight: "60vh" }}>
        <Table stickyHeader aria-label="simple table">
          <TableHead>
            <TableRow component={Paper}>
              <HeaderTableCell>#</HeaderTableCell>
              <HeaderTableCell>Name</HeaderTableCell>
              <HeaderTableCell>Time</HeaderTableCell>
              <HeaderTableCell>Distance</HeaderTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <AlgoAvatarTableCell>
                <AvatarIcon
                  style={{
                    height: "50px",
                    float: "left",
                  }}
                />
              </AlgoAvatarTableCell>
              <AlgoAvatarTableCell>Algo Solution</AlgoAvatarTableCell>
              <AlgoAvatarTableCell>{algoTime}</AlgoAvatarTableCell>
              <AlgoAvatarTableCell>
                {" "}
                <a href={algoLink} style={{ color: "inherit" }}>
                  {algoDistance}
                </a>
              </AlgoAvatarTableCell>
            </TableRow>
            {leaderBoard.map((row, index) => (
              <TableRow
                component={Paper}
                key={row.name}
                sx={{
                  backgroundColor: index % 2 === 0 ? "grey.100" : "white",
                }}
              >
                <TableCell component="th" scope="row">
                  {row.rank}
                </TableCell>
                <TableCell>{row.name}</TableCell>
                <TableCell>{row.time}</TableCell>
                <TableCell>
                  <a href={row.link}>{row.distance}</a>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
}

export default LeadingBoard;
