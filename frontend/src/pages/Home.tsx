import * as React from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardHeader, CardTitle, CardContent } from "../components/ui/Card";
import { SimulationForm } from "../components/simulation/SimulationForm";
import { useNotification } from "../hooks/useNotification";
import { useSimulation } from "../hooks/useSimulation";
import type { SimulationSchema } from "../schemasZod/simulation";
import { Activity, Settings, BarChart3 } from "lucide-react";


const TEAM_MEMBERS = [
  { initials: "JP", name: "Penazzi Juan Ignacio" },
  { initials: "SI", name: "Samocachan Ignacio" },
  { initials: "AJ", name: "Arrigoni Juan Ignacio" },
  { initials: "GO", name: "García Osella Olivia Agostina" },
  { initials: "SF", name: "Saccone Facundo" },
  { initials: "WM", name: "Weller Maitena" },
  { initials: "QL", name: "Quiroga Lucía" },
  { initials: "PA", name: "Paez Areli" },
];

export const Home = () => {
  const navigate = useNavigate();
  const { success } = useNotification();
  const { getDefaultConfig } = useSimulation();
  const [defaultConfig, setDefaultConfig] = React.useState<any>(null);

  React.useEffect(() => {
    getDefaultConfig().then(config => {
      if (config) setDefaultConfig(config);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleSubmit = (data: SimulationSchema) => {
    success("Configuración validada. Iniciando simulación...");
    navigate("/processing", { state: { config: data } });
  };

  return (
    <div className="min-h-screen bg-[#fcf8ff] flex flex-col font-sans">
      {/* Navbar */}
      <header className="flex items-center justify-between px-8 py-4 bg-[#fcf8ff] border-b border-[#e8e8e8]">
        <div className="text-2xl font-bold text-[#5651b6]">Frido</div>
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-[#666666]">
        </nav>
        <div className="flex items-center gap-4">
          <a href="http://localhost:8000/docs" className="text-sm font-medium text-[#666666] hover:text-[#181925] hidden md:block">Documentation</a>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 w-full max-w-6xl mx-auto px-4 py-16 space-y-24">

        {/* Hero Section */}
        <div className="text-center space-y-6 flex flex-col items-center">
          <div className="bg-[#f3eff8] p-4 rounded-2xl text-[#5651b6]">
            <BarChart3 size={32} />
          </div>
          <h1 className="text-4xl md:text-5xl font-semibold text-[#181925]">
            Trabajo Practico #3 –  <span className="text-[#5651b6]">Simulación De Montecarlo</span>
          </h1>
        </div>

        {/* Simulation Cards Section */}
        <div className="grid grid-cols-1  gap-8 items-start">

          {/* Right Card: Form */}
          <Card className="border-[#e8e8e8] shadow-sm h-[600px] flex flex-col">
            <CardHeader className="pb-4 shrink-0">
              <div className="flex items-center gap-2">
                <Settings className="w-5 h-5 text-[#5651b6]" />
                <CardTitle className="text-lg">Configuración de Simulación</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="flex-1 min-h-0">
              {defaultConfig ? (
                <SimulationForm onSubmitData={handleSubmit} defaultConfig={defaultConfig} />
              ) : (
                <div className="flex justify-center p-12 text-[#999999]">Cargando configuración por defecto...</div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Team Section */}
        <div className="space-y-12">
          <div className="text-center space-y-2">
            <h2 className="text-2xl font-semibold text-[#181925]">GRUPO 19</h2>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {TEAM_MEMBERS.map((member, idx) => (
              <Card key={idx} className="border-[#e8e8e8] shadow-sm bg-white">
                <CardContent className="p-6 flex flex-col items-center text-center space-y-4">
                  <div className="w-16 h-16 rounded-full bg-[#f3eff8] text-[#5651b6] flex items-center justify-center text-xl font-semibold">
                    {member.initials}
                  </div>
                  <p className="text-sm font-medium text-[#181925] leading-snug">
                    {member.name}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

      </main>

      {/* Footer */}
      <footer className="w-full bg-[#fcf8ff] border-t border-[#e8e8e8] py-8 px-8 mt-12">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-[#999999]">
          <div className="flex flex-col gap-1">
            <span className="font-semibold text-[#181925] text-sm">Frido</span>
            <p>© 2026 Grupo 19 | TRABAJO PRACTICO #3 – SIMULACION DE MONTECARLO | UNIVERSIDAD TECNOLOGICA NACIONAL - FACULTAD REGIONAL CÓRDOBA</p>
          </div>
        </div>
      </footer>
    </div>
  );
};
