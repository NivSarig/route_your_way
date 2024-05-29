import { styled } from "@mui/material";
import img from "./background.png";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import InputLabel from "@mui/material/InputLabel";
import { TextField, Button } from "@mui/material";
import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

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

function JoinGamePage() {
  const [ URLSearchParams , _]  = useSearchParams();
  const [name, setName] = useState<string>();
  const [code, setCode] = useState<string>(URLSearchParams.get("code") || "");


  const handleCodeChange = (event) => {
    setCode(event.target.value);
  };
  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const navigate = useNavigate();

  const onCreate = () => {
    navigate("/map", { state: { name, code: code.toUpperCase() } });
  };
  return (
    <Container>
      {/* <InputLabel id="demo-simple-select-label">Barel</InputLabel> */}
      <ContentContainer>
        <TextField
          sx={{ backgroundColor: "white" }}
          label="Name"
          variant="filled"
          value={name}
          onChange={handleNameChange}
        />
        <TextField
          sx={{ backgroundColor: "white" }}
          label="Code"
          variant="filled"
          value={code}
          onChange={handleCodeChange}
        />

        <Button
          disabled={!name || !code}
          variant="contained"
          onClick={onCreate}
        >
          Join Game!
        </Button>
      </ContentContainer>
    </Container>
  );
}

export default JoinGamePage;
