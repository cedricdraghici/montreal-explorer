import React from 'react';
import { useLanguage } from '../App';

function Hero() {
  const { language } = useLanguage();

  const translations = {
    en: {
      title: 'Welcome to Montreal Explorer!',
      subtitle: "Your personal AI-powered guide to the city's best events, hidden gems, and tailored adventures.",
      button: 'Start your journey →',
    },
    fr: {
      title: 'Bienvenue à Montréal Explorer!',
      subtitle: 'Votre guide personnalisé alimenté par l’IA pour les meilleurs événements, trésors cachés et aventures sur mesure.',
      button: 'Commencez votre aventure →',
    },
  };

  return (
    <div className="hero">
      <h2 className="hero-title">{translations[language].title}</h2>
      <p className="hero-subtitle">{translations[language].subtitle}</p>
      <button className="hero-button">{translations[language].button}</button>
    </div>
  );
}

export default Hero;
