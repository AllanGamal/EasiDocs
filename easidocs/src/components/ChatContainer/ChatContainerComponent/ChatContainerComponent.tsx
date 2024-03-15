import './ChatContainerComponent.css';
import ChatHistoryContainerComponent from '../ChatHistoryContainerComponent/ChatHistoryContainerComponent';
import ChatInputContainerComponent from '../ChatInputContainerComponent/ChatInputContainerComponent';
import { useState } from 'react';

function ChatContainerComponent() {
  const [chatHistory, setChatHistory] = useState<string[]>([]);

  const addChatToHistory = (message: string) => {
    setChatHistory([...chatHistory, message]);
  };

  return (
    <div className="chat-container">
      <ChatHistoryContainerComponent chatHistory={chatHistory} />
      <ChatInputContainerComponent onSendMessage={addChatToHistory} />
    </div>
  );
}

export default ChatContainerComponent;
