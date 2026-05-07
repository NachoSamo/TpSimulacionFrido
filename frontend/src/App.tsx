import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "sonner";
import { Home } from "./pages/Home";
import { Processing } from "./pages/Processing"
import { Results } from "./pages/Results";
import { Historial } from "./pages/Historial";
import { SimulacionDetalleView } from "./pages/SimulacionDetalle";
function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[#fcf8ff]">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/processing" element={<Processing />} />
          <Route path="/results" element={<Results />} />
          <Route path="/historial" element={<Historial />} />
          <Route path="/historial/:id" element={<SimulacionDetalleView />} />
        </Routes>
      </div>
      <Toaster position="top-right" />
    </BrowserRouter>
  );
}

export default App;
