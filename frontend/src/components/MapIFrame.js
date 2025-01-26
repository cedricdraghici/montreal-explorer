import React from 'react';

const MapIFrame = () => {
  return (
    <div style={{ width: '100%', height: '600px' }}>
      <iframe
        src="http://127.0.0.1:4000/map"  // or wherever your Flask app runs
        width="100%"
        height="100%"
        style={{ border: 'none' }}
        title="Map"
      />
    </div>
  );
};

export default MapIFrame;