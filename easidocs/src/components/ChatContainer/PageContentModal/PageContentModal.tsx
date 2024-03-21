import Modal from 'react-modal';
// import css
import './PageContentModal.css';
Modal.setAppElement('#root');

interface Props {
    modalIsOpen: boolean;
    closeModal: () => void;
    link: string | null;
    pageContents: string[] | null;
}

function PageContentModal({ modalIsOpen, closeModal, link, pageContents }: Props) {

    
    return (
        <Modal
            className="modal-main"
            isOpen={modalIsOpen}
            onRequestClose={closeModal}
            contentLabel="Page Contents"
            style={{
                overlay: {
                    backgroundColor: 'rgba(0, 0, 0, 0.5)',
                }
                
            }}
            
        >
            <div className="button-title-container">

            <h2>Source:&nbsp;&nbsp;&nbsp;{link}</h2>
            <button className="btn btn-close btn-close-white"onClick={closeModal}></button>
            </div>
            {pageContents?.map((content, index) => (
                <p key={index}>{content}</p>
            ))}
            
        </Modal>
    );
}

export default PageContentModal;