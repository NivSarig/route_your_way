import React, {
  useState,
  useCallback,
  useEffect,
  // useEffect
} from "react";
import { GoogleMap, LoadScript } from "@react-google-maps/api";
import Marker from "./Marker";
import Polyline from "./Polyline";
// import  styled from "styled-components";
import { useLocation } from "react-router-dom";
import { set } from "date-fns";

const BACKEND = process.env.BACKEND || "http://localhost:8000";
// import styled from "styled-components";

// const Marker = styled('div')`
// background-color: #D83B01;
// border-radius: 50%;
// color: #fff;
// height: 2.5em;
// position: relative;
// width: 2.5em;
// border: 1px solid transparent;`;
// const Scores = styled.div`
//   background-color: #D83B01;
//   border-radius: 50%;
//   color: red;
//   font-size: 1.5em;`;

// Define the bounding box coordinates for London
const londonBounds = {
  north: 51.6926,
  south: 51.3876,
  west: -0.5087,
  east: 0.2334,
};
const someRandomMarkers: { lat: number; lng: number }[] = [];
for (let i = 0; i < 10; i++) {
  const lat = londonBounds.south + Math.random() * (londonBounds.north - londonBounds.south);
  const lng = londonBounds.west + Math.random() * (londonBounds.east - londonBounds.west);
  someRandomMarkers.push({ lat, lng });
}
someRandomMarkers.push({ lat: 51.518412, lng: -0.125755 });

const MapWithPolyline = () => {
  // const [markers, setMarkers] = useState<{ lat: number; lng: number }[]>([]);
  const [polyline, setPolyline] = useState<{ lat: number; lng: number }[]>([]);
  const [pointsOrder, setPointsOrder] = useState<number[]>([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const [isReady, setIsReady] = useState(false);
  const [totalDistance, setTotalDistance] = useState(0);
  const [totalMinutes, setTotalMinutes] = useState(0);
  const [markers, setMarkers] = useState(someRandomMarkers);

  let location = useLocation();
  const [gameState, setGameState] = useState({} as any);
  useEffect(() => {
    console.log("joining", location.state);
    fetch(`${BACKEND}/game/${location.state.code}/contestant?name=${location.state.name}`, {
      method: "PUT",
    }).then(async response => {
      const newGameState = await response.json();
      console.log("game state", newGameState);
      setGameState(newGameState);
      setMarkers(
        newGameState.location.coordinates.map((coord: [number, number]) => ({ lat: coord[0], lng: coord[1] }))
      );
    });
  }, [location.state.code]);

  // Starting the user path drawing
  const onMarkerClick = useCallback(
    index => {
      setIsDrawing(true);
      setPointsOrder([index]);
      setPolyline([markers[index]]);
    },
    [markers]
  );

  const onMMouseUp = useCallback(index => {
    setIsDrawing(false);
  }, []);

  const [directionsService, setDirectionsService] = useState(null);

  const getPointColor = useCallback(
    (index: number) => {
      if (pointsOrder.includes(index)) {
        return "#FF2C95";
      } else {
        return "grey";
      }
    },
    [pointsOrder]
  );

  useEffect(() => {
    const timer = setTimeout(() => {
      setDirectionsService(new google.maps.DirectionsService());
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  const getRouteDistance = useCallback(
    async (originPoint, destinationPoint) => {
      try {
        const route = await new Promise((resolve, reject) => {
          directionsService.route(
            {
              origin: `${originPoint.lat},${originPoint.lng}`,
              destination: `${destinationPoint.lat},${destinationPoint.lng}`,
              travelMode: google.maps.TravelMode.WALKING,
            },
            (response, status) => {
              if (status === google.maps.DirectionsStatus.OK) {
                resolve(response.routes[0]);
              } else {
                reject(new Error(`Directions request failed. Status: ${status}`));
              }
            }
          );
        });

        //@ts-ignore
        const distance = route.legs[0].distance.value;
        //@ts-ignore
        const polyline = route.legs[0].steps
          .map(step => {
            return step.lat_lngs;
          })
          .flat();

        //@ts-ignore
        const minutes = route.legs[0].duration.value / 60;

        return { distance, polyline, minutes };
      } catch (error) {
        console.error("Error:", error);
        return { distance: 0, polyline: [], minutes: 0 };
      }
    },
    [directionsService]
  );

  const onMarkerHover = useCallback(
    async index => {
      console.log("index", index);
      console.log("marker", markers[index]);
      if (isDrawing && !pointsOrder.includes(index)) {
        setPointsOrder(prevOrder => [...prevOrder, index]);
        const route = await getRouteDistance(markers[pointsOrder[pointsOrder.length - 1]], markers[index]);
        setTotalDistance(prevDistance => prevDistance + route?.distance);
        setTotalMinutes(prevMinutes => prevMinutes + route?.minutes);
        setPolyline(prevPath => [...prevPath, ...route?.polyline]);
      }
    },
    [getRouteDistance, isDrawing, pointsOrder, markers]
  );

  const isGameFinished = useCallback(() => {
    return pointsOrder.length === markers.length;
  }, [pointsOrder.length, markers]);

  const formatTime = (minutes: number): string => {
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return `${hours} Hours, ${remainingMinutes} Minutes`;
  };

  return (
    <LoadScript googleMapsApiKey='AIzaSyDhoZuGMp4OC6-42RUG2VX0O3Havr3o0Rs'>
      <GoogleMap
        onLoad={() => setIsReady(true)}
        mapContainerStyle={{ height: "100vh", width: "100%" }}
        center={markers[0]} // Center on London
        zoom={10}
        // onClick={handleMapClick}
        onMouseUp={onMMouseUp}
        // options={{gestureHandling:'none'}}
      >
        {
          // isReady &&
          markers.map((marker, index) => (
            <Marker
              onClick={() => onMarkerClick(index)}
              onMouseOver={() => onMarkerHover(index)}
              key={index}
              position={marker}
              text={`${index}`}
              color={getPointColor(index)}
            />
          ))
        }
        <Polyline path={polyline} options={{ strokeColor: "#FF2C95", strokeWeight: 5 }} />
        <div
          style={{
            position: "absolute",
            top: "90%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            backgroundColor: "white",
            padding: "10px",
            borderRadius: "5px",
            fontSize: "2em",
            boxShadow: "0 2px 5px rgba(0, 0, 0, 0.3)",
          }}
        >
          {totalDistance} Metres
          <br />
          {formatTime(Math.round(totalMinutes))}
          <br />
          {isGameFinished() && <span style={{ color: "red" }}>Game Over!</span>}
          <br />
          {gameState.game_id}
        </div>
      </GoogleMap>
    </LoadScript>
  );
};

export default MapWithPolyline;
