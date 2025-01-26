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
        { name: "Cedric", intro: "I’m a 20-year-old Computer Science major at McGill University with \
            a strong passion for Artificial Intelligence, real estate, and languages. Fluent in Romanian, \
            French, and English, and with growing proficiency in Korean and Spanish, I’m deeply inspired by\
             multicultural environments and the intersection of language and AI. Beyond academics, my interests \
             include reading movie critiques and staying active through skiing, biking, and running." },
        { name: "Fuka", intro: "" },
        { name: "Sara", intro: "Hi, I’m Sara. I'm majoring in CS. For this website, I collaborated with Cedric on \
            the front-end development, which has been an exciting learning experience. Outside of coding, I enjoy skateboarding, \
            archery, and exploring new hobbies that keep life adventurous and fun!" },
        { name: "Malachi", intro: "" },
      ],
    },
    fr: {
      title: "Notre Équipe",
      teamMembers: [
        { name: "Cédric", intro: "Je suis une étudiante de 20 ans en informatique à l'Université McGill, avec une \
            grande passion pour l'intelligence artificielle, l'immobilier et les langues. Je parle couramment le roumain, \
            le français et l'anglais, et je progresse en coréen et en espagnol. Je suis profondément inspirée par les \
            environnements multiculturels et l'intersection entre les langues et l'intelligence artificielle. En dehors de \
            mes études, mes intérêts incluent la lecture de critiques de films et les activités sportives comme le ski, le vélo et la course à pied." },
        { name: "Fuka", intro: "" },
        { name: "Sara", intro: "Allô, je m'appelle Sara. Je suis étudiante en informatique. Pour ce site web, j'ai collaboré \
            avec Cedric sur le développement front-end, ce qui a été une expérience d'apprentissage passionnante. En dehors du \
            codage, j'aime faire du skateboard, du tir à l'arc et explorer de nouveaux passe-temps qui rendent la vie aventureuse et amusante !" },
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
