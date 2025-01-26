import React, { createContext, useState, useContext } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";
import Header from "./components/Header";
import Hero from "./components/Hero";
import HowItWorks from "./components/HowItWorks";
import MapViewPage from "./components/MapViewPage";
import Chat from "./components/Chat";
import DiscoverMontreal from "./components/DiscoverMontreal";
import AboutUs from "./components/AboutUs";
import ViewList from "./components/ViewList";
import "./App.css";

const LanguageContext = createContext();

export const useLanguage = () => useContext(LanguageContext);

function LanguageSwitcher() {
  const { switchLanguage } = useLanguage();
  return (
    <div className="language-switcher">
      <button onClick={() => switchLanguage("en")}>EN</button>
      <span className="slash">/</span>
      <button onClick={() => switchLanguage("fr")}>FR</button>
    </div>
  );
}

function App() {
  const [language, setLanguage] = useState("en");
  const location = useLocation();

  const switchLanguage = (lang) => setLanguage(lang);

  return (
    <LanguageContext.Provider value={{ language, switchLanguage }}>
      <div className="app">
        {/* Always show language switcher */}
        <LanguageSwitcher />

        {/* Show the background only on the homepage */}
        {location.pathname === "/" && <div className="image" />}

        {/* Show the Header only on the homepage */}
        {location.pathname === "/" && <Header />}

        {/* Define routes */}
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Hero />
                <HowItWorks />
              </>
            }
          />
          <Route path="/DiscoverMontreal" element={<DiscoverMontreal />} />
          <Route path="/AboutUs" element={<AboutUs />} />
          <Route path="/mapview" element={<MapViewPage />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/viewlist" element={<ViewList />} />
        </Routes>
      </div>
    </LanguageContext.Provider>
  );
}

export default App;
