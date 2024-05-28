import styled from "styled-components";
import img from "./background.png";

const Container = styled("div")`
  background-image: url(${img});
  background-size: 100% 100%;
  height: 100vh;
  width: 100vw;
`;

function LandingPage() {
  return <Container></Container>;
}

export default LandingPage;
