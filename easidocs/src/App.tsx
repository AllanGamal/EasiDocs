import { useState } from "react";
import reactLogo from "./assets/react.svg";
import { invoke } from "@tauri-apps/api/tauri";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
  const [greetMsg, setGreetMsg] = useState("");
  const [name, setName] = useState("");

  async function greet() {
    // Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
    setGreetMsg(await invoke("greet", { name }));
  }

  return (
    <div className="main-container">
      <div className="file-container">
        <h1 id="file-title">Files</h1>

        <ul className="list-group file-list">
          <li className="list-group-item file-item">
            <label>File 1</label>
            <button className="btn-close remove-file-button"></button>
          </li>
          <li className="list-group-item file-item">
            <label>File 2</label>
            <button className="btn-close remove-file-button"></button>
          </li>
          <li className="list-group-item file-item">
            <label>File 3</label>
            <button className="btn-close remove-file-button"></button>
          </li>
          <li className="list-group-item file-item">
            <label>File 4</label>
            <button className="btn-close remove-file-button"></button>
          </li>
          <li className="list-group-item file-item">
            <label>File 5</label>
            <button className="btn-close remove-file-button"></button>
          </li>
          <li className="list-group-item file-item">
            <label>File 6</label>
            <button className="btn-close remove-file-button"></button>
          </li>
          <li className="list-group-item file-item">
            <label>File 7</label>
            <button className="btn-close remove-file-button"></button>
          </li>
          <li className="list-group-item file-item">
            <label>File 8</label>
            <button className="btn-close remove-file-button"></button>
          </li>
        </ul>
      </div>

      <div className="chat-container">


        <ul className="chat-history-container list-group">

          <li className="chat-user-container list-group-item">
            <div className="chat-user-logo">
              <img src={reactLogo} className="App-logo" alt="logo" />
            </div>

            <div className="chat-user">
              <p className="chat-history-textfield">This is a test question from the user</p>
            </div>
          </li>

          <li className="chat-user-container list-group-item">
            <div className="chat-user-logo">
              <img src={reactLogo} className="App-logo" alt="logo" />
            </div>
            <div className="chat-bot">
              <p className="chat-history-textfield">This is a test answer from the bot</p>
            </div>
          </li>

        </ul>

        <div className="chat-input-container">
          <input type="text" className="chat-input" placeholder="Ask a question..."></input>
          <button type="button" className="btn btn-primary">Send</button>
        </div>
      </div>



    </div>
  );
}

export default App;
