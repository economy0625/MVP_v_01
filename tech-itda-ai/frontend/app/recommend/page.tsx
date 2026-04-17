"use client";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";

interface Program {
  id: string;
  name: string;
  agency: string;
  category: string;
  budget_min: number;
  budget_max: number;
  deadline: string;
  region: string;
}

interface Recommendation {
  program: Program;
  match_score: number;
  reasons: string[];
}

function RecommendContent() {
  const searchParams = useSearchParams();
  const company_id = searchParams.get("company_id");
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [companyName, setCompanyName] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!company_id) return;

    fetch(`http://localhost:8000/api/recommend/?company_id=${company_id}`, {
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setRecommendations(data.data);
          setCompanyName(data.company_name);
        }
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [company_id]);

  if (loading) {
    return (
      <div style={{ maxWidth: 600, margin: "60px auto", padding: "0 24px", textAlign: "center" }}>
        <p style={{ fontSize: 18, color: "#666" }}>추천 사업을 분석 중입니다...</p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 600, margin: "60px auto", padding: "0 24px" }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 8 }}>
        맞춤 지원사업 추천
      </h1>
      <p style={{ color: "#666", marginBottom: 32 }}>
        <strong>{companyName}</strong> 에 가장 잘 맞는 사업입니다
      </p>

      {recommendations.length === 0 ? (
        <div style={{ padding: 24, background: "#f5f5f5", borderRadius: 12, textAlign: "center" }}>
          <p style={{ color: "#666" }}>조건에 맞는 지원사업이 없습니다.</p>
          <p style={{ color: "#666", fontSize: 14 }}>기업 정보를 다시 확인해주세요.</p>
        </div>
      ) : (
        recommendations.map((rec, index) => (
          <div
            key={rec.program.id}
            style={{
              background: "#fff",
              border: index === 0 ? "2px solid #2563eb" : "1px solid #e5e7eb",
              borderRadius: 12,
              padding: 24,
              marginBottom: 16,
              position: "relative",
            }}
          >
            {/* 1위 배지 */}
            {index === 0 && (
              <span style={{
                position: "absolute",
                top: -12,
                left: 20,
                background: "#2563eb",
                color: "#fff",
                fontSize: 12,
                fontWeight: 600,
                padding: "3px 10px",
                borderRadius: 20,
              }}>
                🏆 최우선 추천
              </span>
            )}

            {/* 매칭 점수 */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
              <h2 style={{ fontSize: 18, fontWeight: 600, margin: 0 }}>
                {rec.program.name}
              </h2>
              <span style={{
                background: rec.match_score >= 70 ? "#dcfce7" : "#fef9c3",
                color: rec.match_score >= 70 ? "#166534" : "#854d0e",
                fontSize: 14,
                fontWeight: 600,
                padding: "4px 12px",
                borderRadius: 20,
              }}>
                매칭 {rec.match_score}점
              </span>
            </div>

            {/* 기본 정보 */}
            <div style={{ fontSize: 14, color: "#666", marginBottom: 12 }}>
              <span style={{ marginRight: 16 }}>🏢 {rec.program.agency}</span>
              <span style={{ marginRight: 16 }}>📁 {rec.program.category}</span>
              <span>📍 {rec.program.region}</span>
            </div>

            {/* 지원금 */}
            <div style={{ fontSize: 14, color: "#333", marginBottom: 12 }}>
              💰 지원금: {rec.program.budget_min?.toLocaleString()}만원
              ~ {rec.program.budget_max?.toLocaleString()}만원
            </div>

            {/* 마감일 */}
            <div style={{ fontSize: 14, color: "#e74c3c", marginBottom: 16 }}>
              ⏰ 마감일: {rec.program.deadline}
            </div>

            {/* 추천 이유 */}
            <div>
              <p style={{ fontSize: 13, color: "#888", marginBottom: 6 }}>추천 이유</p>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                {rec.reasons.map((reason, i) => (
                  <span key={i} style={{
                    background: "#eff6ff",
                    color: "#1d4ed8",
                    fontSize: 12,
                    padding: "3px 10px",
                    borderRadius: 20,
                  }}>
                    ✓ {reason}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))
      )}

      {/* 다시 입력하기 버튼 */}
      <button
        onClick={() => window.location.href = "/onboarding"}
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
        ← 기업 정보 다시 입력하기
      </button>
    </div>
  );
}

export default function RecommendPage() {
  return (
    <Suspense fallback={<div style={{ textAlign: "center", marginTop: 60 }}>로딩 중...</div>}>
      <RecommendContent />
    </Suspense>
  );
}