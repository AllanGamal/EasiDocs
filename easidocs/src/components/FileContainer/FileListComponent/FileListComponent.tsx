import './FileListComponent.css';
import React from 'react';

interface FileListComponentProps {
  files: string[]; // Assuming files is an array of strings
}


export function FileListComponent({ files }: FileListComponentProps) {
    return (
      <ul className="list-group file-list">
        {files.map((file, index) => (
          <li key={index} className="list-group-item file-item">
            <label>{file}</label>
            <button type="button" className="btn-close btn-close-white remove-file-button" ></button>
          </li>
        ))}
      </ul>
    );
}

export default FileListComponent;
