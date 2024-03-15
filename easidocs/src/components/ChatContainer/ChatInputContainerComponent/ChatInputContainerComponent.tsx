import './ChatInputContainerComponent.css';
function ChatInputContainerComponent() {
    return (
      <div className="chat-input-container">
        <div className="chat-input-element-container">
          <input type="text" className="chat-input" placeholder="Ask a question..."></input>
          <button type="button" className="btn btn-primary">Send</button>
        </div>
      </div>
    );
  }
  

export default ChatInputContainerComponent;