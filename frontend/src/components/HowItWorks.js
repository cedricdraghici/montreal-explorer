import React from "react";
import { useLanguage } from "../App"; // Import LanguageContext hook

// Placeholder images for steps
const stepImages = [
  "https://via.placeholder.com/400x300?text=Step+1+Image",
  "https://via.placeholder.com/400x300?text=Step+2+Image",
  "https://via.placeholder.com/400x300?text=Step+3+Image",
];

function HowItWorks() {
  const { language } = useLanguage();

  const translations = {
    en: {
      title: "How to Explore with Us",
      steps: [
        {
          title: "1. Customize Your Interests",
          description:
            "Let us know how you plan to explore Montreal! Share your preferences for transportation, the length of your stay, your budget, and the experiences you’re most excited about—whether it’s gourmet dining, live music, stand-up comedy, or cultural adventures.",
        },
        {
          title: "2. Get Recommendations",
          description:
            "Based on your interests, explore a personalized list of events and activities happening around you. From exclusive concerts to hidden culinary gems, discover options tailored just for you!",
        },
        {
          title: "3. Start Your Adventure",
          description:
            "Experience the best of Montreal like never before. With your personalized guide, navigate the city’s vibrant offerings and create unforgettable memories!",
        },
      ],
    },
    fr: {
      title: "Comment explorer avec nous",
      steps: [
        {
          title: "1. Personnalisez vos intérêts",
          description:
            "Faites-nous savoir comment vous prévoyez d’explorer Montréal ! Partagez vos préférences concernant le transport, la durée de votre séjour, votre budget, et les expériences qui vous enthousiasment le plus—que ce soit la gastronomie, la musique live, le stand-up ou les aventures culturelles.",
        },
        {
          title: "2. Recevez des recommandations",
          description:
            "En fonction de vos intérêts, découvrez une liste personnalisée d’événements et d’activités qui se déroulent autour de vous. Des concerts exclusifs aux trésors culinaires cachés, trouvez des options adaptées juste pour vous !",
        },
        {
          title: "3. Commencez l'aventure",
          description:
            "Découvrez le meilleur de Montréal comme jamais auparavant. Avec votre guide personnalisé, explorez les offres vibrantes de la ville et créez des souvenirs inoubliables !",
        },
      ],
    },
  };

  const { title, steps } = translations[language];

  return (
    <div className="HowItWorks">
      <h1 className="title">{title}</h1>
      <div className="step-container">
        {steps.map((step, index) => (
          <div key={index} className="step">
            <div className="step-details">
              <h2 className="step-title">{step.title}</h2>
              <p className="step-description">{step.description}</p>
            </div>
            <img
              src={stepImages[index]}
              alt={`Step ${index + 1}`}
              className="step-image"
            />
          </div>
        ))}
      </div>
    </div>
  );
}

export default HowItWorks;
