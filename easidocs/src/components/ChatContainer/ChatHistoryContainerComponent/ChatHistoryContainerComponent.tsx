

import rTwoodTwooLogo from "../../../assets/r2d2-logo.png";
import humanLogo from "../../../assets/human-logo.png";
import "./ChatHistoryContainerComponent.css";
import { useEffect, useRef, useState } from "react";
import PageContentModal from "../PageContentModal/PageContentModal";


export interface Message {
  text: string;
  type: 'user' | 'bot';
  metadata?: string[];
  pageContents?: string[];
}

interface Props {
  chatHistory: Message[];
}
function ChatHistoryContainerComponent({ chatHistory }: Props) {
  const messagesEndRef = useRef<null | HTMLLIElement>(null);
  const [currentLink, setCurrentLink] = useState<string | null>(null);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [currentPageContents, setCurrentPageContents] = useState<string[] | null>(null);

  console.log('Chat History:', chatHistory);

  const openModal = (link: string, pageContents: string[]) => {
    setCurrentLink(link);
    setCurrentPageContents(pageContents);
    setModalIsOpen(true);
  };
  
  const closeModal = () => {
    setModalIsOpen(false);
  };

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
              <p className="chat-history-textfield" style={{ fontWeight: "1000" }}>Whirr-beep-bloop! </p>
              <p className="chat-history-textfield">
                Ask me anything about your documents.</p>
              <p className="chat-history-textfield" style={{ fontWeight: "1000" }}>Whistle-bleep!</p>
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
                <p className="chat-history-textfield" dangerouslySetInnerHTML={{ __html: message.text.replace(/\n/g, '<br />') }} />
              </div>
            </div>
            {message.type === "bot" && message.metadata && message.metadata.length > 0 && (
              <div className="source-links-container">
                {message.type === "bot" && message.metadata && message.metadata.length > 0 ? (
                  <div className="source-links-container">
                    {message.metadata?.map((link, idx) => (
                      <a
                        key={idx}
                        className="links"
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => {
                          e.preventDefault();
                          openModal(link, message.pageContents ? [message.pageContents[idx]] : []);                        }}
                      >
                        {link}
                      </a>
                    ))}
                  </div>
                ) : null}

              </div>
            )}

          </li>
        ))}

        <li ref={messagesEndRef} />
      </ul>
      <PageContentModal
        modalIsOpen={modalIsOpen}
        closeModal={closeModal}
        link={currentLink}
        pageContents={currentPageContents}
      />
    </div>
  );
}

export default ChatHistoryContainerComponent;