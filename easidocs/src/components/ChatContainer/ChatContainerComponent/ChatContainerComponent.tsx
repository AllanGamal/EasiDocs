import './ChatContainerComponent.css';
import ChatHistoryContainerComponent from '../ChatHistoryContainerComponent/ChatHistoryContainerComponent';
import ChatInputContainerComponent from '../ChatInputContainerComponent/ChatInputContainerComponent';

function ChatContainerComponent() {
    return (
      <div className="chat-container">
        <ChatHistoryContainerComponent />
        <ChatInputContainerComponent />
      </div>
    );
  }

export default ChatContainerComponent;