

import rTwoodTwooLogo from "../../../assets/r2d2-logo.png";
import humanLogo from "../../../assets/human-logo.png";
import "./ChatHistoryContainerComponent.css";

interface Props {
  chatHistory: string[];
}
function ChatHistoryContainerComponent({ chatHistory }: Props) {
    return (
        <div className="chat-history-container">
            <ul className="chat-history-list list-group">
            {chatHistory && chatHistory.map((message, index) => (
                    <li key={index} className="chat-user-container user list-group-item">
                        <div className="chat-user-logo">
                            <img src={humanLogo} className="App-logo" alt="logo" />
                        </div>
                        <div className="chat-user">
                            <p className="chat-history-textfield">{message}</p>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
  }
  

export default ChatHistoryContainerComponent;