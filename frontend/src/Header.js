import React from 'react';
import { useLanguage } from '../App'; 

function Header() {
  const { language } = useLanguage();

  const translations = {
    en: {
      header: 'Montreal Explorer',
      aboutMontreal: 'ABOUT MONTREAL',
      aboutUs: 'ABOUT US',
    },
    fr: {
      header: 'Montréal Explorer',
      aboutMontreal: 'DÉCOUVREZ MONTRÉAL',
      aboutUs: 'DÉCOUVREZ-NOUS',
    },
  };

  return (
    <header className="headerSection">
      <div className="header">
        {translations[language].header.split(' ')[0]}{' '}
        <span style={{ fontSize: '50px' }}>
          {translations[language].header.split(' ')[1]}
        </span>
      </div>
      <nav>
        <ul className="nav-list">
          <li><a href="#About Montreal">{translations[language].aboutMontreal}</a></li>
          <li><a href="#About Us">{translations[language].aboutUs}</a></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
