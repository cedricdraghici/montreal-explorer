import React from 'react';

const MapIFrame = (props) => {
  const sessionId = props.session_id;
  return (
    <div style={{ width: '1900px', height: '100%' }}>
      <iframe
        src={"http://10.122.141.184:4000/map"}
        width="100%"
        height="100%"
        style={{ border: 'none' }}
        title="Map"
      />
    </div>
  );
};

export default MapIFrame;