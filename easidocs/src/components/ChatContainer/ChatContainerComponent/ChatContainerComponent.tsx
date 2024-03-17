import './ChatContainerComponent.css';
import ChatHistoryContainerComponent from '../ChatHistoryContainerComponent/ChatHistoryContainerComponent';
import ChatInputContainerComponent from '../ChatInputContainerComponent/ChatInputContainerComponent';
import { useState } from 'react';
import { Message } from '../ChatHistoryContainerComponent/ChatHistoryContainerComponent';

function ChatContainerComponent() {
  const [chatHistory, setChatHistory] = useState<Message[]>([]);

  const addChatToHistory = (message: Message) => {
    setChatHistory(prevHistory => [...prevHistory, message]);
  };
  
  return (
    <div className="chat-container">
      <ChatHistoryContainerComponent chatHistory={chatHistory} />
      <ChatInputContainerComponent onSendMessage={addChatToHistory} />
    </div>
  );
}

export default ChatContainerComponent;
