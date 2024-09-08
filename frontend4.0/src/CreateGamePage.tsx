import { styled } from "@mui/material";
import disabledButton from "./createDisabled.png";
import createButton from "./createButton.png";
import img from "./background.png";
import selectArrow from "./selectArrow.png";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
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
});
const ContentContainer = styled("div")({
  display: "flex",
  flexDirection: "column",
  marginTop: "400px",
  alignItems: "center",
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
const StyledButton = styled(Button)(({ disabled }) => ({
  background: `url(${disabled ? disabledButton : createButton})`,
  backgroundSize: "100%",
  border: "none",
  height: disabled ? "100px" : "140px",
  width: disabled ? "100px" : "140px",
  marginTop: disabled ? "70px" : "50px",
}));
const cities = ["London", "Tel Aviv", "Paris", "New York", "Berlin"];

function CreateGamePage() {
  const [city, setCity] = useState<string>("");
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
          location: city,
          random: "false",
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
      <ContentContainer>
        <StyledSelect
          value={city}
          displayEmpty
          onChange={handleChange}
          sx={{ borderRadius: "40px" }}
          IconComponent={() => <img alt='arrow' src={selectArrow} style={{ width: "50px" }} />}
        >
          <MenuItem value={""}>
            <em>Select city</em>
          </MenuItem>
          {cities.map(city => (
            <MenuItem value={city}>{city}</MenuItem>
          ))}
        </StyledSelect>
        {city && (
          <TextField
            sx={{
              backgroundColor: "white",
              marginTop: "15px",
              borderRadius: "40px",
            }}
            autoComplete='off'
            label='Name'
            variant='filled'
            value={name}
            onChange={handleNameChange}
          />
        )}
        {city && <StyledButton disabled={!name} onClick={onCreate}></StyledButton>}
      </ContentContainer>
    </Container>
  );
}

export default CreateGamePage;
