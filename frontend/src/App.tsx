import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "sonner";
import { Home } from "./pages/Home";
import { Processing } from "./pages/Processing"
import { Results } from "./pages/Results";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[#fcf8ff]">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/processing" element={<Processing />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      </div>
      <Toaster position="top-right" />
    </BrowserRouter>
  );
}

export default App;
