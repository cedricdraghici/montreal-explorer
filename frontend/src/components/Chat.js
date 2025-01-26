import React, { useState } from "react";
import { ReactComponent as HomeIcon } from '../homeIcon.svg';
import { useNavigate } from 'react-router-dom';

function Chat() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [pendingResponse, setPendingResponse] = useState(false);

  
  const handleSendMessage = async () => {
    if (input.trim() === "" || pendingResponse) return;

    const userMessage = input;
    setInput("");
    const assistantMessageIndex = messages.length + 1;

    setMessages(prev => [
      ...prev,
      { text: userMessage, sender: "user" },
      { text: "", sender: "recipient", isStreaming: true }
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
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const chunks = buffer.split('\n\n');
        
        for (let i = 0; i < chunks.length - 1; i++) {
          const chunk = chunks[i].trim();
          if (!chunk.startsWith('data: ')) continue;

          try {
            const data = JSON.parse(chunk.slice(6));
            if (data.session_id) setSessionId(data.session_id);

            if (data.delta) {
              setMessages(prev => prev.map((msg, index) => 
                index === assistantMessageIndex ? {
                  ...msg,
                  text: msg.text + data.delta,
                  isStreaming: !data.finished
                } : msg
              ));
            }

            if (data.finished) setPendingResponse(false);
          } catch (error) {
            console.error('Error parsing chunk:', error);
          }
        }
        buffer = chunks[chunks.length - 1];
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages(prev => prev.map((msg, index) => 
        index === assistantMessageIndex ? {
          text: error.message,
          sender: "recipient"
        } : msg
      ));
      setPendingResponse(false);
    }
  };

  const messageStyles = (message) => ({
    ...styles.message,
    alignSelf: message.sender === "user" ? "flex-end" : "flex-start",
    backgroundColor: message.sender === "user" ? "#007BFF" : "#F3F3F3",
    color: message.sender === "user" ? "white" : "black",
    position: 'relative',
  });

  const handleHomeButton = () => navigate('/');

  return (
    <div style={styles.container}>
      <div style={styles.iconBar}>
        <button className="home-button" onClick={handleHomeButton}>
          <HomeIcon style={{ width: "24px", height: "24px", color: "#808080" }} />
          <span className="HomeIconText">Back to Homepage</span>
        </button>
      </div>

      <div style={styles.chatBox}>
        {messages.map((message, index) => (
          <div key={index} style={messageStyles(message)}>
            {message.text}
            {message.isStreaming && (
              <div style={{
                display: 'inline-block',
                marginLeft: '8px',
                animation: 'pulse 1s infinite',
                fontSize: '0.8em'
              }}>
                ●
              </div>
            )}
          </div>
        ))}
      </div>

      <div style={styles.inputBox}>
        <input
          style={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything..."
          onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
          disabled={pendingResponse}
        />
        <button 
          style={styles.sendButton} 
          onClick={handleSendMessage}
          disabled={pendingResponse}
        >
          {pendingResponse ? '...' : '➤'}
        </button>
      </div>

      <style>{`@keyframes pulse { 0% { opacity:1; } 50% { opacity:0.2; } 100% { opacity:1; } }`}</style>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    height: "100vh", // Full viewport height
    width: "100vw", // Full viewport width
    backgroundColor: "#FFF5F5",
    padding: "20px",
    boxSizing: "border-box",
    margin: "0 auto", // Center horizontally
  },
  chatBox: {
    flex: 1,
    overflowY: "auto",
    padding: "15px", // Increased padding
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    backgroundColor: "#FFFFFF",
    borderRadius: "8px",
  },
  message: {
    padding: "10px 15px",
    borderRadius: "20px",
    maxWidth: "80%",
    wordWrap: "break-word",
  },
  inputBox: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    padding: "15px 0",
  },
  input: {
    flex: 1,
    padding: "15px",
    borderRadius: "25px",
    border: "1px solid #CCC",
    backgroundColor: "#F9F9F9",
    outline: "none",
  },
  sendButton: {
    padding: "12px 18px",
    borderRadius: "50%",
    backgroundColor: "#007BFF",
    color: "white",
    border: "none",
    cursor: "pointer",
  },
};

export default Chat;