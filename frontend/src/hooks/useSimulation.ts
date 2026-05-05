import { useState } from "react";
import { simulationService } from "../services/api";
import { useNotification } from "./useNotification";
import type { SimulationSchema } from "../schemasZod/simulation";

export const useSimulation = () => {
  const [isLoading, setIsLoading] = useState(false);
  const { error } = useNotification();

  const getDefaultConfig = async () => {
    try {
      return await simulationService.getDefaultConfig();
    } catch (err: any) {
      error("Error al obtener configuración por defecto desde el backend.");
      return null;
    }
  };

  const runSimulation = async (data: SimulationSchema) => {
    setIsLoading(true);
    try {
      const res = await simulationService.runSimulation(data);
      setIsLoading(false);
      return res;
    } catch (err: any) {
      setIsLoading(false);
      error(err.response?.data?.detail?.[0]?.msg || "Falló la ejecución de la simulación.");
      throw err;
    }
  };

  return { getDefaultConfig, runSimulation, isLoading };
};
