import { styled } from "@mui/material";
import img from "./background.png";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import InputLabel from "@mui/material/InputLabel";
import { TextField, Button } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Container = styled("div")({
  backgroundImage: `url(${img})`,
  backgroundSize: "100% 100%",
  height: "100vh",
  width: "100vw",
  display: "flex",
  justifyContent: "center",
  // alignItems: "center",
  // flexDirection: "column",
});
const ContentContainer = styled("div")({
  display: "flex",
  flexDirection: "column",
  marginTop: "400px",
});
const StyledSelect = styled(Select)({
  color: "white",
  background: "linear-gradient(to right bottom, #4100fd, #2a0680)",
  // backgroundColor: "#2a0680",
  height: "50px",
  width: "200px",
  borderRadius: "10px",
  fontSize: "20px",
  // margin: "10px",
});
const cities = ["London", "Tel Aviv"];
const BACKEND = process.env.BACKEND || "http://localhost:8000";

function JoinGamePage() {
  const [city, setCity] = useState<string>();
  const [name, setName] = useState<string>();
  const [code, setCode] = useState<string>();

  const handleCodeChange = (event) => {
    setCode(event.target.value);
  };
  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const navigate = useNavigate();

  const onCreate = () => {
    fetch(
      `${BACKEND}/game?` +
        new URLSearchParams({
          location: city,
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
      {/* <InputLabel id="demo-simple-select-label">Barel</InputLabel> */}
      <ContentContainer>
        <TextField
          label="Name"
          variant="filled"
          value={name}
          onChange={handleNameChange}
        />
        <TextField
          label="Code"
          variant="filled"
          value={name}
          onChange={handleCodeChange}
        />

        {name && code && (
          <Button disabled={!name} variant="contained" onClick={onCreate}>
            Create
          </Button>
        )}
      </ContentContainer>
    </Container>
  );
}

export default JoinGamePage;
