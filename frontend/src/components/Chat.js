import React, { useState } from "react";

function Chat() {
  const [messages, setMessages] = useState([]); // State to store the message history
  const [input, setInput] = useState(""); // State to store the current input

  // Function to handle sending a message
  const handleSendMessage = () => {
    if (input.trim() !== "") {
      // Add the user's message
      setMessages([...messages, { text: input, sender: "user" }]);
      setInput(""); // Clear the input

      // Simulate a response from the recipient after a short delay
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: "This is a response from the recipient.", sender: "recipient" },
        ]);
      }, 1000); // 1 second delay
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