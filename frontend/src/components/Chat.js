import React, { useState } from "react";
import { ReactComponent as HomeIcon } from '../homeIcon.svg';
import { useNavigate } from 'react-router-dom'; // Import useNavigate



function Chat() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [pendingResponse, setPendingResponse] = useState(false);

  const handleSendMessage = async () => {
    if (input.trim() === "" || pendingResponse) return;

    setMessages((prev) => [
      ...prev,
      { text: input, sender: "user" },
    ]);
    setInput("");
  };

  const handleHomeButton = () => {
    navigate('/');
  };

  const messageStyles = (message) => ({
    ...styles.message,
    alignSelf: message.sender === "user" ? "flex-end" : "flex-start",
    backgroundColor: message.sender === "user" ? "#007BFF" : "#F3F3F3",
    color: message.sender === "user" ? "white" : "black",
  });


  return (
    <div style={styles.container}>
      {/* Icons Section */}
      <div style={styles.iconBar}>
        <button className="home-button" onClick={handleHomeButton}>
          <HomeIcon style={{ width: "24px", height: "24px", color: "#808080" }} />
          <span className="HomeIconText">Back to Homepage</span>
        </button>
      </div>

      {/* Chat Box */}
      <div style={styles.chatBox}>
        {messages.map((message, index) => (
          <div key={index} style={messageStyles(message)}>
            {message.text}
          </div>
        ))}
      </div>

      {/* Input Box */}
      <div style={styles.inputBox}>
        <input
          style={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything..."
          onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
        />
        <button style={styles.sendButton} onClick={handleSendMessage}>
          ➤
        </button>
      </div>

    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    height: "100vh",
    width: "40%",
    backgroundColor: "#FFF5F5",
    borderRight: "1px solid #E6E6E6",
    padding: "20px",
    boxSizing: "border-box",
  },
  iconBar: {
    display: "flex",
    gap: "20px",
    padding: "10px 0",
    borderBottom: "1px solid #E6E6E6",
  },
  chatBox: {
    flex: 1,
    overflowY: "auto",
    padding: "10px 0",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  message: {
    padding: "10px 15px",
    borderRadius: "20px",
    maxWidth: "70%",
    wordWrap: "break-word",
  },
  inputBox: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    padding: "10px 0",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "25px",
    border: "1px solid #CCC",
    backgroundColor: "#F9F9F9",
    outline: "none",
  },
  sendButton: {
    padding: "10px 15px",
    borderRadius: "50%",
    backgroundColor: "#007BFF",
    color: "white",
    border: "none",
    cursor: "pointer",

  },
};

export default Chat;
