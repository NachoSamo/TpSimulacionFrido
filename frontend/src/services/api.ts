import axios from "axios";
import type { SimulationSchema } from "../schemasZod/simulation";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export const simulationService = {
  getDefaultConfig: async () => {
    const response = await api.get("/simulacion/config-default");
    return response.data;
  },
  runSimulation: async (data: SimulationSchema) => {
    const response = await api.post("/simulacion/run", data);
    return response.data;
  },
};
