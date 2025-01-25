import React, { createContext, useState, useContext } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Header from "./components/Header";
import Hero from "./components/Hero";
import HowItWorks from "./components/HowItWorks";
import MapViewPage from "./components/MapViewPage"; // Correct import for MapViewPage
import Chat from "./components/Chat"; // Updated path for Chat.js
import "./App.css"; // Import your CSS file

// Create Language Context
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

  const switchLanguage = (lang) => setLanguage(lang);

  return (
    <LanguageContext.Provider value={{ language, switchLanguage }}>
      <Router>
        <div className="app">
          <div className="image">
            <LanguageSwitcher /> {/* Add the Language Switcher */}
            <Header />
            <nav>
              {/* Navigation Links */}
              <Link to="/">Home</Link>
              <Link to="/map-view">Map View</Link>
              <Link to="/chat">Chat</Link>
            </nav>
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
        </div>
      </Router>
    </LanguageContext.Provider>
  );
}

export default App;
