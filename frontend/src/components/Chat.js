import React, { useState } from "react";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);

  const handleSendMessage = async () => {
    if (input.trim() === "") return;

    // Save user message immediately
    const userMessage = input;
    setInput("");
    setMessages(prev => [...prev, { text: userMessage, sender: "user" }]);

    try {
      // Send request to Flask backend
      const response = await fetch("http://127.0.0.1:5000/gpt", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          user_message: userMessage
        }),
      });

      if (!response.ok) throw new Error("Request failed");

      const data = await response.json();

      // Update session ID if received new one
      if (data.session_id && data.session_id !== sessionId) {
        setSessionId(data.session_id);
      }

      // Add AI response to messages
      setMessages(prev => [
        ...prev,
        { text: data.response, sender: "recipient" }
      ]);
    } catch (error) {
      console.error("Error:", error);
      setMessages(prev => [
        ...prev,
        { 
          text: "Sorry, I'm having trouble connecting. Please try again.", 
          sender: "recipient" 
        }
      ]);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.chatBox}>
        {messages.map((message, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              alignSelf: message.sender === "user" ? "flex-end" : "flex-start",
              backgroundColor: message.sender === "user" ? "#007BFF" : "#f0f0f0",
              color: message.sender === "user" ? "white" : "black",
            }}
          >
            {message.text}
          </div>
        ))}
      </div>
      <div style={styles.inputBox}>
        <input
          style={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
        />
        <button style={styles.sendButton} onClick={handleSendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}

// Basic styles for the chat interface
const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    height: "500px",
    width: "300px",
    border: "1px solid #ccc",
    borderRadius: "8px",
    overflow: "hidden",
  },
  chatBox: {
    flex: 1,
    padding: "10px",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "5px",
  },
  message: {
    padding: "8px 12px",
    borderRadius: "16px",
    maxWidth: "70%",
    wordWrap: "break-word",
  },
  inputBox: {
    display: "flex",
    padding: "10px",
    borderTop: "1px solid #ccc",
  },
  input: {
    flex: 1,
    padding: "8px",
    borderRadius: "8px",
    border: "1px solid #ccc",
  },
  sendButton: {
    marginLeft: "10px",
    padding: "8px 12px",
    backgroundColor: "#007BFF",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },
};

export default Chat;