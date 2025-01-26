import React from 'react';

const MapIFrame = () => {
  return (
    <div style={{ width: '100%', height: '1000px' }}>
      <iframe
        src="http://10.122.141.184:4000/map"
        width="100%"
        height="100%"
        style={{ border: 'none' }}
        title="Map"
      />
    </div>
  );
};

export default MapIFrame;