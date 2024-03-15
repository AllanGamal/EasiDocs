import './FileListComponent.css';

export function FileListComponent() {
    const files = ['File 1', 'File 2', 'File 3', 'File 4', 'File 5', 'File 6', 'File 7', 'File 8']; // Dynamic data could be passed here
  
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
  