import * as React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, RefreshCw, Settings, BarChart3 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { useHistorial } from "../hooks/useHistorial";

type Estadisticas = {
  tiempo_promedio_traslado: number;
  pct_detencion_y_parada_extra: number;
  cant_sin_detencion_ni_extra: number;
  tiempo_maximo: number;
  tiempo_minimo: number;
  distribucion_lineas: Record<string, any>;
  tiempo_promedio_por_linea: Record<string, any>;
  pct_tiempo_perdido_detenciones: number;
};

type SimulacionDetalle = {
  id: string;
  creada_en: string;
  n: number;
  seed: number | null;
  config: Record<string, any>;
  estadisticas: Estadisticas;
};

const formatFecha = (iso: string) =>
  new Date(iso).toLocaleString("es-AR", {
    day: "2-digit", month: "2-digit", year: "numeric",
    hour: "2-digit", minute: "2-digit", second: "2-digit",
  });

const formatNum = (n: number, dec = 4) =>
  n.toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: dec });

const labelMap: Record<string, string> = {
  tiempo_promedio_traslado: "Tiempo promedio de traslado (min)",
  pct_detencion_y_parada_extra: "% ciclos con detención + parada extra",
  cant_sin_detencion_ni_extra: "Ciclos sin detención ni parada extra",
  tiempo_maximo: "Tiempo máximo (min)",
  tiempo_minimo: "Tiempo mínimo (min)",
  pct_tiempo_perdido_detenciones: "% tiempo perdido en detenciones",
};

const configLabelMap: Record<string, string> = {
  n: "Iteraciones (n)",
  seed: "Seed",
  fila_desde: "Fila desde",
  cant_visibles: "Filas visibles",
  lineas_prob: "Probabilidades de líneas",
  lineas_etapas: "Etapas por línea",
  p_detencion_intermedia: "P(detención intermedia)",
  detencion_media_seg: "Media detención (seg)",
  detencion_desv_seg: "Desv. detención (seg)",
  p_ajuste_tecnico: "P(ajuste técnico)",
  factor_ajuste: "Factor de ajuste",
  etapa_tiempo_min: "T. mínimo etapa (min)",
  etapa_tiempo_max: "T. máximo etapa (min)",
  p_parada_extra: "P(parada extra)",
  parada_extra_min: "T. parada extra (min)",
};

const formatConfigVal = (v: any): string => {
  if (v === null || v === undefined) return "—";
  if (Array.isArray(v)) return v.join(", ");
  if (typeof v === "number") return formatNum(v, 4);
  return String(v);
};

const formatStatVal = (key: string, val: any): string => {
  if (typeof val === "number") {
    if (key.startsWith("pct_")) return `${(val * 100).toFixed(2)}%`;
    return formatNum(val, 4);
  }
  return String(val);
};

export const SimulacionDetalleView = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [sim, setSim] = React.useState<SimulacionDetalle | null>(null);
  const [cargando, setCargando] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const { getDetalle } = useHistorial();

  React.useEffect(() => {
    if (!id) return;
    setCargando(true);
    getDetalle(id)
      .then((data) => {
        if (data) setSim(data);
        else setError("No se encontró la simulación.");
      })
      .catch(() => setError("No se encontró la simulación o el backend no responde."))
      .finally(() => setCargando(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const stats = sim?.estadisticas;
  const statsEscalares = stats
    ? Object.entries(stats).filter(([, v]) => typeof v !== "object")
    : [];
  const statsComplejas = stats
    ? Object.entries(stats).filter(([, v]) => typeof v === "object" && v !== null)
    : [];

  return (
    <div className="min-h-screen bg-[#fcf8ff] flex flex-col font-sans">
      {/* Navbar */}
      <header className="flex items-center justify-between px-8 py-4 bg-[#fcf8ff] border-b border-[#e8e8e8]">
        <div className="text-2xl font-bold text-[#5651b6] cursor-pointer" onClick={() => navigate("/")}>Frido</div>
        <div className="flex items-center gap-4">
          <a href="http://localhost:8000/docs" className="text-sm font-medium text-[#666666] hover:text-[#181925] hidden md:block">Documentation</a>
        </div>
      </header>

      <main className="flex-1 w-full max-w-6xl mx-auto px-4 py-10 space-y-6">
        {/* Encabezado */}
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate("/historial")} className="px-2 border border-[#e8e8e8]">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Historial
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-[#181925]">Detalle de Simulación</h1>
            {sim && (
              <p className="text-sm text-[#666666] mt-0.5 font-mono">{sim.id}</p>
            )}
          </div>
        </div>

        {/* Cargando */}
        {cargando && (
          <div className="flex justify-center items-center py-24 text-[#999999]">
            <RefreshCw className="w-5 h-5 animate-spin mr-3" />
            Cargando detalle...
          </div>
        )}

        {/* Error */}
        {!cargando && error && (
          <Card className="border-red-200 bg-red-50">
            <CardContent className="pt-6 text-center text-red-600">{error}</CardContent>
          </Card>
        )}

        {/* Contenido */}
        {!cargando && sim && (
          <>
            {/* Metadata */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Card className="bg-[#f3eff8] border-[#d4cff0]">
                <CardContent className="pt-5">
                  <p className="text-xs text-[#888888] uppercase font-semibold mb-1">Fecha</p>
                  <p className="text-sm font-semibold text-[#181925]">{formatFecha(sim.creada_en)}</p>
                </CardContent>
              </Card>
              <Card className="bg-[#def6e4] border-[#a8e6b8]">
                <CardContent className="pt-5">
                  <p className="text-xs text-[#888888] uppercase font-semibold mb-1">Iteraciones</p>
                  <p className="text-3xl font-bold text-[#181925]">{sim.n.toLocaleString("en-US")}</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-5">
                  <p className="text-xs text-[#888888] uppercase font-semibold mb-1">Seed</p>
                  <p className="text-2xl font-bold text-[#181925]">{sim.seed ?? <span className="text-[#aaaaaa] italic text-base">Sin seed</span>}</p>
                </CardContent>
              </Card>
              <Card className="bg-[#dad9fc] border-[#b5b3f0]">
                <CardContent className="pt-5">
                  <p className="text-xs text-[#888888] uppercase font-semibold mb-1">T. Promedio</p>
                  <p className="text-3xl font-bold text-[#5651b6]">{formatNum(sim.estadisticas.tiempo_promedio_traslado)} <span className="text-sm font-normal text-[#888888]">min</span></p>
                </CardContent>
              </Card>
            </div>

            {/* Estadísticas escalares */}
            <Card>
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-[#5651b6]" />
                  <CardTitle className="text-lg">Indicadores</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {statsEscalares.map(([key, val]) => (
                    <div key={key} className="rounded-xl bg-[#fafafa] border border-[#e8e8e8] p-4">
                      <p className="text-xs text-[#888888] mb-1 leading-snug">
                        {labelMap[key] ?? key.replace(/_/g, " ")}
                      </p>
                      <p className="text-xl font-bold text-[#181925]">
                        {formatStatVal(key, val as number)}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Estadísticas complejas */}
            {statsComplejas.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {statsComplejas.map(([key, val]) => (
                  <Card key={key}>
                    <CardHeader className="pb-3">
                      <CardTitle className="text-base capitalize">
                        {key.replace(/_/g, " ")}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        {Object.entries(val as Record<string, any>).map(([subKey, subVal]) => (
                          <div key={subKey} className="flex justify-between items-start border-b border-[#e8e8e8] last:border-0 pb-2 last:pb-0">
                            <span className="text-sm text-[#666666]">{subKey}</span>
                            <span className="text-sm font-semibold text-[#181925] text-right ml-4">
                              {typeof subVal === "object"
                                ? Object.entries(subVal).map(([k, v]) => `${k}: ${formatNum(v as number)}`).join(" · ")
                                : formatNum(subVal as number)}
                            </span>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* Configuración usada */}
            <Card>
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <Settings className="w-5 h-5 text-[#5651b6]" />
                  <CardTitle className="text-lg">Configuración usada</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {Object.entries(sim.config).map(([key, val]) => (
                    <div key={key} className="rounded-xl bg-[#fafafa] border border-[#e8e8e8] p-4">
                      <p className="text-xs text-[#888888] mb-1">
                        {configLabelMap[key] ?? key.replace(/_/g, " ")}
                      </p>
                      <p className="text-sm font-semibold text-[#181925] break-all">
                        {formatConfigVal(val)}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </>
        )}
      </main>

      <footer className="w-full bg-[#fcf8ff] border-t border-[#e8e8e8] py-6 px-8">
        <div className="max-w-6xl mx-auto text-xs text-[#999999]">
          © 2026 Grupo 19 · UTN FRC · TP#3 Simulación de Montecarlo
        </div>
      </footer>
    </div>
  );
};
