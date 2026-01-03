import { apiClient } from "./client";

export const uploadFiles = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await apiClient.post("/upload/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return res.data;
};

export const searchEvents = async (payload: {
  query: Record<string, string>;
  start_time: number;
  end_time: number;
  dataset_id: string;
}) => {
  const res = await apiClient.post("/search/", payload);
  return res.data;
};
