import React from 'react';
import { Marker as GoogleMapsMarker } from '@react-google-maps/api';

const Marker = ({ position, text }) => {
  return (
    <GoogleMapsMarker
      position={position}
      zIndex={999}
      icon={{
        path: google.maps.SymbolPath.BACKWARD_OPEN_ARROW,
        scale: 6,
        strokeColor: 'red',
        fillColor: 'red',
        fillOpacity: 1,
      }}
      label={{
        text: text || '',
        color: 'white',
        fontSize: '400px',
      }}
    />
  );
};

export default Marker;