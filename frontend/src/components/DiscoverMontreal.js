import React from "react";
import { useLanguage } from "../App"; // Import LanguageContext hook
import homeIcon from "../assets/homeBlue.svg"; // Home Icon import

function DiscoverMontreal() {
  const { language } = useLanguage(); // Get the current language

  const translations = {
    en: {
      title: "Discover Montreal",
      description:
        "Welcome to Montreal, where culture, cuisine, and creativity come together. Explore and savor the beauty of this vibrant city.",
      footer: "Designed with care to highlight the charm of Montreal♡♡♡",
      places: [
        { name: "Old Montreal", image: "https://media.timeout.com/images/105465851/1536/864/image.webp" },
        { name: "Mount Royal Beaver Lake", image: "https://afar.brightspotcdn.com/dims4/default/a75cc9f/2147483647/strip/true/crop/728x500+36+0/resize/1320x906!/format/webp/quality/90/?url=https%3A%2F%2Fk3-prod-afar-media.s3.us-west-2.amazonaws.com%2Fbrightspot%2F36%2F75%2F7b5fba5584a9fea9565455a3ddef%2Foriginal-mountroyalpark-acx-acp77466-perry-mastrovito-agefotostock.jpg" },
        { name: "Smoked Meat Sandwich", image: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Schwartz_smoked_meat_montreal.JPG/2560px-Schwartz_smoked_meat_montreal.JPG" },
        { name: "Poutine", image: "https://zestykits.s3.us-west-2.amazonaws.com/wp-content/uploads/2020/06/17220012/poutine.png" },
        { name: "Basilique Notre-Dame", image: "https://a.travel-assets.com/findyours-php/viewfinder/images/res70/508000/508484-notre-dame-basilica-montreal.jpg" },
        { name: "Oratoire St-Joseph", image: "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcSWz9EM7dt-PqNGWQ_v_A4nkhMpOdXLC51ycAqrBHh6SzcDlV2gi3W7_jmLvk8cPYHt_IpszRsFmoJGusDm_5RFOisRywOZouqamb4Spw" },
        { name: "Montreal Canadiens", image: "https://upload.wikimedia.org/wikipedia/commons/5/55/Nick_Suzuki%28nicolas_suzuki%29.jpg" },
        { name: "Montreal Museum of Fine Arts", image: "https://a.travel-assets.com/findyours-php/viewfinder/images/res70/49000/49384-Montreal-Museum-Of-Fine-Arts.jpg" },
      ],
    },
    fr: {
      title: "Découvrez Montréal",
      description:
        "Bienvenue à Montréal, où la culture, la cuisine et la créativité se rejoignent. Explorez et savourez la beauté de cette ville vibrante.",
      footer: "Conçu avec soin pour mettre en valeur le charme de Montréal♡♡♡",
      places: [
        { name: "Vieux-Montréal", image: "https://media.timeout.com/images/105465851/1536/864/image.webp" },
        { name: "Lac des Castors, Mont-Royal", image: "https://afar.brightspotcdn.com/dims4/default/a75cc9f/2147483647/strip/true/crop/728x500+36+0/resize/1320x906!/format/webp/quality/90/?url=https%3A%2F%2Fk3-prod-afar-media.s3.us-west-2.amazonaws.com%2Fbrightspot%2F36%2F75%2F7b5fba5584a9fea9565455a3ddef%2Foriginal-mountroyalpark-acx-acp77466-perry-mastrovito-agefotostock.jpg" },
        { name: "Sandwich à la viande fumée", image: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Schwartz_smoked_meat_montreal.JPG/2560px-Schwartz_smoked_meat_montreal.JPG" },
        { name: "Poutine", image: "https://zestykits.s3.us-west-2.amazonaws.com/wp-content/uploads/2020/06/17220012/poutine.png" },
        { name: "Basilique Notre-Dame", image: "https://a.travel-assets.com/findyours-php/viewfinder/images/res70/508000/508484-notre-dame-basilica-montreal.jpg" },
        { name: "Oratoire Saint-Joseph", image: "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcSWz9EM7dt-PqNGWQ_v_A4nkhMpOdXLC51ycAqrBHh6SzcDlV2gi3W7_jmLvk8cPYHt_IpszRsFmoJGusDm_5RFOisRywOZouqamb4Spw" },
        { name: "Canadiens de Montréal", image: "https://upload.wikimedia.org/wikipedia/commons/5/55/Nick_Suzuki%28nicolas_suzuki%29.jpg" },
        { name: "Musée des beaux-arts de Montréal", image: "https://a.travel-assets.com/findyours-php/viewfinder/images/res70/49000/49384-Montreal-Museum-Of-Fine-Arts.jpg" },
      ],
    },
  };

  const { title, description, footer, places } = translations[language];

  return (
    <div
      className="DiscoverMontreal"
      style={{
        padding: "2rem",
        fontFamily: "Newsreader",
        backgroundColor: "#FFFCF2",
        color: "#335058",
      }}
    >
      <header style={{ textAlign: "center", marginBottom: "2rem" }}>
        <h1 style={{ fontSize: "2.5rem", fontWeight: "700", color: "#335058", padding: "1rem" }}>
          {title}
        </h1>
        <p style={{ fontSize: "1.3rem", color: "#335058" }}>{description}</p>
      </header>
      <a
        href="/"
        style={{
          position: "absolute",
          top: "3.2rem",
          left: "2.5rem",
        }}
      >
        <img
          className="home-icon"
          src={homeIcon}
          alt="Home Icon"
          style={{
            width: "40px",
            height: "40px",
            cursor: "pointer",
          }}
        />
      </a>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: "0.5rem",
          padding: "1rem",
          borderRadius: "1rem",
          backgroundColor: "#ffffff",
          boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
        }}
      >
        {places.map((place, index) => (
          <div key={index}>
            <img src={place.image} alt={place.name} style={{ width: "100%", height: "80%" }} />
            <p style={{ padding: "0.3rem", color: "#335058", fontWeight: "500", textAlign: "center" }}>
              {place.name}
            </p>
          </div>
        ))}
      </div>

      <footer style={{ textAlign: "center", marginTop: "2rem", color: "#335058" }}>
        <p style={{ fontSize: "1.1rem", color: "#335058", fontWeight: "700" }}>{footer}</p>
      </footer>
    </div>
  );
}

export default DiscoverMontreal;
