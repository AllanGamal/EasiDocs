import { useState } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import FileContainerComponent from "./components/FileContainer/FileContainerComponent/FileContainerComponent";
import ChatContainerComponent from "./components/ChatContainer/ChatContainerComponent/ChatContainerComponent";

function App() {
  const [greetMsg, setGreetMsg] = useState("");
  const [name, setName] = useState("");

  async function greet() {
    // Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
    setGreetMsg(await invoke("greet", { name }));
  }

  return (
    <div className="main-container">
      <FileContainerComponent />
      <ChatContainerComponent />

    </div>
  );
}

export default App;
