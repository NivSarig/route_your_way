import React from "react";
import { Marker as GoogleMapsMarker } from "@react-google-maps/api";

const Marker = ({ position, text, onClick, onMouseOver }) => {
  return (
    <GoogleMapsMarker
      onClick={onClick}
      onMouseOver={onMouseOver}
      position={position}
      // center={position}
      // options={{
      //   fillColor: "red",
      //   fillOpacity: 1,
      //   radius: 600,
      //   // clickable: true,
      //   // draggable: false,
      // }}
      zIndex={999}
      icon={{
        path: google.maps.SymbolPath.CIRCLE,
        scale: 6,
        strokeColor: "#396DFF",
        fillColor: "#396DFF",
        fillOpacity: 1,
      }}
      label={{
        text: text || "",
        color: "#271076",
        fontSize: "40px",
      }}
    />
  );
};

export default Marker;
