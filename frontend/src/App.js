import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "@/pages/HomePage";
import SeasonPage from "@/pages/SeasonPage";
import SimulationPage from "@/pages/SimulationPage";
import { RealityListPage, RealityDetailPage } from "@/pages/RealityPage";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/temporadas" element={<HomePage />} />
          <Route path="/temporadas/:year" element={<SeasonPage />} />
          <Route path="/simulacao/:id" element={<SimulationPage />} />
          <Route path="/realidade" element={<RealityListPage />} />
          <Route path="/realidade/:id" element={<RealityDetailPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
