import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate for navigation
import rectangle from "../assets/rectangle.svg";
import curvedRec from "../assets/curved-rec.svg";
import collapseIcon from "../assets/collapse.svg";
import restaurantsIcon from "../assets/restaurants.svg";
import cafesIcon from "../assets/cafes.svg";
import historicalIcon from "../assets/historical.svg";
import artCultureIcon from "../assets/artculture.svg";
import parksIcon from "../assets/parks.svg";
import viewListIcon from "../assets/viewlist.svg";
import plusIcon from "../assets/plus.svg";
import sendButtonIcon from "../assets/send-button.svg";
import homeIcon from "../assets/home.svg";
import "./MapViewPage.css";
import "./MapIFrame.js";
import MapIFrame from "./MapIFrame.js";

function MapViewPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [pendingResponse, setPendingResponse] = useState(false);
  const [hoveredIndex, setHoveredIndex] = useState(null);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const navigate = useNavigate(); // Initialize useNavigate for navigation

  const handleCollapseClick = () => {
    setIsCollapsed((prev) => !prev);
  };

  const handleSendMessage = async () => {
    if (input.trim() === "" || pendingResponse) return;

    const userMessage = input;
    setInput("");

    const assistantIndex = messages.length + 1;

    setMessages((prev) => [
      ...prev,
      { text: userMessage, sender: "user" },
      { text: "", sender: "assistant", isStreaming: true },
    ]);

    setPendingResponse(true);

    try {
      const response = await fetch("http://10.122.141.184:4000/gpt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, user_message: userMessage }),
      });

      if (!response.ok) throw new Error("Request failed");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const chunks = buffer.split("\n\n");

        for (let i = 0; i < chunks.length - 1; i++) {
          const chunk = chunks[i].trim();
          if (!chunk.startsWith("data: ")) continue;

          try {
            const data = JSON.parse(chunk.slice(6));

            if (data.session_id) {
              setSessionId(data.session_id);
            }

            if (data.delta) {
              setMessages((prev) =>
                prev.map((msg, index) =>
                  index === assistantIndex
                    ? {
                        ...msg,
                        text: msg.text + data.delta,
                        isStreaming: !data.finished,
                      }
                    : msg
                )
              );
            }

            if (data.finished) {
              setPendingResponse(false);
            }
          } catch (error) {
            console.error("Error parsing chunk:", error);
          }
        }
        buffer = chunks[chunks.length - 1];
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) =>
        prev.map((msg, index) =>
          index === assistantIndex
            ? {
                text: error.message,
                sender: "assistant",
              }
            : msg
        )
      );
      setPendingResponse(false);
    }
  };

  const handleViewListClick = () => {
    navigate("/viewlist"); // Navigate to the ViewList page
  };

  return (
    <div className="macbook-pro">
      <div className="div">
        {/* Home icon */}
        <div className="home-container">
          <a href="/">
            <img className="home-icon" src={homeIcon} alt="Home Icon" />
          </a>
        </div>

        {/* Right panel */}
        <div className={`right-panel ${isCollapsed ? "collapsed" : ""}`}>
          <div className="rectangle">
            <MapIFrame />
          </div>
          <img className="curved-rec" src={curvedRec} alt="Curved Background" />
          <img
            className="collapse"
            src={collapseIcon}
            alt="Collapse Icon"
            onClick={handleCollapseClick}
          />
          <img className="restaurants" src={restaurantsIcon} alt="Restaurants Icon" />
          <img className="cafes" src={cafesIcon} alt="Cafes Icon" />
          <img className="historical" src={historicalIcon} alt="Historical Icon" />
          <img className="artculture" src={artCultureIcon} alt="Art & Culture Icon" />
          <img className="parks" src={parksIcon} alt="Parks Icon" />
          <img
            className="viewlist"
            src={viewListIcon}
            alt="View List Icon"
            onClick={handleViewListClick}
            style={{ cursor: "pointer" }} // Make cursor a pointer for click indication
          />
        </div>

        {/* Input bar */}
        <div className="overlap-group">
          <input
            className="askany"
            type="text"
            placeholder="Ask anything..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
            disabled={pendingResponse}
          />
          <img className="plus" src={plusIcon} alt="Plus Icon" />
          <img
            className="send-button"
            src={sendButtonIcon}
            alt="Send Button"
            onClick={handleSendMessage}
          />
        </div>

        {/* Messages */}
        <div
          style={{
            position: "absolute",
            top: "48%",
            left: "12%",
            transform: "translate(-25%, -50%)",
            width: "50.7%",
            height: "70%",
            padding: "20px",
            overflowY: "auto",
            backgroundColor: "transparent",
            borderRadius: "10px",
            display: "flex",
            flexDirection: "column",
            gap: "10px",
          }}
        >
          {messages.map((msg, i) => {
            const isChatGPTResponse = msg.sender === "assistant";
            const isHovered = hoveredIndex === i;

            return (
              <div
                key={i}
                onMouseEnter={() => isChatGPTResponse && setHoveredIndex(i)}
                onMouseLeave={() => setHoveredIndex(null)}
                style={{
                  textAlign: "left",
                  margin: "0",
                  padding: "10px",
                  backgroundColor: isHovered
                    ? "#D9D9D9"
                    : isChatGPTResponse
                    ? "#EDEDED"
                    : "transparent",
                  borderRadius: "10px",
                  maxWidth: "100%",
                  wordWrap: "break-word",
                  alignSelf: "flex-start",
                  fontFamily:
                    '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
                  transition: "background-color 0.3s ease",
                }}
              >
                {isChatGPTResponse ? <b>{msg.text}</b> : msg.text}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default MapViewPage;
