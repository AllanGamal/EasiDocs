import FileListComponent from '../FileListComponent/FileListComponent';
import './FileContainerComponent.css';



function FileContainerComponent() {
  

  

  return (
    <div className="file-container">
        <h1 id="file-title">Files</h1>
        <FileListComponent />
    
      </div>
  );
}

export default FileContainerComponent;
