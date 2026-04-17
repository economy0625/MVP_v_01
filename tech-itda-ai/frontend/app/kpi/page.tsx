"use client";
import { useState } from "react";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";

interface KpiItem {
  name: string;
  target: string;
  verification: string;
  period: string;
  field: string;
}

interface ValidationResult {
  status: string;
  message: string;
  formula: string;
  corrected_value?: number;
  tip?: string;
  needs_expert_review: boolean;
}

function KpiContent() {
  const searchParams = useSearchParams();
  const company_id = searchParams.get("company_id");
  const [techGoal, setTechGoal] = useState("");
  const [kpis, setKpis] = useState<KpiItem[]>([]);
  const [validations, setValidations] = useState<{ [key: number]: ValidationResult }>({});
  const [loading, setLoading] = useState(false);
  const [validateLoading, setValidateLoading] = useState<number | null>(null);

  // KPI 생성
  const handleGenerate = async () => {
    if (!techGoal.trim()) return;
    setLoading(true);
    setKpis([]);
    setValidations({});

    try {
      const res = await fetch("https://mvpv01-production.up.railway.app/api/kpi/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          company_id: company_id,
          tech_goal: techGoal,
        }),
      });
      const data = await res.json();
console.log("API 응답:", data);
if (data.success) {
  if (data.data && data.data.kpis) {
    setKpis(data.data.kpis);
  } else if (data.data && data.data.error) {
    alert("KPI 생성 오류: " + data.data.error);
  } else {
    alert("KPI 데이터 형식이 올바르지 않습니다: " + JSON.stringify(data.data));
  }
}
    } catch (e) {
      alert("오류가 발생했습니다. 백엔드 서버를 확인해주세요.");
    }
    setLoading(false);
  };

  // KPI 물리 검증
  const handleValidate = async (index: number, kpi: KpiItem) => {
    setValidateLoading(index);
    try {
      // 목표값에서 숫자 추출 (예: "350MPa" → 350)
      const match = kpi.target.match(/[\d.]+/);
      const targetValue = match ? parseFloat(match[0]) : 0;

      const res = await fetch("https://mvpv01-production.up.railway.app/api/kpi/validate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          field: kpi.field,
          target_value: targetValue,
          unit: "%",
        }),
      });
      const data = await res.json();
      if (data.success) {
        setValidations((prev) => ({ ...prev, [index]: data.data }));
      }
    } catch (e) {
      alert("검증 중 오류가 발생했습니다.");
    }
    setValidateLoading(null);
  };

  const getStatusColor = (status: string) => {
    if (status === "달성가능") return { bg: "#dcfce7", color: "#166534", border: "#86efac" };
    if (status === "보정필요") return { bg: "#fef9c3", color: "#854d0e", border: "#fde047" };
    return { bg: "#f3f4f6", color: "#374151", border: "#d1d5db" };
  };

  return (
    <div style={{ maxWidth: 640, margin: "60px auto", padding: "0 24px" }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 8 }}>
        KPI 자동 생성
      </h1>
      <p style={{ color: "#666", marginBottom: 32 }}>
        기술 목표를 입력하면 AI가 정량 KPI를 생성하고 물리적 달성 가능성을 검증합니다
      </p>

      {/* 기술 목표 입력 */}
      <div style={{ marginBottom: 16 }}>
        <label style={{ display: "block", marginBottom: 6, fontWeight: 500 }}>
          기술 목표 입력
        </label>
        <input
          type="text"
          placeholder="예: 경량화 소재 개발, 에너지 효율 향상, 불량률 개선"
          value={techGoal}
          onChange={(e) => setTechGoal(e.target.value)}
          style={{
            width: "100%",
            padding: "12px",
            border: "1px solid #ddd",
            borderRadius: 8,
            fontSize: 14,
            color: "#000",
            background: "#fff",
          }}
        />
      </div>

      <button
        onClick={handleGenerate}
        disabled={loading || !techGoal.trim()}
        style={{
          width: "100%",
          padding: "14px",
          background: loading ? "#ccc" : "#2563eb",
          color: "#fff",
          border: "none",
          borderRadius: 8,
          fontSize: 16,
          fontWeight: 600,
          cursor: loading ? "not-allowed" : "pointer",
          marginBottom: 32,
        }}
      >
        {loading ? "AI가 KPI를 생성 중입니다..." : "KPI 자동 생성 →"}
      </button>

      {/* KPI 결과 */}
      {kpis.length > 0 && (
        <>
          <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>
            생성된 KPI ({kpis.length}개)
          </h2>
          {kpis.map((kpi, index) => (
            <div
              key={index}
              style={{
                background: "#fff",
                border: "1px solid #e5e7eb",
                borderRadius: 12,
                padding: 24,
                marginBottom: 16,
              }}
            >
              {/* KPI 기본 정보 */}
              <div style={{ marginBottom: 16 }}>
                <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 8 }}>
                  KPI {index + 1}. {kpi.name}
                </h3>
                <table style={{ width: "100%", fontSize: 14, borderCollapse: "collapse" }}>
                  <tbody>
                    <tr>
                      <td style={{ color: "#888", padding: "4px 0", width: 100 }}>목표 수치</td>
                      <td style={{ fontWeight: 600, color: "#2563eb" }}>{kpi.target}</td>
                    </tr>
                    <tr>
                      <td style={{ color: "#888", padding: "4px 0" }}>검증 방법</td>
                      <td>{kpi.verification}</td>
                    </tr>
                    <tr>
                      <td style={{ color: "#888", padding: "4px 0" }}>달성 기간</td>
                      <td>{kpi.period}</td>
                    </tr>
                    <tr>
                      <td style={{ color: "#888", padding: "4px 0" }}>검증 분야</td>
                      <td>{kpi.field}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* 물리 검증 결과 */}
              {validations[index] && (
                <div style={{
                  background: getStatusColor(validations[index].status).bg,
                  border: `1px solid ${getStatusColor(validations[index].status).border}`,
                  borderRadius: 8,
                  padding: 16,
                  marginBottom: 12,
                }}>
                  <p style={{ fontWeight: 600, color: getStatusColor(validations[index].status).color, marginBottom: 6 }}>
                    {validations[index].status === "달성가능" ? "✅" :
                     validations[index].status === "보정필요" ? "⚠️" : "❓"} {validations[index].status}
                  </p>
                  <p style={{ fontSize: 13, color: "#555", marginBottom: 4 }}>
                    {validations[index].message}
                  </p>
                  <p style={{ fontSize: 12, color: "#888" }}>
                    적용 수식: {validations[index].formula}
                  </p>
                  {validations[index].tip && (
                    <p style={{ fontSize: 12, color: "#2563eb", marginTop: 4 }}>
                      💡 {validations[index].tip}
                    </p>
                  )}
                </div>
              )}

              {/* 물리 검증 버튼 */}
              <button
                onClick={() => handleValidate(index, kpi)}
                disabled={validateLoading === index}
                style={{
                  padding: "8px 16px",
                  background: validateLoading === index ? "#ccc" : "#f3f4f6",
                  color: "#374151",
                  border: "1px solid #d1d5db",
                  borderRadius: 6,
                  fontSize: 13,
                  fontWeight: 500,
                  cursor: validateLoading === index ? "not-allowed" : "pointer",
                }}
              >
                {validateLoading === index ? "검증 중..." : "⚗️ 물리 검증하기"}
              </button>
            </div>
          ))}
        </>
      )}

      {/* 뒤로 가기 */}
      <button
        onClick={() => window.history.back()}
        style={{
          width: "100%",
          padding: "14px",
          background: "#f3f4f6",
          color: "#374151",
          border: "none",
          borderRadius: 8,
          fontSize: 16,
          fontWeight: 600,
          cursor: "pointer",
          marginTop: 8,
        }}
      >
        ← 뒤로 가기
      </button>
    </div>
  );
}

export default function KpiPage() {
  return (
    <Suspense fallback={<div style={{ textAlign: "center", marginTop: 60 }}>로딩 중...</div>}>
      <KpiContent />
    </Suspense>
  );
}