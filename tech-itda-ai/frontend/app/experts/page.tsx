"use client";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";

interface Expert {
  id: string;
  name: string;
  grade: string;
  fields: string;
  rating: number;
  location: string;
  career: string;
}

interface MatchResult {
  expert: Expert;
  match_score: number;
  reasons: string[];
}

function ExpertsContent() {
  const searchParams = useSearchParams();
  const company_id = searchParams.get("company_id");
  const [matches, setMatches] = useState<MatchResult[]>([]);
  const [companyName, setCompanyName] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!company_id) return;
    fetch(`http://localhost:8000/api/experts/match?company_id=${company_id}`, {
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setMatches(data.data);
          setCompanyName(data.company_name);
        }
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [company_id]);

  const getGradeBadge = (grade: string) => {
    if (grade === "넥서스인증") return { bg: "#dbeafe", color: "#1e40af", text: "🔵 넥서스 인증" };
    if (grade === "골드") return { bg: "#fef9c3", color: "#854d0e", text: "🟡 골드" };
    if (grade === "실버") return { bg: "#f3f4f6", color: "#374151", text: "⚪ 실버" };
    return { bg: "#f3f4f6", color: "#374151", text: grade };
  };

  if (loading) {
    return (
      <div style={{ maxWidth: 600, margin: "60px auto", padding: "0 24px", textAlign: "center" }}>
        <p style={{ fontSize: 18, color: "#666" }}>전문가를 매칭 중입니다...</p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 600, margin: "60px auto", padding: "0 24px" }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 8, color: "#111" }}>
        전문가 매칭
      </h1>
      <p style={{ color: "#666", marginBottom: 32 }}>
        <strong>{companyName}</strong> 에 가장 잘 맞는 전문가입니다
      </p>

      {matches.length === 0 ? (
        <div style={{ padding: 24, background: "#f5f5f5", borderRadius: 12, textAlign: "center" }}>
          <p style={{ color: "#666" }}>매칭되는 전문가가 없습니다.</p>
        </div>
      ) : (
        matches.map((match, index) => {
          const badge = getGradeBadge(match.expert.grade);
          return (
            <div
              key={match.expert.id}
              style={{
                background: "#ffffff",
                border: index === 0 ? "2px solid #2563eb" : "1px solid #e5e7eb",
                borderRadius: 12,
                padding: 24,
                marginBottom: 16,
                position: "relative",
              }}
            >
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

              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
                <div>
                  <h2 style={{ fontSize: 18, fontWeight: 700, margin: 0, color: "#111111" }}>
                    {match.expert.name}
                  </h2>
                  <div style={{ display: "flex", gap: 8, marginTop: 6 }}>
                    <span style={{
                      background: badge.bg,
                      color: badge.color,
                      fontSize: 12,
                      padding: "3px 10px",
                      borderRadius: 20,
                      fontWeight: 600,
                    }}>
                      {badge.text}
                    </span>
                    <span style={{
                      background: "#f3f4f6",
                      color: "#374151",
                      fontSize: 12,
                      padding: "3px 10px",
                      borderRadius: 20,
                    }}>
                      📍 {match.expert.location}
                    </span>
                  </div>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div style={{ fontSize: 20, fontWeight: 700, color: "#2563eb" }}>
                    {match.match_score}점
                  </div>
                  <div style={{ fontSize: 13, color: "#d97706" }}>
                    ⭐ {match.expert.rating}
                  </div>
                </div>
              </div>

              <div style={{ marginBottom: 12 }}>
                <p style={{ fontSize: 13, color: "#888", marginBottom: 6 }}>전문 분야</p>
                <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                  {match.expert.fields.split(",").map((field, i) => (
                    <span key={i} style={{
                      background: "#f3f4f6",
                      color: "#374151",
                      fontSize: 12,
                      padding: "3px 10px",
                      borderRadius: 20,
                    }}>
                      {field.trim()}
                    </span>
                  ))}
                </div>
              </div>

              <div style={{ marginBottom: 12 }}>
                <p style={{ fontSize: 13, color: "#888", marginBottom: 4 }}>경력</p>
                <p style={{ fontSize: 13, color: "#333333", lineHeight: 1.6, margin: 0 }}>
                  {match.expert.career}
                </p>
              </div>

              <div style={{ marginBottom: 16 }}>
                <p style={{ fontSize: 13, color: "#888", marginBottom: 6 }}>매칭 이유</p>
                <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                  {match.reasons.map((reason, i) => (
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

              <button
                onClick={() => alert(`${match.expert.name} 전문가에게 매칭 요청을 보냈습니다!\n담당자가 확인 후 연락드리겠습니다.`)}
                style={{
                  width: "100%",
                  padding: "10px",
                  background: "#2563eb",
                  color: "#ffffff",
                  border: "none",
                  borderRadius: 8,
                  fontSize: 14,
                  fontWeight: 600,
                  cursor: "pointer",
                }}
              >
                매칭 요청하기 →
              </button>
            </div>
          );
        })
      )}

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

export default function ExpertsPage() {
  return (
    <Suspense fallback={<div style={{ textAlign: "center", marginTop: 60 }}>로딩 중...</div>}>
      <ExpertsContent />
    </Suspense>
  );
}