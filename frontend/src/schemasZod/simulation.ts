import { z } from "zod";

export const simulationSchema = z.object({
  n: z.number().min(1).max(1000000),
  fila_desde: z.number().min(1),
  cant_visibles: z.number().min(1).max(1000),
  lineas_prob: z.array(z.number()).length(3),
  lineas_etapas: z.array(z.number()).length(3),
  p_detencion_intermedia: z.number().min(0).max(1),
  detencion_media_seg: z.number().min(0),
  detencion_desv_seg: z.number().min(0),
  p_ajuste_tecnico: z.number().min(0).max(1),
  factor_ajuste: z.number().min(0),
  etapa_tiempo_min: z.number().min(0),
  etapa_tiempo_max: z.number().min(0),
  p_parada_extra: z.number().min(0).max(1),
  parada_extra_min: z.number().min(0),
});

export type SimulationSchema = z.infer<typeof simulationSchema>;
