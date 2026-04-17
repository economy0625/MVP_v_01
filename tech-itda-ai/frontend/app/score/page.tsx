"use client";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";

interface ScoreData {
  total_score: number;
  probability: number;
  breakdown: { [key: string]: number };
  deductions: string[];
  feedback: string[];
}

function ScoreContent() {
  const searchParams = useSearchParams();
  const company_id = searchParams.get("company_id");
  const [scoreData, setScoreData] = useState<ScoreData | null>(null);
  const [companyName, setCompanyName] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!company_id) return;

    fetch(`http://localhost:8000/api/score/?company_id=${company_id}`, {
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setScoreData(data.data);
          setCompanyName(data.company_name);
        }
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [company_id]);

  if (loading) {
    return (
      <div style={{ maxWidth: 600, margin: "60px auto", padding: "0 24px", textAlign: "center" }}>
        <p style={{ fontSize: 18, color: "#666" }}>점수를 계산 중입니다...</p>
      </div>
    );
  }

  if (!scoreData) {
    return (
      <div style={{ maxWidth: 600, margin: "60px auto", padding: "0 24px", textAlign: "center" }}>
        <p style={{ color: "#666" }}>데이터를 불러올 수 없습니다.</p>
      </div>
    );
  }

  const probabilityColor =
    scoreData.probability >= 70 ? "#16a34a" :
    scoreData.probability >= 50 ? "#d97706" : "#dc2626";

  return (
    <div style={{ maxWidth: 600, margin: "60px auto", padding: "0 24px" }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 8 }}>
        선정 확률 분석
      </h1>
      <p style={{ color: "#666", marginBottom: 32 }}>
        <strong>{companyName}</strong> 의 현재 선정 가능성입니다
      </p>

      {/* 확률 게이지 */}
      <div style={{
        background: "#fff",
        border: "1px solid #e5e7eb",
        borderRadius: 16,
        padding: 32,
        marginBottom: 24,
        textAlign: "center",
      }}>
        <p style={{ fontSize: 14, color: "#666", marginBottom: 8 }}>예상 선정 확률</p>
        <p style={{ fontSize: 64, fontWeight: 700, color: probabilityColor, margin: 0 }}>
          {scoreData.probability}%
        </p>
        <p style={{ fontSize: 16, color: "#333", marginTop: 8 }}>
          총점 {scoreData.total_score}점 / 100점
        </p>

        {/* 게이지 바 */}
        <div style={{
          background: "#f3f4f6",
          borderRadius: 99,
          height: 12,
          marginTop: 16,
          overflow: "hidden",
        }}>
          <div style={{
            background: probabilityColor,
            width: `${scoreData.probability}%`,
            height: "100%",
            borderRadius: 99,
            transition: "width 1s ease",
          }} />
        </div>

        <p style={{ fontSize: 13, color: "#888", marginTop: 12 }}>
          {scoreData.probability >= 70 ? "✅ 선정 가능성이 높습니다" :
           scoreData.probability >= 50 ? "⚠️ 보완이 필요합니다" :
           "❌ 준비가 더 필요합니다"}
        </p>
      </div>

      {/* 항목별 점수 */}
      <div style={{
        background: "#fff",
        border: "1px solid #e5e7eb",
        borderRadius: 16,
        padding: 24,
        marginBottom: 24,
      }}>
        <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 16 }}>항목별 점수</h2>
        {Object.entries(scoreData.breakdown).map(([key, value]) => (
          <div key={key} style={{ marginBottom: 14 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
              <span style={{ fontSize: 14, color: "#333" }}>{key}</span>
              <span style={{ fontSize: 14, fontWeight: 600, color: "#333" }}>{value} / 20점</span>
            </div>
            <div style={{ background: "#f3f4f6", borderRadius: 99, height: 8, overflow: "hidden" }}>
              <div style={{
                background: value >= 16 ? "#16a34a" : value >= 10 ? "#d97706" : "#dc2626",
                width: `${(value / 20) * 100}%`,
                height: "100%",
                borderRadius: 99,
              }} />
            </div>
          </div>
        ))}
      </div>

      {/* 감점 요소 */}
      {scoreData.deductions.length > 0 && (
        <div style={{
          background: "#fef2f2",
          border: "1px solid #fecaca",
          borderRadius: 12,
          padding: 20,
          marginBottom: 24,
        }}>
          <h2 style={{ fontSize: 16, fontWeight: 600, color: "#dc2626", marginBottom: 12 }}>
            ❌ 감점 요소
          </h2>
          {scoreData.deductions.map((d, i) => (
            <p key={i} style={{ fontSize: 14, color: "#dc2626", margin: "4px 0" }}>• {d}</p>
          ))}
        </div>
      )}

      {/* 개선 제안 */}
      {scoreData.feedback.length > 0 && (
        <div style={{
          background: "#eff6ff",
          border: "1px solid #bfdbfe",
          borderRadius: 12,
          padding: 20,
          marginBottom: 24,
        }}>
          <h2 style={{ fontSize: 16, fontWeight: 600, color: "#1d4ed8", marginBottom: 12 }}>
            💡 개선 제안
          </h2>
          {scoreData.feedback.map((f, i) => (
            <p key={i} style={{ fontSize: 14, color: "#1d4ed8", margin: "4px 0" }}>• {f}</p>
          ))}
        </div>
      )}

      {/* 버튼 */}
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
        }}
      >
        ← 추천 결과로 돌아가기
      </button>
    </div>
  );
}

export default function ScorePage() {
  return (
    <Suspense fallback={<div style={{ textAlign: "center", marginTop: 60 }}>로딩 중...</div>}>
      <ScoreContent />
    </Suspense>
  );
}