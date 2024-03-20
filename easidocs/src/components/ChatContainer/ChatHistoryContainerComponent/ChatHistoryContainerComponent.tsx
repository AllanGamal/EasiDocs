

import rTwoodTwooLogo from "../../../assets/r2d2-logo.png";
import humanLogo from "../../../assets/human-logo.png";
import "./ChatHistoryContainerComponent.css";
import { useEffect, useRef } from "react";

export interface Message {
  text: string;
  type: 'user' | 'bot';
  source?: string[];
}

interface Props {
  chatHistory: Message[];
}
function ChatHistoryContainerComponent({ chatHistory }: Props) {
  const messagesEndRef = useRef<null | HTMLLIElement>(null);
  console.log('Chat History:', chatHistory);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  return (
    <div className="chat-history-container">
      <ul className="chat-history-list list-group">
      <li className={`chat-user-container bot list-group-item`}>
      <div className="item-container">
            <div className="chat-user-logo">
              <img src={rTwoodTwooLogo} className="App-logo" alt="logo" />
            </div>
            <div className="chat-user">
              <p className="chat-history-textfield" style={{fontWeight: "1000"}}>Whirr-beep-bloop! </p>
              <p className="chat-history-textfield">
              Ask me anything about your documents.</p>
              <p className="chat-history-textfield" style={{fontWeight: "1000"}}>Whistle-bleep!</p>
            </div>
            </div>
          </li>
        {chatHistory && chatHistory.map((message, index) => (
          <li key={index} className={`chat-user-container ${message.type} list-group-item`}>
            <div className="item-container">

            <div className="chat-user-logo">
              <img src={message.type === 'user' ? humanLogo : rTwoodTwooLogo} className="App-logo" alt="logo" />
            </div>
            <div className="chat-user">
              <p className="chat-history-textfield">{message.text}</p>
              
            </div>
            </div>
            {message.type === "bot" && message.source && message.source.length > 0 && (
  <div className="source-links-container">
    {message.type === "bot" && message.source && message.source.length > 0 ? (
  <div className="source-links-container">
    {message.source.map((link, idx) => (
      <a key={idx} className="links" href={link} target="_blank" rel="noopener noreferrer">{link}</a>
    ))}
  </div>
) : null}

  </div>
)}

          </li>
        ))}

        <li ref={messagesEndRef} />
      </ul>
    </div>
  );
}

export default ChatHistoryContainerComponent;