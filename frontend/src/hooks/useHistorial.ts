import { useCallback, useState } from "react";
import { historialService } from "../services/api";
import { useNotification } from "./useNotification";

export const useHistorial = () => {
  const [isLoading, setIsLoading] = useState(false);
  const { error } = useNotification();

  const getHistorial = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await historialService.getHistorial();
      return data;
    } catch (err: any) {
      error("Error al obtener el historial de simulaciones.");
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [error]);

  const getDetalle = useCallback(async (id: string) => {
    setIsLoading(true);
    try {
      const data = await historialService.getDetalle(id);
      return data;
    } catch (err: any) {
      error("Error al obtener el detalle de la simulación.");
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [error]);

  return { getHistorial, getDetalle, isLoading };
};