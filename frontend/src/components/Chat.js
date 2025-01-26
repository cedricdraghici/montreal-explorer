import React, { useState } from "react";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [pendingResponse, setPendingResponse] = useState(false);

  const handleSendMessage = async () => {
    if (input.trim() === "" || pendingResponse) return;

    const userMessage = input;
    setInput("");
    
    const initialLength = messages.length;
    const assistantMessageIndex = initialLength + 1;

    setMessages(prev => [
      ...prev,
      { text: userMessage, sender: "user" },
      { text: "", sender: "recipient", isStreaming: true }
    ]);
    
    setPendingResponse(true);

    try {
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

            if (data.finished) {
              setPendingResponse(false);
            }
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
    backgroundColor: message.sender === "user" ? "#007BFF" : "#f0f0f0",
    color: message.sender === "user" ? "white" : "black",
    position: 'relative',
  });

  return (
    <div style={styles.container}>
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
          placeholder="Type a message..."
          onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
          disabled={pendingResponse}
        />
        <button 
          style={styles.sendButton} 
          onClick={handleSendMessage}
          disabled={pendingResponse}
        >
          {pendingResponse ? '...' : 'Send'}
        </button>
      </div>
      <style>{`
        @keyframes pulse {
          0% { opacity: 1; }
          50% { opacity: 0.2; }
          100% { opacity: 1; }
        }
      `}</style>
    </div>
  );
}

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
    '&:disabled': {
      backgroundColor: "#ccc",
      cursor: "not-allowed"
    }
  },
};

export default Chat;