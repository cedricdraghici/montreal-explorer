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
        { name: "Fuka", intro: "I’m Fuka Ono Computer Science and Honours Economics major at McGill. I have a strong passion for Data Analysis, Data Science, and Machine Learning, and I love creating projects that allow me to be both creative and impactful.What excites me most is using my skills to solve real-world problems and help others through innovative solutions. I am thrilled to collaborate, learn, and build something meaningful with teammates at hackathon." },
        { name: "Sara", intro: "Hi, I’m Sara. I'm majoring in CS. For this website, I collaborated with Cedric on \
            the front-end development, which has been an exciting learning experience. Outside of coding, I enjoy skateboarding, \
            archery, and exploring new hobbies that keep life adventurous and fun!" },
        { name: "Malachi", intro: "Hi I'm Malachi, a CS and Linguistics student at McGill. This is my first time participating in a hackathon so excuse our half finished project. My personal passions lie in low-level and systems development. Rushed introduction ten minutes left :)" },
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
        { name: "Fuka", intro: "Je m’appelle Fuka Ono, je suis en double majeure en Informatique et en Économie Honours à McGill. J’ai une grande passion pour l’analyse de données, la science des données et l’apprentissage automatique, et j’adore créer des projets qui me permettent d’être à la fois créative et d’avoir un impact. Ce qui m’enthousiasme le plus, c’est d’utiliser mes compétences pour résoudre des problèmes concrets et aider les autres grâce à des solutions innovantes. Je suis ravie de collaborer, d’apprendre et de construire quelque chose de significatif avec mes coéquipiers lors de ce hackathon." },
        { name: "Sara", intro: "Allô, je m'appelle Sara. Je suis étudiante en informatique. Pour ce site web, j'ai collaboré \
            avec Cedric sur le développement front-end, ce qui a été une expérience d'apprentissage passionnante. En dehors du \
            codage, j'aime faire du skateboard, du tir à l'arc et explorer de nouveaux passe-temps qui rendent la vie aventureuse et amusante !" },
        { name: "Malachi", intro: "Salut, je m'appelle Malachi, je suis étudiant en Informatique et en Linguistique à McGill. C'est ma première participation à un hackathon, alors excusez notre projet à moitié terminé. Mes passions personnelles se trouvent dans le développement bas niveau et les systèmes. Introduction rapide, il reste dix minutes :)" },
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
