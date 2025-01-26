import React from "react";
import { useLanguage } from "../App"; // Import the LanguageContext hook
import person1Photo from "../assets/Cedric.jpg";
import person2Photo from "../assets/Fuka.PNG";
import person3Photo from "../assets/Sara.png";
import person4Photo from "../assets/Malachi.png";
import homeIcon from "../assets/homeBlue.svg"; // Home Icon import
import "./AboutUs.css";

function AboutUs() {
  const { language } = useLanguage(); // Access current language

  // Translations for team members and the page
  const translations = {
    en: {
      title: "About Us",
      teamMembers: [
        { name: "Cedric", intro: "" },
        { name: "Fuka", intro: "" },
        { name: "Sara", intro: "" },
        { name: "Malachi", intro: "" },
      ],
    },
    fr: {
      title: "Notre Équipe",
      teamMembers: [
        { name: "Cédric", intro: "" },
        { name: "Fuka", intro: "" },
        { name: "Sara", intro: "" },
        { name: "Malachi", intro: "" },
      ],
    },
  };

  // Get the translated content based on the selected language
  const { title, teamMembers } = translations[language];

  return (
    <div className="about-us-container">
      {/* Home Icon */}
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

      {/* Page Title */}
      <h1 className="about-us-title">{title}</h1>

      {/* Team Members */}
      <div className="team-grid">
        {teamMembers.map((member, index) => (
          <div key={index} className="team-member">
            <img
              src={[person1Photo, person2Photo, person3Photo, person4Photo][index]} // Assign corresponding photo
              alt={member.name}
              className="team-member-photo"
            />
            <h2 className="team-member-name">{member.name}</h2>
            <p className="team-member-intro">{member.intro}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AboutUs;
