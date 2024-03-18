import React, { useEffect, useState } from 'react';
import FileListComponent from '../FileListComponent/FileListComponent';
import './FileContainerComponent.css';
import { listen } from '@tauri-apps/api/event'
import axios from 'axios';


function FileContainerComponent() {
  const [fileNames, setFileNames] = useState<string[]>([]);
  const [deletingFiles, setDeletingFiles] = useState<string[]>([]);
  const [uploadCount, setUploadCount] = useState(0);
  const [deletingCount, setDeletingCount] = useState(0);
  const [isOverDropZone, setIsOverDropZone] = useState(false);


  const handleDragOver = (event: React.DragEvent) => {
    console.log(isOverDropZone);
    event.preventDefault();
    setIsOverDropZone(true);
  };
  
  const handleDragLeave = () => {
    setIsOverDropZone(false);
    console.log(isOverDropZone);
  };


  const onRemoveFile = (file: string) => {
    const apiUrl = "http://localhost:8001/delete";
    setDeletingFiles(prevFiles => [...prevFiles, file]);
    setDeletingCount(prevCount => prevCount + 1);
    
    
    setTimeout(() => {
    axios.delete(apiUrl, { data: { file_path: "pdf/" + file } })
      .then(response => {
        setDeletingFiles(prevFiles => prevFiles.filter(f => f !== file));
        if (response.status === 200) {
          setFileNames(existingFileNames => existingFileNames.filter(name => name !== file));      
          console.log('File deleted');
        } else {      
          console.log('Failed to delete file');
        }
      })
      .catch(error => {    
        setDeletingFiles(prevFiles => prevFiles.filter(f => f !== file));
        console.error(error);
      })
      .finally(() => {
        setDeletingCount(prevCount => prevCount - 1);
      });;

  }, deletingCount*1000);
  }


  const handleFileUpload = (file_paths: string[]) => {
    setIsOverDropZone(false);
    
    const apiUrl = 'http://localhost:8001/upload';
    setUploadCount(prevCount => prevCount + 1);
    
    
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
      })
      .finally(() => {
        setUploadCount(prevCount => prevCount - 1);
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
    if (deletingCount > 0 || !isOverDropZone) {
      return;
    }
    
    
    const unlisten = listen('tauri://file-drop', event => {

      const filePaths = event.payload;
      if (Array.isArray(filePaths)) {

        const validFileTypes = ['pdf', 'docx', 'doc', 'txt', 'md']; // remove files from filePaths that is not pdf, docx, doc, txt, md files
        const validFilePaths = filePaths.filter(path => validFileTypes.includes(path.split('.').pop() || ''));
        const newFileNames = validFilePaths.map(path => path.split('/').pop() || '');

        // Filter out file names that already exist
        const uniqueFileNames = newFileNames.filter(name => !fileNames.includes(name));
        setFileNames(existingFileNames => [...existingFileNames, ...uniqueFileNames]); // 
        
        // Only upload files that are not already in the list
        const uniqueFilePaths = validFilePaths.filter((index) => !fileNames.includes(newFileNames[index]));
        handleFileUpload(uniqueFilePaths);
         // 

      }

  
    });
  


    return () => {
      unlisten.then((fn) => fn());
    };
  }, [deletingCount, isOverDropZone, fileNames]); // Add fileNames as a dependency

  return (
    <div className={`file-container ${uploadCount > 0 ? 'uploading' : ''}`}>
      <h1 id="file-title">easiDocs</h1>
      {uploadCount > 0 && (
        <div className="uploading-text" style={{ color: "white" }}>
          <label>Uploading</label>
          <label> Please wait...</label>
          </div>
      )}
      <div
        className={`file-container-zone ${uploadCount > 0 ? 'uploading' : ''} `}
      >
  <FileListComponent files={fileNames} onRemoveFile={onRemoveFile} deletingFiles={deletingFiles} /> 
   <div
          className={`dropZone ${deletingCount > 0 ? 'deleting' : ''} ${isOverDropZone ? 'over' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          >
          {deletingCount > 0 ? "WAIT FOR DELETION TO COMPLETE" : "DROP ZONE"}
        </div>
      </div>
    </div>

  );
}

export default FileContainerComponent;