import './ChatInputContainerComponent.css';
import React, { useState } from 'react';
import axios from 'axios';
import { Message } from '../ChatHistoryContainerComponent/ChatHistoryContainerComponent';

interface Props {
  // message and type 
  onSendMessage: (message: Message) => void;
  
}



function ChatInputContainerComponent({ onSendMessage }: Props) {
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(event.target.value);
  };

  
  
  
  const handleSendClick = () => {
    const apiUrl = 'http://localhost:8001/message';
    
    
    if (message !== '') {
      setIsLoading(true);
      onSendMessage({ text: message, type: 'user' });
      setMessage('');
      axios.post(apiUrl, { message })
      .then(response => {
        setIsLoading(false);
        if (response.status === 200) {
          console.log('Message sent');
          onSendMessage({ text: response.data, type: 'bot' });
       
      
          console.log(response.data);
        } else {
          onSendMessage({ text: "Failed to send message: " + response.statusText, type: 'bot' });
          setIsLoading(false);
          setMessage('');
        }
      })
      
      .catch(error => {
        onSendMessage({text : "Failed to send message, could not connect to server.", type: 'bot' });
        setIsLoading(false);
        setMessage('');
        console.error(error);
      });
      
    }
  };

  return (
    <div className="chat-input-container" >
      <div className="chat-input-element-container">
        <input
          type="text"
          className="chat-input"
          placeholder="Ask a question..."
          value={message}
          onChange={handleInputChange}
          
        >
          
        </input>
        <button type="button" className="btn btn-primary" onClick={handleSendClick} disabled={isLoading}>
        {isLoading ? '....' : 'Send'}
        </button>
      </div>
    </div>
  );
}

export default ChatInputContainerComponent;