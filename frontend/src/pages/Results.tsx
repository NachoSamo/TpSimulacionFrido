import * as React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Card, CardHeader, CardTitle, CardContent } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { ArrowLeft, Download } from "lucide-react";

export const Results = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const config = location.state?.config;
  const result = location.state?.result;

  if (!config || !result) {
    navigate("/");
    return null;
  }

  const stats = result.estadisticas || {};
  const filas = result.filas_visibles || [];

  const formatValue = (val: any, isTable: boolean = false): string => {
    if (typeof val === "number") {
      if (Number.isInteger(val)) return val.toString();
      const decimals = isTable ? 2 : 4;
      return val.toLocaleString("en-US", {
        minimumFractionDigits: 0,
        maximumFractionDigits: decimals
      });
    }
    if (typeof val === "object" && val !== null) {
      if (Array.isArray(val)) {
        return `[${val.map(v => formatValue(v, isTable)).join(", ")}]`;
      }
      return Object.entries(val)
        .map(([k, v]) => `${k}: ${formatValue(v, isTable)}`)
        .join(" | ");
    }
    return String(val ?? "-");
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6 pt-12 pb-12 px-4 bg-[#fcf8ff] min-h-screen">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-8 gap-4">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate("/")} className="px-2 border border-[#e8e8e8]">
            <ArrowLeft className="w-5 h-5 mr-2" />
            Volver
          </Button>
          <h1 className="text-3xl font-bold text-[#181925]">Resultados de Simulación</h1>
        </div>
      </div>

      {/* General Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <Card className="bg-[#def6e4] border-[#33c758] border-opacity-20 shadow-sm">
          <CardContent className="pt-6">
            <p className="text-sm font-medium text-[#666666]">Iteraciones Simuladas</p>
            <h3 className="text-3xl font-bold text-[#181925] mt-2">{result.n}</h3>
          </CardContent>
        </Card>
        {Object.entries(stats)
          .filter(([, value]) => typeof value !== 'object' || value === null)
          .map(([key, value]: [string, any], idx) => (
            <Card key={idx} className="shadow-sm">
              <CardContent className="pt-6 flex flex-col justify-between h-full">
                <p className="text-sm font-medium text-[#666666] capitalize truncate mb-2" title={key.replace(/_/g, ' ')}>
                  {key.replace(/_/g, ' ')}
                </p>
                <h3 className="text-2xl font-bold text-[#181925] truncate" title={formatValue(value)}>
                  {formatValue(value)}
                </h3>
              </CardContent>
            </Card>
          ))}
      </div>

      {/* Complex Stats Grid (Objects/Arrays) */}
      {Object.entries(stats).filter(([, value]) => typeof value === 'object' && value !== null).length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          {Object.entries(stats)
            .filter(([, value]) => typeof value === 'object' && value !== null)
            .map(([key, value]: [string, any], idx) => (
              <Card key={`complex-${idx}`} className="shadow-sm">
                <CardContent className="pt-6 h-full flex flex-col">
                  <p className="text-sm font-medium text-[#666666] capitalize truncate mb-4" title={key.replace(/_/g, ' ')}>
                    {key.replace(/_/g, ' ')}
                  </p>
                  <div className="flex flex-col gap-2 mt-auto">
                    {Object.entries(value).map(([subKey, subValue]: [string, any]) => (
                      <div key={subKey} className="flex items-center justify-between text-sm border-b border-[#e8e8e8] last:border-0 pb-2 last:pb-0">
                        <span className="text-[#666666] font-medium">{subKey}</span>
                        <span className="font-bold text-[#181925] text-right">{formatValue(subValue)}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Filas Visibles ({filas.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto border border-[#e8e8e8] rounded-xl max-h-[500px]">
            {filas.length > 0 ? (
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-[#666666] uppercase bg-[#f0ecf6] sticky top-0">
                  <tr>
                    {Object.keys(filas[0]).map(k => (
                      <th key={k} className="px-4 py-3 border-b whitespace-nowrap">{k}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {filas.map((row: any, i: number) => (
                    <tr key={i} className="border-b last:border-0 hover:bg-[#fafafa]">
                      {Object.keys(filas[0]).map(k => (
                        <td key={k} className="px-4 py-3 whitespace-nowrap">{formatValue(row[k], true)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="p-8 text-center text-[#999999]">No hay filas para mostrar</div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
