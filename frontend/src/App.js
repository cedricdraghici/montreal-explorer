import React, { createContext, useState, useContext } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import HowItWorks from './components/HowItWorks';
import './App.css';

// Create Language Context
const LanguageContext = createContext();

export const useLanguage = () => useContext(LanguageContext);


function LanguageSwitcher() {
    const { switchLanguage } = useLanguage();
    return (
      <div className="language-switcher">
        <button onClick={() => switchLanguage('en')}>EN</button>
        <button onClick={() => switchLanguage('fr')}>FR</button>
      </div>
    );
  }

function App() {
  const [language, setLanguage] = useState('en'); // Default: English

  const switchLanguage = (lang) => setLanguage(lang);

  return (
    <LanguageContext.Provider value={{ language, switchLanguage }}>
      <div className="app">
        <div className="image">
          <LanguageSwitcher /> {/* Add the Language Switcher */}
          <Header />
          <Hero />
          <HowItWorks />
        </div>
      </div>
    </LanguageContext.Provider>
  );
}



export default App;