import React from "react";
import person1Photo from "../assets/Cedric.jpg";
import person2Photo from "../assets/Fuka.PNG";
import person3Photo from "../assets/Sara.png";
import person4Photo from "../assets/Malachi.png";
import "./AboutUs.css";
import homeIcon from "../assets/homeBlue.svg"; // Home Icon import


function AboutUs() {
  const teamMembers = [
    {
      name: "Cedric",
      intro: "",
      photo: person1Photo,
    },
    {
      name: "Fuka",
      intro: "",
      photo: person2Photo,
    },
    {
      name: "Sara",
      intro: "",
      photo: person3Photo,
    },
    {
      name: "Malachi",
      intro: "",
      photo: person4Photo,
    },
  ];

  return (
    <div className="about-us-container">
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
      <h1 className="about-us-title">About Us</h1>
      <div className="team-grid">
        {teamMembers.map((member, index) => (
          <div key={index} className="team-member">
            <img src={member.photo} alt={member.name} className="team-member-photo" />
            <h2 className="team-member-name">{member.name}</h2>
            <p className="team-member-intro">{member.intro}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AboutUs;
