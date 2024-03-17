import React, { useEffect, useState } from 'react';
import FileListComponent from '../FileListComponent/FileListComponent';
import './FileContainerComponent.css';
import { listen } from '@tauri-apps/api/event'
import axios from 'axios';

function FileContainerComponent() {
  const [dragging, setDragging] = useState(false);
  const [fileNames, setFileNames] = useState<string[]>([]);

  const onRemoveFile = (file: string) => {
    const apiUrl = "http://localhost:8001/delete";
    
    
    axios.delete(apiUrl, { data: { file_path: "pdf/" + file } })
    .then(response => {
      if (response.status === 200) {
          setFileNames(existingFileNames => existingFileNames.filter(name => name !== file));
          console.log('File deleted');
        } else {
          console.log('Failed to delete file');
        }
      })
      .catch(error => {
        console.error(error);
      });
  }

  const dragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragging(true);

  };

  const dragLeave = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragging(false);
  };

  

  const handleFileUpload = (file_paths: string[]) => {
    
    const apiUrl = 'http://localhost:8001/upload';
    console.log(file_paths);
    
    // send the array of paths to the server
    axios.post(apiUrl, { file_paths })
      .then(response => {
        if (response.status === 200) {
          console.log(response.data);
          console.log('Files uploaded');
        } else {
          console.log('Failed to upload files');
        }
      })
      .catch(error => {
        console.error(error);
      });
  }
  const loadFileList = () => {
    const apiUrl = 'http://localhost:8001/files';
    axios.get(apiUrl)
      .then(response => {
        if (response.status === 200) {
          setFileNames(response.data);
        } else {
          console.log('Failed to fetch files');
        }
      })
      .catch(error => {
        console.error(error);
      });
  }
  useEffect(() => {
    loadFileList();
  }
  , []);

  useEffect(() => {
    const unlisten = listen('tauri://file-drop', event => {
      
      const filePaths = event.payload; 
      if (Array.isArray(filePaths)) {
        
        const validFileTypes = ['pdf', 'docx', 'doc', 'txt', 'md']; // remove files from filePaths that is not pdf, docx, doc, txt, md files
        const validFilePaths = filePaths.filter(path => validFileTypes.includes(path.split('.').pop() || ''));
        const newFileNames = validFilePaths.map(path => path.split('/').pop() || '');
        setFileNames(existingFileNames => [...existingFileNames, ...newFileNames]);

        handleFileUpload(validFilePaths);
        
        
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
      <FileListComponent files={fileNames} onRemoveFile={onRemoveFile} />
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