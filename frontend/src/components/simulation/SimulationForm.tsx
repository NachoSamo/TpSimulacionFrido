import * as React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { simulationSchema, type SimulationSchema } from "../../schemasZod/simulation";
import { Input } from "../ui/Input";
import { Button } from "../ui/Button";
import { Play } from "lucide-react";

interface SimulationFormProps {
  onSubmitData: (data: SimulationSchema) => void;
  defaultConfig?: any;
  isLoading?: boolean;
}

export const SimulationForm: React.FC<SimulationFormProps> = ({ onSubmitData, defaultConfig, isLoading }) => {
  const { register, handleSubmit, reset, formState: { errors } } = useForm<SimulationSchema>({
    resolver: zodResolver(simulationSchema),
    defaultValues: defaultConfig || {}
  });

  React.useEffect(() => {
    if (defaultConfig) {
      reset(defaultConfig);
    }
  }, [defaultConfig, reset]);

  return (
    <form onSubmit={handleSubmit(onSubmitData)} className="flex flex-col h-full max-h-[500px]">
      <div className="flex-1 overflow-y-auto pr-2 space-y-6 pb-6">
        <div className="space-y-4">
          <h4 className="text-sm font-semibold text-[#181925] border-b border-[#e8e8e8] pb-2">General</h4>
          <div className="grid grid-cols-2 gap-4">
            <Input type="number" label="Iteraciones (N)" {...register("n", { valueAsNumber: true })} error={errors.n?.message} />
            <Input type="number" label="Fila Desde" {...register("fila_desde", { valueAsNumber: true })} error={errors.fila_desde?.message} />
            <Input type="number" label="Cant. Visibles" {...register("cant_visibles", { valueAsNumber: true })} error={errors.cant_visibles?.message} />
          </div>
        </div>

        <div className="space-y-4">
          <h4 className="text-sm font-semibold text-[#181925] border-b border-[#e8e8e8] pb-2">Tiempos Etapa (min)</h4>
          <div className="grid grid-cols-2 gap-4">
            <Input type="number" step="0.1" label="Mínimo" {...register("etapa_tiempo_min", { valueAsNumber: true })} error={errors.etapa_tiempo_min?.message} />
            <Input type="number" step="0.1" label="Máximo" {...register("etapa_tiempo_max", { valueAsNumber: true })} error={errors.etapa_tiempo_max?.message} />
          </div>
        </div>

        <div className="space-y-4">
          <h4 className="text-sm font-semibold text-[#181925] border-b border-[#e8e8e8] pb-2">Ajuste Técnico</h4>
          <div className="grid grid-cols-2 gap-4">
            <Input type="number" step="0.01" label="Probabilidad" {...register("p_ajuste_tecnico", { valueAsNumber: true })} error={errors.p_ajuste_tecnico?.message} />
            <Input type="number" step="0.1" label="Factor Multiplicador" {...register("factor_ajuste", { valueAsNumber: true })} error={errors.factor_ajuste?.message} />
          </div>
        </div>

        <div className="space-y-4">
          <h4 className="text-sm font-semibold text-[#181925] border-b border-[#e8e8e8] pb-2">Detención Intermedia</h4>
          <div className="grid grid-cols-2 gap-4">
            <Input type="number" step="0.01" label="Probabilidad" {...register("p_detencion_intermedia", { valueAsNumber: true })} error={errors.p_detencion_intermedia?.message} />
            <Input type="number" step="0.1" label="Media (seg)" {...register("detencion_media_seg", { valueAsNumber: true })} error={errors.detencion_media_seg?.message} />
            <Input type="number" step="0.1" label="Desv Est (seg)" {...register("detencion_desv_seg", { valueAsNumber: true })} error={errors.detencion_desv_seg?.message} />
          </div>
        </div>

        <div className="space-y-4">
          <h4 className="text-sm font-semibold text-[#181925] border-b border-[#e8e8e8] pb-2">Parada Extra</h4>
          <div className="grid grid-cols-2 gap-4">
            <Input type="number" step="0.001" label="Probabilidad" {...register("p_parada_extra", { valueAsNumber: true })} error={errors.p_parada_extra?.message} />
            <Input type="number" step="0.1" label="Minutos" {...register("parada_extra_min", { valueAsNumber: true })} error={errors.parada_extra_min?.message} />
          </div>
        </div>
      </div>

      <div className="pt-4 border-t border-[#e8e8e8] bg-white mt-auto">
        <Button type="submit" disabled={isLoading} className="w-full bg-[#5651b6] hover:bg-[#464196] text-white py-6">
          <Play className="w-5 h-5 mr-2 fill-white" />
          {isLoading ? "Iniciando..." : "Iniciar Simulación"}
        </Button>
      </div>
    </form>
  );
};
