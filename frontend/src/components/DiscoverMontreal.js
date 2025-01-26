import React from 'react';
import homeIcon from "../assets/homeBlue.svg"; // Home Icon import


function DiscoverMontreal() {
  return (
    
    <div className="DiscoverMontreal" style={{ padding: '2rem', fontFamily: 'Inter, sans-serif', backgroundColor: '#FFFCF2', color: '#335058' }}>
      <header style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: '700', color: '#335058', padding:'1rem'}}>Discover Montreal</h1>
        <p style={{ fontSize: '1.3rem', color: '#335058' }}>
          Welcome to Montreal, where culture, cuisine, and creativity come together. Explore and savor the beauty of this vibrant city.
        </p>
      </header>
      <a href="/" style={{
        position: 'absolute', // Position the button relative to the parent container
        top: '3.2rem', // Adjust the vertical position (higher on the page)
        left: '2.5rem', // Adjust the horizontal position (e.g., near the left edge)
        }}>
        <img className="home-icon" src={homeIcon} alt="Home Icon" style={{
          width: '40px', // Set icon size
          height: '40px',
          cursor: 'pointer', // Add a pointer cursor for interaction
        }} />
      </a>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '0.5rem',
        padding: '1rem',
        borderRadius: '1rem',
        backgroundColor: '#ffffff',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)'
      }}>
        <div >
          <img src="https://media.timeout.com/images/105465851/1536/864/image.webp" alt="Old Montreal" style={{ width: '100%', height: '80%' }} />
          <p style={{ padding: '0.30rem', color: '#335058', fontWeight: '500',  textAlign: 'center'}}>Old Montreal</p>
        </div>
        <div >
          <img src="https://afar.brightspotcdn.com/dims4/default/a75cc9f/2147483647/strip/true/crop/728x500+36+0/resize/1320x906!/format/webp/quality/90/?url=https%3A%2F%2Fk3-prod-afar-media.s3.us-west-2.amazonaws.com%2Fbrightspot%2F36%2F75%2F7b5fba5584a9fea9565455a3ddef%2Foriginal-mountroyalpark-acx-acp77466-perry-mastrovito-agefotostock.jpg" alt="Mount Royal" style={{ width: '100%', height: '80%' }} />
          <p style={{ padding: '0.3rem', color: '#335058', fontWeight: '500', textAlign: 'center'  }}>Mount Royal Beaver Lake</p>
        </div>
        <div>
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Schwartz_smoked_meat_montreal.JPG/2560px-Schwartz_smoked_meat_montreal.JPG" alt="Food Scene" style={{ width: '100%', height: '80%' }} />
          <p style={{ padding: '0.3rem', color: '#335058', fontWeight: '500', textAlign: 'center'}}>Smoked Meat Sandwich </p>
        </div>
        <div>
          <img src="https://zestykits.s3.us-west-2.amazonaws.com/wp-content/uploads/2020/06/17220012/poutine.png" alt="Festivals" style={{ width: '100%', height: '80%' }} />
          <p style={{ padding: '0.3rem', color: '#335058', fontWeight: '500',textAlign: 'center' }}>Poutine</p>
        </div>
        <div >
          <img src="https://a.travel-assets.com/findyours-php/viewfinder/images/res70/508000/508484-notre-dame-basilica-montreal.jpg" alt="Art and Culture" style={{ width: '100%', height: '80%' }} />
          <p style={{ padding: '0.3rem', color: '#335058', fontWeight: '500', textAlign: 'center' }}>Basilique Notre-Dame</p>
        </div>
        <div >
          <img src="https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcSWz9EM7dt-PqNGWQ_v_A4nkhMpOdXLC51ycAqrBHh6SzcDlV2gi3W7_jmLvk8cPYHt_IpszRsFmoJGusDm_5RFOisRywOZouqamb4Spw" alt="Art and Culture" style={{ width: '100%', height: '80%' }} />
          <p style={{ padding: '0.3rem', color: '#335058', fontWeight: '500', textAlign: 'center' }}>Oratoire St-Joseph</p>
        </div>
        <div >
          <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Nick_Suzuki%28nicolas_suzuki%29.jpg" alt="Art and Culture" style={{ width: '100%', height: '80%' }} />
          <p style={{ padding: '0.3rem', color: '#335058', fontWeight: '500',  textAlign: 'center' }}>Montreal Canadiens</p>
        </div>
        <div >
          <img src="https://a.travel-assets.com/findyours-php/viewfinder/images/res70/49000/49384-Montreal-Museum-Of-Fine-Arts.jpg" alt="Art and Culture" style={{ width: '100%', height: '80%' }} />
          <p style={{ padding: '0.30rem', color: '#335058', fontWeight: '500', textAlign: 'center' }}>Montreal Museum of Fine Arts</p>
        </div>
        
        

      </div>

      <footer style={{ textAlign: 'center', marginTop: '2rem', color: '#335058'}}>
        <p style={{ fontSize: '1.1rem', color: '#335058', fontWeight: '700'}}>Designed with care to highlight the charm of Montreal♡♡♡</p>
      </footer>
    </div>
  );
}

export default DiscoverMontreal;
