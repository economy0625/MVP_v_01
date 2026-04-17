"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function OnboardingPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    name: "",
    industry: "",
    company_stage: "",
    tech_level: 1,
    location: "",
    certs: "",
  });

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch("https://mvpv01-production.up.railway.app/api/companies/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          tech_level: Number(form.tech_level),
        }),
      });
      const data = await res.json();
      if (data.success) {
        alert("기업 정보가 저장되었습니다!");
        router.push(`/recommend?company_id=${data.data.id}`);
      }
    } catch (e) {
      alert("오류가 발생했습니다. 백엔드 서버를 확인해주세요.");
    }
    setLoading(false);
  };

  const selectStyle = {
    width: "100%",
    padding: "10px 12px",
    border: "1px solid #ddd",
    borderRadius: 8,
    fontSize: 14,
    color: "#000",
    background: "#fff",
  };

  const inputStyle = {
    width: "100%",
    padding: "10px 12px",
    border: "1px solid #ddd",
    borderRadius: 8,
    fontSize: 14,
    color: "#000",
    background: "#fff",
  };

  const labelStyle = {
    display: "block",
    marginBottom: 6,
    fontWeight: 500,
  };

  return (
    <div style={{ maxWidth: 480, margin: "60px auto", padding: "0 24px" }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 8 }}>
        테크잇다AI
      </h1>
      <p style={{ color: "#666", marginBottom: 32 }}>
        기업 정보를 입력하면 맞춤 지원사업을 추천해드립니다
      </p>

      <div style={{ marginBottom: 20 }}>
        <label style={labelStyle}>기업명 *</label>
        <input
          type="text"
          placeholder="예: 테크잇다 주식회사"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          style={inputStyle}
        />
      </div>

      <div style={{ marginBottom: 20 }}>
        <label style={labelStyle}>업종 *</label>
        <select
          value={form.industry}
          onChange={(e) => setForm({ ...form, industry: e.target.value })}
          style={selectStyle}
        >
          <option value="">선택해주세요</option>
          <option value="제조업">제조업</option>
          <option value="소재부품">소재부품</option>
          <option value="자동차부품">자동차부품</option>
          <option value="전자전기">전자전기</option>
          <option value="화학">화학</option>
          <option value="바이오">바이오</option>
          <option value="ICT">ICT</option>
          <option value="기타">기타</option>
        </select>
      </div>

      <div style={{ marginBottom: 20 }}>
        <label style={labelStyle}>기업 단계 *</label>
        <select
          value={form.company_stage}
          onChange={(e) => setForm({ ...form, company_stage: e.target.value })}
          style={selectStyle}
        >
          <option value="">선택해주세요</option>
          <option value="예비창업">예비창업 (아직 창업 전)</option>
          <option value="초기">초기 (창업 3년 이하)</option>
          <option value="성장">성장 (창업 3년 이상)</option>
        </select>
      </div>

      <div style={{ marginBottom: 20 }}>
        <label style={labelStyle}>기술 수준 (TRL) *</label>
        <select
          value={form.tech_level}
          onChange={(e) => setForm({ ...form, tech_level: Number(e.target.value) })}
          style={selectStyle}
        >
          <option value={1}>TRL 1~2 — 아이디어/기초 연구 단계</option>
          <option value={3}>TRL 3~4 — 개념 검증 단계</option>
          <option value={5}>TRL 5~6 — 시제품 개발 단계</option>
          <option value={7}>TRL 7~8 — 실증/검증 단계</option>
          <option value={9}>TRL 9 — 양산/사업화 단계</option>
        </select>
      </div>

      <div style={{ marginBottom: 20 }}>
        <label style={labelStyle}>지역 *</label>
        <select
          value={form.location}
          onChange={(e) => setForm({ ...form, location: e.target.value })}
          style={selectStyle}
        >
          <option value="">선택해주세요</option>
          <option value="대구">대구</option>
          <option value="서울">서울</option>
          <option value="경기">경기</option>
          <option value="부산">부산</option>
          <option value="경북">경북</option>
          <option value="기타">기타</option>
        </select>
      </div>

      <div style={{ marginBottom: 32 }}>
        <label style={labelStyle}>보유 인증 (선택)</label>
        <select
          value={form.certs}
          onChange={(e) => setForm({ ...form, certs: e.target.value })}
          style={selectStyle}
        >
          <option value="">없음</option>
          <option value="벤처">벤처기업</option>
          <option value="이노비즈">이노비즈</option>
          <option value="ISO">ISO</option>
          <option value="벤처,이노비즈">벤처 + 이노비즈</option>
        </select>
      </div>

      <button
        onClick={handleSubmit}
        disabled={
          loading ||
          !form.name ||
          !form.industry ||
          !form.company_stage ||
          !form.location
        }
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
        }}
      >
        {loading ? "저장 중..." : "맞춤 지원사업 추천받기 →"}
      </button>
    </div>
  );
}