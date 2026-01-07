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
  query: string;
  start_time: number | null;
  end_time: number | null;
  dataset_id: string;
  page?: number;
  limit?: number;
}) => {
  const res = await apiClient.post("/search/", payload);
  return res.data;
};