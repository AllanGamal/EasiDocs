

import reactLogo from "../../../assets/react.svg";
import "./ChatHistoryContainerComponent.css";
function ChatHistoryContainerComponent() {
    return (
      <div className="chat-history-container">
        <ul className="chat-history-list list-group">
        <li className="chat-user-container user list-group-item">
            <div className="chat-user-logo">
              <img src={reactLogo} className="App-logo" alt="logo" />
            </div>

            <div className="chat-user">
              <p className="chat-history-textfield">This is a test question from the user</p>
            </div>
          </li>

          <li className="chat-user-container bot list-group-item">
            <div className="chat-user-logo">
              <img src={reactLogo} className="App-logo" alt="logo" />
            </div>
            <div className="chat-user">
              <p className="chat-history-textfield">This is a test answer from the bot</p>
            </div>
          </li>
          <li className="chat-user-container user list-group-item">
            <div className="chat-user-logo">
              <img src={reactLogo} className="App-logo" alt="logo" />
            </div>

            <div className="chat-user">
              <p className="chat-history-textfield">This is a test question from the user</p>
            </div>
          </li>

          <li className="chat-user-container bot list-group-item">
            <div className="chat-user-logo">
              <img src={reactLogo} className="App-logo" alt="logo" />
            </div>
            <div className="chat-user">
              <p className="chat-history-textfield">This is a test answer from the bot</p>
            </div>
          </li>
          <li className="chat-user-container user list-group-item">
            <div className="chat-user-logo">
              <img src={reactLogo} className="App-logo" alt="logo" />
            </div>

            <div className="chat-user">
              <p className="chat-history-textfield">This is a test question from the user</p>
            </div>
          </li>

          <li className="chat-user-container bot list-group-item">
            <div className="chat-user-logo">
              <img src={reactLogo} className="App-logo" alt="logo" />
            </div>
            <div className="chat-user">
              <p className="chat-history-textfield">This is a test answer from the bot</p>
            </div>
          </li>
        </ul>
      </div>
    );
  }
  

export default ChatHistoryContainerComponent;