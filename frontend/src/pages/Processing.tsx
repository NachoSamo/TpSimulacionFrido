import * as React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Loader2 } from "lucide-react";
import { useSimulation } from "../hooks/useSimulation";
import { useNotification } from "../hooks/useNotification";

export const Processing = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const config = location.state?.config;
  const { runSimulation } = useSimulation();
  const { error } = useNotification();
  const processedRef = React.useRef(false);

  React.useEffect(() => {
    if (!config) {
      navigate("/");
      return;
    }

    if (!processedRef.current) {
      processedRef.current = true;
      runSimulation(config)
        .then(result => {
          navigate("/results", { state: { config, result } });
        })
        .catch(() => {
          error("Error en la simulación. Volviendo al inicio.");
          navigate("/");
        });
    }
  }, [config, navigate, runSimulation, error]);

  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center space-y-6 bg-[#fcf8ff]">
      <div className="relative">
        <div className="absolute inset-0 bg-[#918df6] rounded-full blur-xl opacity-20 animate-pulse"></div>
        <div className="bg-white p-6 rounded-2xl shadow-subtle border border-[#e8e8e8] relative z-10">
          <Loader2 className="w-12 h-12 text-[#918df6] animate-spin" />
        </div>
      </div>
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-bold text-[#181925]">Procesando Simulación en el Servidor</h2>
        <p className="text-[#666666]">Ejecutando modelo Monte Carlo con {config?.n || 100000} iteraciones...</p>
      </div>
    </div>
  );
};
