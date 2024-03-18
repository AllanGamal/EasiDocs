import './FileListComponent.css';

interface FileListComponentProps {
  files: string[];
  onRemoveFile: (file: string) => void;
  deletingFiles: string[];
}

export function FileListComponent({ files, onRemoveFile, deletingFiles }: FileListComponentProps) {
  return (
    <ul className="list-group file-list">
      {files.map((file, index) => (
        <li key={index} className={`list-group-item file-item ${deletingFiles.includes(file) ? 'deleting' : ''}`}>          <label >
            {deletingFiles.includes(file) ? 'Deleting...' : file}
          </label>
          <button 
            type="button" 
            className="btn-close btn-close-white remove-file-button" 
            onClick={() => onRemoveFile(file)}
          ></button>
        </li>
      ))}
    </ul>
  );
}

export default FileListComponent;