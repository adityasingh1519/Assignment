import { useNavigate } from "react-router-dom";
import FileUpload from "../components/FileUpload";

const UploadPage = () => {
  const navigate = useNavigate();

  const handleSuccess = (dataset_id: string) => {
    sessionStorage.setItem("uploadedEventdataset_id", dataset_id);
    navigate("/search");
  };

  return (
    <div className="p-6 max-w-xl mx-auto ">
      <h1 className="text-xl font-semibold mb-4">Upload Event Files</h1>
      <FileUpload onSuccess={handleSuccess} />
    </div>
  );
};

export default UploadPage;
