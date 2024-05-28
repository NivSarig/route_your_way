import { styled } from "@mui/material";
import img from "./background.png";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import InputLabel from "@mui/material/InputLabel";
import { TextField, Button } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { BACKEND } from "./backend";

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

function CreateGamePage() {
  const [city, setCity] = useState<string>();
  const [name, setName] = useState<string>();

  const handleChange = (event: SelectChangeEvent) => {
    setCity(event.target.value);
  };
  const handleNameChange = event => {
    setName(event.target.value);
  };

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
    ).then(async response => {
      const newGameState = await response.json();
      console.log("newly created game", newGameState);
      navigate("/map", { state: { name: name, code: newGameState.game_id } });
    });
  };
  return (
    <Container>
      {/* <InputLabel id="demo-simple-select-label">Barel</InputLabel> */}
      <ContentContainer>
        <StyledSelect
          labelId='demo-simple-select-label'
          id='demo-simple-select'
          value={city}
          label='Barel'
          variant='standard'
          // placeholder="Select a city"
          onChange={handleChange}
        >
          {cities.map(city => (
            <MenuItem value={city}>{city}</MenuItem>
          ))}
        </StyledSelect>
        {city && <TextField label='Name' variant='filled' value={name} onChange={handleNameChange} />}
        {city && name && (
          <Button variant='contained' onClick={onCreate}>
            Create
          </Button>
        )}
      </ContentContainer>
    </Container>
  );
}

export default CreateGamePage;
