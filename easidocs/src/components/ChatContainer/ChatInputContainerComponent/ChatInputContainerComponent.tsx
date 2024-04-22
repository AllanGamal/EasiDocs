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
  const [isEnglish, setIsEnglish] = useState(true);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(event.target.value);
  };

  const toggleLanguage = () => {
    setIsEnglish(!isEnglish)
  }




  const handleSendClick = () => {
    const apiUrl = 'http://localhost:8001/message';


    if (message !== '') {
      setIsLoading(true);
      onSendMessage({ text: message, type: 'user'});
      setMessage('');
      axios.post(apiUrl, { message, is_english: isEnglish }, { timeout: 1000*60*60 }) // 1 hour timeout, default seems to be 1min
        .then(response => {
          setIsLoading(false);
          if (response.status === 200) {
            console.log('Message sent');
            // go ghrough the source list and print out the source
            console.log("test")
            console.log(response.data.answer);
            console.log(response.data.pageContents);
            let newMetadata = response.data.metadata;
            let newPageContents = response.data.pageContents;
            
            // go through the pageContents list and check if there is less that 100 characters
            for (let i = 0; i < newPageContents.length; i++) {
              if (response.data.pageContents[i].length < 100) {
                newPageContents.splice(i, 1);
                newMetadata.splice(i, 1);
                i--;
              }
            }

            onSendMessage({ text: response.data.answer, type: 'bot', metadata: newMetadata, pageContents: newPageContents});
            console.log(response.data);
            
          } else {
            onSendMessage({ text: "Failed to send message: " + response.statusText, type: 'bot'});
            setIsLoading(false);
            setMessage('');
          }
        })

        .catch(error => {
          onSendMessage({ text: "Failed to send message, could not connect to server.", type: 'bot'});
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
          onKeyPress={(event) => {
            if (event.key === 'Enter') {
              handleSendClick();
            }
          }}

        >

        </input>
        <div className="language-container">

          <input type="checkbox" className="btn-check language-btn" id="btn-check" autoComplete="off" onClick={toggleLanguage} >
          </input>
          <label className="btn btn-primary language-label" htmlFor="btn-check">{isEnglish ? "EN" : "SV"}</label>
        </div>
        <button type="button" className="btn btn-primary" onClick={handleSendClick} disabled={isLoading} >
          {isLoading ? '....' : 'Send'}
        </button>
        
      </div>
    </div>
  );
}

export default ChatInputContainerComponent;