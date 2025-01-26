import React from 'react';
import { useLanguage } from '../App'; 

function HowItWorks() {
  const { language } = useLanguage();

  const translations = {
    en: {
        title: 'How to Explore with Us',
        step1Title:'1. Customize Your Interests',
        step1Details: 'Let us know how you plan to explore Montreal! \
                Share your preferences for transportation, the length of your stay, \
                your budget, and the experiences you’re most excited about—whether\
                it’s gourmet dining, live music, stand-up comedy, or cultural adventures.',
        step2Title: '2. Get Recommendations',
        step2Details: 'Based on your interests, explore a personalized list of events \
                and activities happening around you. From exclusive concerts to hidden culinary \
                gems, discover options tailored just for you!',
        step3Title: '3. Start Your Adventure',
        step3Details: 'Experience the best of Montreal like never before. With your personalized \
                guide, navigate the city’s vibrant offerings and create unforgettable memories! \
                                                                                  \n             '
      
    },
    fr: {
        title: 'Comment Explorer avec Nous',
    },
  };
  return(
    <div className="HowItWorks">
        <h1 className="title">{translations[language].title}</h1>
        <div className="Step1">
            <h2 className="step1Title">{translations[language].step1Title}</h2>
            <p className="step1Details">{translations[language].step1Details}</p>
        </div>
        <div className="Step2">
            <h2 className="step2Title">{translations[language].step2Title}</h2>
            <p className="step2Details">{translations[language].step2Details}</p>
        </div>
        <div className="Step3">
          <h2 className="step3Title">{translations[language].step3Title}</h2>
          <p className="step3Details">{translations[language].step3Details}</p>
        </div>
    </div>
  )
}
export default HowItWorks