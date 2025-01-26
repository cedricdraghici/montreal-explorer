import React from 'react';
import { useLanguage } from '../App';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

function Hero() {
  const { language } = useLanguage();
  const navigate = useNavigate(); // Initialize useNavigate

  const translations = {
    en: {
      title: 'Welcome to Montréal Explorer!',
      subtitle: "Your personal AI-powered guide to the city's best events, hidden gems, and tailored adventures.",
      button: 'Start your journey',
    },
    fr: {
      title: 'Bienvenue à Montréal Explorer!',
      subtitle: 'Votre guide personnalisé alimenté par l’IA pour les meilleurs événements, trésors cachés et aventures sur mesure.',
      button: 'Commencez votre aventure',
    },
  };

  // Function to handle button click
  const handleStartJourney = () => {
    navigate('/map-view'); // Navigate to the Map View page
  };

  return (
    <div className="hero">
      <h2 className="hero-title">{translations[language].title}</h2>
      <p className="hero-subtitle">{translations[language].subtitle}</p>
      <button className="hero-button" onClick={handleStartJourney}>
        {translations[language].button}
      </button>
    </div>
  );
}

export default Hero;
