import React, {
  useState,
  useCallback,
  // useEffect
} from "react";
import { GoogleMap, LoadScript } from "@react-google-maps/api";
import Marker from "./Marker";
import Polyline from "./Polyline";
// import styled from "styled-components";

// const Marker = styled('div')`
// background-color: #D83B01;
// border-radius: 50%;
// color: #fff;
// height: 2.5em;
// position: relative;
// width: 2.5em;
// border: 1px solid transparent;`;

// Define the bounding box coordinates for London
const londonBounds = {
  north: 51.6926,
  south: 51.3876,
  west: -0.5087,
  east: 0.2334,
};
const newMarkers: { lat: number; lng: number }[] = [];
for (let i = 0; i < 10; i++) {
  const lat =
    londonBounds.south +
    Math.random() * (londonBounds.north - londonBounds.south);
  const lng =
    londonBounds.west + Math.random() * (londonBounds.east - londonBounds.west);
  newMarkers.push({ lat, lng });
}
newMarkers.push({ lat: 51.518412, lng: -0.125755 });
console.log("newMarkers", newMarkers);

const MapWithPolyline = () => {
  // const [markers, setMarkers] = useState<{ lat: number; lng: number }[]>([]);
  const [polyline, setPolyline] = useState<{ lat: number; lng: number }[]>([]);
  const [pointsOrder, setPointsOrder] = useState<number[]>([]);
  const [isDrawing, setIsDrawing] = useState(false);

  // const generateRandomPoints = useCallback(() => {
  //   const newMarkers: { lat: number; lng: number }[] = [];
  //   for (let i = 0; i < 10; i++) {
  //     const lat =
  //       londonBounds.south +
  //       Math.random() * (londonBounds.north - londonBounds.south);
  //     const lng =
  //       londonBounds.west +
  //       Math.random() * (londonBounds.east - londonBounds.west);
  //     newMarkers.push({ lat, lng });
  //   }
  //   newMarkers.push({ lat: 51.518412, lng: -0.125755 });
  //   console.log("newMarkers", newMarkers);
  //   setMarkers(newMarkers);
  // }, []);

  // const handleMapClick = useCallback((event) => {
  //   setPolyline((prevPath) => [...prevPath, event.latLng.toJSON()]);
  // }, []);

  // useEffect(() => {
  //   generateRandomPoints();
  // }, [generateRandomPoints]);
  // Starting the user path drawing
  const onMarkerClick = useCallback((index) => {
    setIsDrawing(true);
  }, []);

  const onMMouseUp = useCallback((index) => {
    setIsDrawing(false);
  }, []);

  const onMarkerHover = useCallback(
    (index) => {
      if (isDrawing && !pointsOrder.includes(index)) {
        setPointsOrder((prevOrder) => [...prevOrder, index]);
      }
      setPolyline((prevPath) => [...prevPath, newMarkers[index]]);
    },
    [isDrawing, pointsOrder]
  );

  // const handleMapClick = useCallback((event) => {
  //   setPolyline((prevPath) => [...prevPath, event.latLng.toJSON()]);
  // }, []);

  return (
    <LoadScript googleMapsApiKey="AIzaSyDhoZuGMp4OC6-42RUG2VX0O3Havr3o0Rs">
      <GoogleMap
        mapContainerStyle={{ height: "100vh", width: "100%" }}
        center={{ lat: 51.5074, lng: -0.1278 }} // Center on London
        zoom={10}
        // onClick={handleMapClick}
        onMouseUp={onMMouseUp}
        // options={{
        //   markerClusterer: null, // Disable marker clustering
        // }}
      >
        {newMarkers.map((marker, index) => (
          <Marker
            onClick={onMarkerClick}
            onMouseOver={onMarkerHover}
            key={index}
            position={marker}
            text={`${index}`}
          />
        ))}
        {/* {markers.map((marker, index) => (
          <Marker {...marker} key={index} />
        ))} */}
        <Polyline
          path={polyline}
          options={{ strokeColor: "red", strokeWeight: 2 }}
        />
      </GoogleMap>
    </LoadScript>
  );
};

export default MapWithPolyline;
