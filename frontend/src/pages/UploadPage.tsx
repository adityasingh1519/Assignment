import { useNavigate } from "react-router-dom";
import FileUpload from "../components/FileUpload";

const UploadPage = () => {
  const navigate = useNavigate();

  const handleSuccess = (dataset_id: string) => {
    sessionStorage.setItem("uploadedEventdataset_id", dataset_id);
    navigate("/search");
  };

  return (
      <FileUpload onSuccess={handleSuccess} />
  );
};

export default UploadPage;
