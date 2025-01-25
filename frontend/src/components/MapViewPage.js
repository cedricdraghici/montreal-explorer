import React from 'react';
import Chat from './Chat'; // Import the Chat component

function MapViewPage() {
  return (
    <div>
      <h1>Map View</h1>
      <p>Here is where your map or related content will be displayed.</p>
      
      {/* Add Chat Component */}
      <Chat />
    </div>
  );
}

export default MapViewPage;
