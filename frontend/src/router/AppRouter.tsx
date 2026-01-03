import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import UploadPage from "../pages/UploadPage";
import SearchPage from "../pages/SearchPage";

const AppRouter = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Navigate to="/upload" />} />
      <Route path="/upload" element={<UploadPage />} />
      <Route path="/search" element={<SearchPage />} />
    </Routes>
  </BrowserRouter>
);

export default AppRouter;
