import './ChatInputContainerComponent.css';
import React, { useState } from 'react';

interface Props {
  onSendMessage: (message: string) => void;
}



function ChatInputContainerComponent({ onSendMessage }: Props) {
  const [message, setMessage] = useState('');

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(event.target.value);
  };
  
  
  const handleSendClick = () => {
    onSendMessage(message);
    console.log(message);  // Lägg till denna för att se uppdateringar
    setMessage('');
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