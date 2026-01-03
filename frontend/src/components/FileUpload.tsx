import { useState } from "react";
import { uploadFiles } from "../services/eventService";

interface Props {
  onSuccess: (data: any) => void;
}

const FileUpload = ({ onSuccess }: Props) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    try {
      const data =  await uploadFiles(file);
      console.log("Upload successful", data);
      if (data.dataset_id){
          onSuccess(data.dataset_id);
      }
        
    
    } catch (err) {
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <input
        type="file"
        accept=".tgz"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="border p-2 border-black rounded w-full bg-gray-200 text-black placeholder-gray-400 cursor-pointer"
      />
      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
};

export default FileUpload;
