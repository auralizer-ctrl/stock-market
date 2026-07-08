import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

import json

def generate_summary(indices, news):
    """
    수집된 지수 및 뉴스 데이터를 바탕으로 Gemini API를 통해 카카오톡용 요약 보고서와 국내 추천 종목을 작성합니다.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        return {
            "summary": "에러: GEMINI_API_KEY 환경변수가 설정되지 않았습니다.",
            "recommendations": []
        }
        
    genai.configure(api_key=gemini_key)
    
    # 텍스트 데이터 포맷팅
    indices_str = ""
    for name, data in indices.items():
        if data:
            sign = "+" if data['change'] > 0 else ""
            indices_str += f"- {name}: {data['price']} ({sign}{data['change']} / {sign}{data['percent']}%)\n"
        else:
            indices_str += f"- {name}: 데이터 수집 실패\n"
            
    news_str = ""
    for n in news:
        news_str += f"- {n['title']}\n"
        
    prompt = f"""
당신은 금융 시장 분석가이자 개인 주식 비서입니다.
아래에 제공된 [증시 지수 및 환율 현황]과 [오늘의 글로벌 금융 뉴스] 정보를 기반으로, 카카오톡 메시지로 받아볼 수 있는 **읽기 쉽고 유익한 아침 증시 브리핑**을 작성하고, 추가로 당일 수혜가 예상되는 국내 대표 종목을 추천해주세요.

[증시 지수 및 환율 현황]
{indices_str}

[오늘의 글로벌 금융 뉴스]
{news_str}

---

**작성 가이드라인:**
1. **메시지 제한**: 전체 글자 수는 카카오톡 텍스트 메시지 제한(약 1000자 이내)에 맞게 간결하고 직관적으로 작성해 주세요.
2. **이모지 활용**: 각 섹션마다 적절한 이모지를 사용하여 가독성을 높여주세요.
3. **어조**: 정중하면서도 친근한 어조(~입니다, ~세요)를 사용해 주세요.
4. **구성 항목**:
   - 📢 **오늘 아침 브리핑**: 오늘 날짜와 핵심 시황 요약 (1~2줄)
   - 📈 **주요 증시 현황**: 제공된 지수 데이터를 가독성 있게 정리 (이전 대비 변동 방향에 따라 변동률 옆에 🔴/🔵/⚪ 표시)
   - 📰 **주요 이슈 요약**: 뉴스들을 종합하여 세계 증시 동향의 핵심 줄기 2~3가지를 요약
   - 💡 **국내 시장 영향성**: 이러한 동향이 오늘 한국 증시(코스피/코스닥)에 미칠 영향이나 체크포인트 제안
   - 좋은 하루 되라는 마무리 인사
5. 뉴스 기사 제목의 단순 나열이 아닌, 전체적인 시장 맥락을 요약해주세요.

---

**국내 대표 종목 추천 가이드라인 (A안):**
- 오늘 글로벌 증시 흐름에 민감하게 반응할 것으로 예상되는 국내 대표 우량주/대형주 중에서 1~3개를 추천하십시오.
- 예: 미국 반도체 지수 상승 시 (삼성전자, SK하이닉스), 미국 친환경/테슬라 상승 시 (LG에너지솔루션, 삼성SDI), 인플레이션/유가 상승 시 정유주 등 대형주 위주 매핑.
- 각 추천 항목은 다음 필드를 가져야 합니다:
  - `name`: 종목명 (예: "삼성전자")
  - `ticker`: 6자리 종목 코드 (예: "005930")
  - `sector`: 업종/섹터 (예: "반도체")
  - `reason`: 추천 사유 (글로벌 증시 및 지수, 뉴스와 어떻게 연계되는지 구체적으로 기술)
  - `action_plan`: 오늘 하루의 구체적인 투자 대응 전략 및 체크포인트 (예: "시초가 급등 시 추격 매수 자제, 분할 매수 대응")

---

**출력 형식 (MUST BE JSON):**
반드시 다음 구조의 JSON 객체로만 응답하십시오. 다른 텍스트는 포함하지 마십시오.

{{
  "summary": "카카오톡 증시 브리핑 마크다운 텍스트 (위 작성 가이드라인에 맞춘 내용)",
  "recommendations": [
    {{
      "name": "종목명",
      "ticker": "종목코드(6자리)",
      "sector": "업종",
      "reason": "추천 사유",
      "action_plan": "대응 전략"
    }}
  ]
}}
"""
    try:
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )
        response = model.generate_content(prompt)
        # JSON 파싱하여 반환
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating summary: {e}")
        return {
            "summary": f"Gemini API 요약 중 오류 발생: {e}",
            "recommendations": []
        }

if __name__ == "__main__":
    # 테스트용 모의 데이터
    test_indices = {
        "S&P 500": {"price": 5300.0, "change": 25.0, "percent": 0.47},
        "Nasdaq": {"price": 16500.0, "change": -10.0, "percent": -0.06},
        "Dow Jones": {"price": 39000.0, "change": 120.0, "percent": 0.31},
        "KOSPI": {"price": 2700.0, "change": 5.0, "percent": 0.18},
        "KOSDAQ": {"price": 850.0, "change": -2.0, "percent": -0.23},
        "USD/KRW": {"price": 1360.0, "change": -3.5, "percent": -0.26}
    }
    test_news = [
        {"title": "뉴욕증시, Fed 금리인하 기대 확산에 S&P500·다우 상승...나스닥은 소폭 하락", "link": ""},
        {"title": "달러화 약세 속 원/달러 환율 하락 출발 전망", "link": ""},
        {"title": "엔비디아 주가 주춤했으나 반도체 섹터 전반은 견조", "link": ""}
    ]
    
    print(generate_summary(test_indices, test_news))
