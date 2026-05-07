import * as React from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, Clock, Hash, TrendingUp, ChevronRight, RefreshCw, Database } from "lucide-react";
import { Card, CardContent } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { useHistorial } from "../hooks/useHistorial";

type SimulacionItem = {
  id: string;
  creada_en: string;
  n: number;
  seed: number | null;
  estadisticas: {
    tiempo_promedio_traslado: number;
    pct_detencion_y_parada_extra: number;
    cant_sin_detencion_ni_extra: number;
    tiempo_maximo: number;
    tiempo_minimo: number;
    distribucion_lineas: Record<string, any>;
    tiempo_promedio_por_linea: Record<string, any>;
    pct_tiempo_perdido_detenciones: number;
  };
};

const formatFecha = (iso: string) => {
  const d = new Date(iso);
  return d.toLocaleString("es-AR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const formatNum = (n: number, decimals = 2) =>
  n.toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: decimals });

export const Historial = () => {
  const navigate = useNavigate();
  const [simulaciones, setSimulaciones] = React.useState<SimulacionItem[]>([]);
  const [cargando, setCargando] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const { getHistorial } = useHistorial();

  const cargar = async () => {
    setCargando(true);
    setError(null);
    try {
      const data = await getHistorial();
      if (data) {
        setSimulaciones(data);
      } else {
        setError("Error al obtener las simulaciones.");
      }
    } catch {
      setError("No se pudo conectar al backend. Verificá que esté corriendo.");
    } finally {
      setCargando(false);
    }
  };

  React.useEffect(() => {
    cargar();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm" onClick={() => navigate("/")} className="px-2 border border-[#e8e8e8]">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Inicio
            </Button>
            <div>
              <h1 className="text-3xl font-bold text-[#181925]">Historial de Simulaciones</h1>
              <p className="text-sm text-[#666666] mt-0.5">
                {!cargando && `${simulaciones.length} registro${simulaciones.length !== 1 ? "s" : ""} guardado${simulaciones.length !== 1 ? "s" : ""}`}
              </p>
            </div>
          </div>
          <Button variant="ghost" size="sm" onClick={cargar} className="border border-[#e8e8e8]" disabled={cargando}>
            <RefreshCw className={`w-4 h-4 mr-2 ${cargando ? "animate-spin" : ""}`} />
            Actualizar
          </Button>
        </div>

        {/* Estado de carga */}
        {cargando && (
          <div className="flex justify-center items-center py-24 text-[#999999]">
            <RefreshCw className="w-5 h-5 animate-spin mr-3" />
            Cargando simulaciones...
          </div>
        )}

        {/* Error */}
        {!cargando && error && (
          <Card className="border-red-200 bg-red-50">
            <CardContent className="pt-6 text-center text-red-600">{error}</CardContent>
          </Card>
        )}

        {/* Lista vacía */}
        {!cargando && !error && simulaciones.length === 0 && (
          <div className="flex flex-col items-center justify-center py-24 gap-4 text-[#999999]">
            <Database className="w-12 h-12 opacity-30" />
            <p className="text-lg font-medium">No hay simulaciones guardadas todavía</p>
            <p className="text-sm">Corré una simulación desde la pantalla de inicio</p>
            <Button onClick={() => navigate("/")} className="mt-2">Ir al inicio</Button>
          </div>
        )}

        {/* Tabla */}
        {!cargando && !error && simulaciones.length > 0 && (
          <Card className="overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-[#f0ecf6] text-xs text-[#666666] uppercase">
                  <tr>
                    <th className="px-5 py-3 text-left font-semibold">
                      <span className="flex items-center gap-1.5"><Clock className="w-3.5 h-3.5" />Fecha</span>
                    </th>
                    <th className="px-5 py-3 text-right font-semibold">
                      <span className="flex items-center gap-1.5 justify-end"><Hash className="w-3.5 h-3.5" />Iteraciones</span>
                    </th>
                    <th className="px-5 py-3 text-right font-semibold hidden md:table-cell">Seed</th>
                    <th className="px-5 py-3 text-right font-semibold">
                      <span className="flex items-center gap-1.5 justify-end"><TrendingUp className="w-3.5 h-3.5" />T. Promedio (min)</span>
                    </th>
                    <th className="px-5 py-3 text-right font-semibold hidden lg:table-cell">% Detención+Extra</th>
                    <th className="px-5 py-3 text-right font-semibold hidden lg:table-cell">T. Máx (min)</th>
                    <th className="px-5 py-3 text-right font-semibold hidden lg:table-cell">T. Mín (min)</th>
                    <th className="px-5 py-3"></th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#e8e8e8]">
                  {simulaciones.map((sim) => (
                    <tr
                      key={sim.id}
                      className="hover:bg-[#f9f6ff] cursor-pointer transition-colors"
                      onClick={() => navigate(`/historial/${sim.id}`)}
                    >
                      <td className="px-5 py-4 text-[#181925] font-medium whitespace-nowrap">
                        {formatFecha(sim.creada_en)}
                      </td>
                      <td className="px-5 py-4 text-right font-mono text-[#181925]">
                        {sim.n.toLocaleString("en-US")}
                      </td>
                      <td className="px-5 py-4 text-right text-[#666666] hidden md:table-cell">
                        {sim.seed ?? <span className="text-[#bbbbbb] italic">—</span>}
                      </td>
                      <td className="px-5 py-4 text-right font-semibold text-[#5651b6]">
                        {formatNum(sim.estadisticas.tiempo_promedio_traslado)}
                      </td>
                      <td className="px-5 py-4 text-right text-[#666666] hidden lg:table-cell">
                        {(sim.estadisticas.pct_detencion_y_parada_extra * 100).toFixed(1)}%
                      </td>
                      <td className="px-5 py-4 text-right text-[#666666] hidden lg:table-cell">
                        {formatNum(sim.estadisticas.tiempo_maximo)}
                      </td>
                      <td className="px-5 py-4 text-right text-[#666666] hidden lg:table-cell">
                        {formatNum(sim.estadisticas.tiempo_minimo)}
                      </td>
                      <td className="px-5 py-4 text-right">
                        <ChevronRight className="w-4 h-4 text-[#aaaaaa] ml-auto" />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
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
