import React, {
  useState,
  useCallback,
  useEffect,
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
  const [isReady, setIsReady] = useState(false);
  const [totalDistance, setTotalDistance] = useState(0);

  // Starting the user path drawing
  const onMarkerClick = useCallback((index) => {
    setIsDrawing(true);
    setPointsOrder([index]);
    setPolyline([newMarkers[index]]);
  }, []);

  const onMMouseUp = useCallback((index) => {
    setIsDrawing(false);
  }, []);

  const [directionsService, setDirectionsService] = useState(null);

  // const directionsService = new google.maps.DirectionsService();

  useEffect(() => {
    const timer = setTimeout(() => {
      setDirectionsService(new google.maps.DirectionsService());
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

    const getRouteDistance = useCallback(async (originPoint, destinationPoint) => {
      debugger;
      try {
        // directionsService.route()
        // const response = await fetch(
        //   `https://maps.googleapis.com/maps/api/directions/json?origin=${originPoint.lat},${originPoint.lng}&destination=${destinationPoint.lat},${destinationPoint.lng}&mode=walking&key=YOUR_API_KEY`,
        //   { mode: 'cors' }
        // );
        // const data = await response.json();
        // if (data.status === "OK") {
        //   const route = data.routes[0];
        //   const distance = route.legs[0].distance.text;
        //   const polyline = route.overview_polyline.points;
        //   return { distance, polyline };
        // } else {
        //   return { distance: 0, polyline: [] };
        // }
        const route = await new Promise((resolve, reject) => {
          directionsService.route(
            {
              origin: `${originPoint.lat},${originPoint.lng}`,
              destination: `${destinationPoint.lat},${destinationPoint.lng}`,
              travelMode: google.maps.TravelMode.WALKING,
            },
            (response, status) => {
              debugger;
              if (status === google.maps.DirectionsStatus.OK) {
                resolve(response.routes[0]);
              } else {
                reject(new Error(`Directions request failed. Status: ${status}`));
              }
            }
          );
        });

        //@ts-ignore
        const distance = route.legs[0].distance.text;
        //@ts-ignore
        const polyline = route.legs[0].steps.map(step=> {return step.lat_lngs}).flat();

        return { distance, polyline };
      } catch (error) {
        console.error("Error:", error);
        return { distance: 0, polyline: [] };
      }
    }, [directionsService]);

  const onMarkerHover = useCallback(
    async (index) => {
      console.log("index", index);
      console.log("marker", newMarkers[index]);
      if (isDrawing && !pointsOrder.includes(index)) {
        setPointsOrder((prevOrder) => [...prevOrder, index]);
        const route = await getRouteDistance(newMarkers[pointsOrder[pointsOrder.length - 1]], newMarkers[index]);
        
        setPolyline((prevPath) => [...prevPath, ...route?.polyline]);
      }
    },
    [getRouteDistance, isDrawing, pointsOrder]
  );

  // const handleMapClick = useCallback((event) => {
  //   setPolyline((prevPath) => [...prevPath, event.latLng.toJSON()]);
  // }, []);

  return (
    <LoadScript
      googleMapsApiKey="AIzaSyDhoZuGMp4OC6-42RUG2VX0O3Havr3o0Rs"
      // onLoad={() => setIsReady(true)}
    >
      <GoogleMap
        onLoad={() => setIsReady(true)}
        mapContainerStyle={{ height: "100vh", width: "100%" }}
        center={{ lat: 51.5074, lng: -0.1278 }} // Center on London
        zoom={10}
        // onClick={handleMapClick}
        onMouseUp={onMMouseUp}
        // options={{gestureHandling:'none'}}

        // options={{
        //   markerClusterer: null, // Disable marker clustering
        // }}
      >
        {
          // isReady &&
          newMarkers.map((marker, index) => (
            <Marker
              onClick={() => onMarkerClick(index)}
              onMouseOver={() => onMarkerHover(index)}
              key={index}
              position={marker}
              text={`${index}`}
            />
          ))
        }
        {/* {markers.map((marker, index) => (
          <Marker {...marker} key={index} />
        ))} */}
        <Polyline
          path={polyline}
          options={{ strokeColor: "#FF2C95", strokeWeight: 2 }}
        />
      </GoogleMap>
    </LoadScript>
  );
};

export default MapWithPolyline;
