"use client";
import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";

interface Section {
  title: string;
  content: string;
}

interface Program {
  id: string;
  name: string;
  agency: string;
}

function PlanContent() {
  const searchParams = useSearchParams();
  const company_id = searchParams.get("company_id");
  const [programs, setPrograms] = useState<Program[]>([]);
  const [selectedProgram, setSelectedProgram] = useState("");
  const [techGoal, setTechGoal] = useState("");
  const [kpiInput, setKpiInput] = useState("");
  const [sections, setSections] = useState<Section[]>([]);
  const [companyName, setCompanyName] = useState("");
  const [programName, setProgramName] = useState("");
  const [loading, setLoading] = useState(false);

  // 지원사업 목록 불러오기
  useEffect(() => {
    fetch("https://mvpv01-production.up.railway.app/api/programs/")
      .then((res) => res.json())
      .then((data) => {
        if (data.success) setPrograms(data.data);
      });
  }, []);

  // 계획서 생성
  const handleGenerate = async () => {
    if (!selectedProgram || !techGoal.trim()) {
      alert("지원사업과 기술 목표를 입력해주세요.");
      return;
    }
    setLoading(true);
    setSections([]);

    const kpis = kpiInput
      .split("\n")
      .map((k) => k.trim())
      .filter((k) => k.length > 0);

    try {
      const res = await fetch("https://mvpv01-production.up.railway.app/api/plan/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          company_id: company_id,
          program_id: selectedProgram,
          tech_goal: techGoal,
          kpis: kpis,
        }),
      });
      const data = await res.json();
      if (data.success && data.data.sections) {
        setSections(data.data.sections);
        setCompanyName(data.company_name);
        setProgramName(data.program_name);
      } else {
        alert("계획서 생성 중 오류가 발생했습니다.");
      }
    } catch (e) {
      alert("오류가 발생했습니다. 백엔드 서버를 확인해주세요.");
    }
    setLoading(false);
  };

  // 전체 텍스트 복사
  const handleCopy = () => {
    const text = sections
      .map((s) => `${s.title}\n\n${s.content}`)
      .join("\n\n---\n\n");
    navigator.clipboard.writeText(text);
    alert("계획서가 클립보드에 복사되었습니다!");
  };

  return (
    <div style={{ maxWidth: 700, margin: "60px auto", padding: "0 24px" }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 8 }}>
        사업계획서 초안 생성
      </h1>
      <p style={{ color: "#666", marginBottom: 32 }}>
        기업 정보와 기술 목표를 바탕으로 AI가 계획서 초안을 자동 작성합니다
      </p>

      {/* 지원사업 선택 */}
      <div style={{ marginBottom: 20 }}>
        <label style={{ display: "block", marginBottom: 6, fontWeight: 500 }}>
          지원사업 선택 *
        </label>
        <select
          value={selectedProgram}
          onChange={(e) => setSelectedProgram(e.target.value)}
          style={{
            width: "100%",
            padding: "10px 12px",
            border: "1px solid #ddd",
            borderRadius: 8,
            fontSize: 14,
            color: "#000",
            background: "#fff",
          }}
        >
          <option value="">선택해주세요</option>
          {programs.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name} ({p.agency})
            </option>
          ))}
        </select>
      </div>

      {/* 기술 목표 */}
      <div style={{ marginBottom: 20 }}>
        <label style={{ display: "block", marginBottom: 6, fontWeight: 500 }}>
          기술 목표 *
        </label>
        <input
          type="text"
          placeholder="예: 경량화 소재 개발을 통한 제품 경쟁력 강화"
          value={techGoal}
          onChange={(e) => setTechGoal(e.target.value)}
          style={{
            width: "100%",
            padding: "10px 12px",
            border: "1px solid #ddd",
            borderRadius: 8,
            fontSize: 14,
            color: "#000",
            background: "#fff",
          }}
        />
      </div>

      {/* KPI 입력 */}
      <div style={{ marginBottom: 24 }}>
        <label style={{ display: "block", marginBottom: 6, fontWeight: 500 }}>
          KPI 목록 (선택 — 줄바꿈으로 구분)
        </label>
        <textarea
          placeholder={"불량률 5% 이하 달성 (24개월)\n생산성 30% 향상 (18개월)\n에너지 효율 20% 향상 (20개월)"}
          value={kpiInput}
          onChange={(e) => setKpiInput(e.target.value)}
          rows={4}
          style={{
            width: "100%",
            padding: "10px 12px",
            border: "1px solid #ddd",
            borderRadius: 8,
            fontSize: 14,
            color: "#000",
            background: "#fff",
            resize: "vertical",
          }}
        />
      </div>

      {/* 생성 버튼 */}
      <button
        onClick={handleGenerate}
        disabled={loading || !selectedProgram || !techGoal.trim()}
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
        {loading ? "AI가 계획서를 작성 중입니다... (약 10~20초)" : "사업계획서 초안 생성 →"}
      </button>

      {/* 계획서 결과 */}
      {sections.length > 0 && (
        <>
          <div style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: 16,
          }}>
            <div>
              <h2 style={{ fontSize: 18, fontWeight: 600, margin: 0 }}>
                {programName} 계획서 초안
              </h2>
              <p style={{ fontSize: 13, color: "#888", margin: "4px 0 0" }}>
                {companyName} | ⚠️ 이 문서는 AI 초안입니다. 반드시 검토 후 사용하세요.
              </p>
            </div>
            <button
              onClick={handleCopy}
              style={{
                padding: "8px 16px",
                background: "#f3f4f6",
                color: "#374151",
                border: "1px solid #d1d5db",
                borderRadius: 6,
                fontSize: 13,
                fontWeight: 500,
                cursor: "pointer",
                whiteSpace: "nowrap",
              }}
            >
              📋 전체 복사
            </button>
          </div>

          {sections.map((section, index) => (
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
              <h3 style={{
                fontSize: 15,
                fontWeight: 600,
                color: "#2563eb",
                marginBottom: 12,
                paddingBottom: 8,
                borderBottom: "1px solid #e5e7eb",
              }}>
                {section.title}
              </h3>
              <p style={{
                fontSize: 14,
                color: "#333",
                lineHeight: 1.8,
                margin: 0,
                whiteSpace: "pre-wrap",
              }}>
                {section.content}
              </p>
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

export default function PlanPage() {
  return (
    <Suspense fallback={<div style={{ textAlign: "center", marginTop: 60 }}>로딩 중...</div>}>
      <PlanContent />
    </Suspense>
  );
}