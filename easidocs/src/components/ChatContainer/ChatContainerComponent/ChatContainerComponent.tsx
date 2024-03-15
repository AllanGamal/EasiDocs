import './ChatContainerComponent.css';
import ChatHistoryContainerComponent from '../ChatHistoryContainerComponent/ChatHistoryContainerComponent';
import ChatInputContainerComponent from '../ChatInputContainerComponent/ChatInputContainerComponent';
import { useState } from 'react';
import { Message } from '../ChatHistoryContainerComponent/ChatHistoryContainerComponent';

function ChatContainerComponent() {
  const [chatHistory, setChatHistory] = useState<Message[]>([]);

  const addChatToHistory = (message: string) => {
    const newMessage: Message = { text: message, type: 'bot' };  // Assuming all messages from this method are 'user' type
    setChatHistory([...chatHistory, newMessage]);
  };

  return (
    <div className="chat-container">
      <ChatHistoryContainerComponent chatHistory={chatHistory} />
      <ChatInputContainerComponent onSendMessage={addChatToHistory} />
    </div>
  );
}

export default ChatContainerComponent;
