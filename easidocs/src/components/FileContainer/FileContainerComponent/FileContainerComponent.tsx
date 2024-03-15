import React, { useEffect, useState } from 'react';
import FileListComponent from '../FileListComponent/FileListComponent';
import './FileContainerComponent.css';
import { listen } from '@tauri-apps/api/event'

function FileContainerComponent() {
  const [dragging, setDragging] = useState(false);
  const [fileNames, setFileNames] = useState<string[]>([]);

  const dragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragging(true);

  };

  const dragLeave = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragging(false);
  };

  useEffect(() => {
    const unlisten = listen('tauri://file-drop', event => {
      
      const payload = event.payload; 
      console.log(payload);
      if (Array.isArray(payload)) {
        const newFileNames = payload.map(path => path.split('/').pop() || '');
        setFileNames(existingFileNames => [...existingFileNames, ...newFileNames]);
        console.log(newFileNames[0]);
        console.log(payload[0])
      }

      setDragging(false);
    });

    return () => {
      unlisten.then((fn) => fn());
    };
  }, []);

  return (
    <div
      className="file-container"
    >
      <h1 id="file-title">easiDocs</h1>
      <FileListComponent files={fileNames} />
        <div
          className={`dropZone ${dragging ? 'dragging' : ''}`}
          onDragOver={(e) => dragOver(e)}
          onDragLeave={(e) => dragLeave(e)}>
          DROP FILES
        </div>
      </div>

  );
}

export default FileContainerComponent;