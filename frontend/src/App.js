import React, { createContext, useState, useContext } from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import Header from "./components/Header";
import Hero from "./components/Hero";
import HowItWorks from "./components/HowItWorks";
import MapViewPage from "./components/MapViewPage";
import Chat from "./components/Chat";
import "./App.css";

const LanguageContext = createContext();

export const useLanguage = () => useContext(LanguageContext);

function LanguageSwitcher() {
  const { switchLanguage } = useLanguage();
  return (
    <div className="language-switcher">
      <button onClick={() => switchLanguage("en")}>EN</button>
      <button onClick={() => switchLanguage("fr")}>FR</button>
    </div>
  );
}

function App() {
  const [language, setLanguage] = useState("en"); // Default: English
  const location = useLocation(); // Get the current route location

  const switchLanguage = (lang) => setLanguage(lang);

  return (
    <LanguageContext.Provider value={{ language, switchLanguage }}>
      <div className="app">
        {/* Ensure LanguageSwitcher is always displayed */}
        <LanguageSwitcher />

        {/* Conditionally render the background */}
        {location.pathname === "/" && <div className="image" />}

        {/* Header is consistent across all pages */}
        {location.pathname === "/" && <Header />}

        {/* Define Routes */}
        <Routes>
          <Route
            path="/"
            element={
              <div>
                <Hero />
                <HowItWorks />
              </div>
            }
          />
          <Route path="/map-view" element={<MapViewPage />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </div>
    </LanguageContext.Provider>
  );
}

export default App;
