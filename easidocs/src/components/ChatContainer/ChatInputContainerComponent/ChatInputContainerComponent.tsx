import './ChatInputContainerComponent.css';
import React, { useState } from 'react';
import axios from 'axios';

interface Props {
  onSendMessage: (message: string) => void;
}



function ChatInputContainerComponent({ onSendMessage }: Props) {
  const [message, setMessage] = useState('');

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(event.target.value);
  };
  
  
  const handleSendClick = () => {
    const apiUrl = 'http://localhost:8000/message';
    
    if (message !== '') {
    axios.post(apiUrl, { message })
      .then(response => {
        console.log("response");
  
        if (response.status === 200) {
          console.log('Message sent');
          onSendMessage(message);
          setMessage('');
        } else {
          onSendMessage("Failed to send message: " + response.status + " - " + response.statusText);
          setMessage('');
        }
      })
      
      .catch(error => {
        onSendMessage("Failed to send message, could not connect to server.");
        setMessage('');
        console.error(error);
      });
      
    }
  };

  return (
    <div className="chat-input-container">
      <div className="chat-input-element-container">
        <input
          type="text"
          className="chat-input"
          placeholder="Ask a question..."
          value={message}
          onChange={handleInputChange}
        ></input>
        <button type="button" className="btn btn-primary" onClick={handleSendClick}>Send</button>
      </div>
    </div>
  );
}

export default ChatInputContainerComponent;