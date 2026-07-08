import os
import google.generativeai as genai
from dotenv import load_dotenv
import datetime
import json

load_dotenv()

def generate_summary(indices, news):
    """
    수집된 지수 및 뉴스 데이터를 바탕으로 Gemini API를 통해 아침 증시 브리핑을 오늘 날짜 기준으로 작성합니다.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        return {
            "summary": "에러: GEMINI_API_KEY 환경변수가 설정되지 않았습니다.",
            "recommendations": []
        }
        
    genai.configure(api_key=gemini_key)
    
    # 1. 한국 표준시(KST) 날짜 계산 (GitHub Actions 서버 표준시 극복)
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_kst = now_utc + datetime.timedelta(hours=9)
    today_str = now_kst.strftime("%Y년 %m월 %d일")
    
    # 2. 텍스트 데이터 포맷팅
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
아래에 제공된 [오늘의 날짜], [증시 지수 및 환율 현황]과 [오늘의 글로벌 금융 뉴스] 정보를 기반으로, 대시보드 웹앱에서 받아볼 수 있는 **읽기 쉽고 유익한 아침 증시 브리핑**을 작성하고, 추가로 당일 수혜가 예상되는 국내 대표 종목을 추천해주세요.

[오늘 날짜 (기준일자)]
{today_str}

[증시 지수 및 환율 현황]
{indices_str}

[오늘의 글로벌 금융 뉴스]
{news_str}

---

**작성 가이드라인:**
1. **메시지 제한**: 전체 글자 수는 카카오톡 및 모바일 가독성을 높이기 위해 컴팩트하게(약 1000자 이내) 작성해 주세요.
2. **이모지 활용**: 각 섹션마다 적절한 이모지를 사용하여 가독성을 높여주세요.
3. **어조**: 정중하면서도 친근한 어조(~입니다, ~세요)를 사용해 주세요.
4. **구성 항목**:
   - 📢 **오늘 아침 브리핑**: 제공된 오늘 날짜({today_str})를 명시하며 핵심 시황 요약 (1~2줄)
   - 📈 **주요 증시 현황**: 제공된 지수 데이터를 가독성 있게 정리 (이전 대비 변동 방향에 따라 변동률 옆에 🔴/🔵/⚪ 표시)
   - 📰 **주요 이슈 요약**: 뉴스들을 종합하여 세계 증시 동향의 핵심 줄기 2~3가지를 요약
   - 💡 **국내 시장 영향성**: 이러한 동향이 오늘 한국 증시(코스피/코스닥)에 미칠 영향이나 체크포인트 제안
   - 좋은 하루 되라는 마무리 인사
5. 뉴스 기사 제목의 단순 나열이 아닌, 전체적인 시장 맥락을 요약해주세요.

---

**국내 대표 종목 추천 가이드라인:**
- 오늘 글로벌 증시 흐름에 민감하게 반응할 것으로 예상되는 국내 대표 우량주/대형주 중에서 1~3개를 추천하십시오.
- 예: 미국 반도체 지수 상승 시 (삼성전자, SK하이닉스), 미국 친환경/테슬라 상승 시 (LG에너지솔루션, 삼성SDI), 인플레이션/유가 상승 시 정유주 등 대형주 위주 매핑.
- 각 추천 항목은 다음 필드를 가져야 합니다:
  - `name`: 종목명 (예: "삼성전자")
  - `ticker`: 6자리 종목 코드 (예: "005930")
  - `sector`: 업종/섹터 (예: "반도체")
  - `reason`: 추천 사유 (글로벌 증시 및 지수, 뉴스와 어떻게 연계되는지 구체적으로 기술)
  - `action_plan`: 오늘 하루의 구체적인 투자 대응 전략 및 체크포인트 (예: "시초가 급등 시 추격 매수 자제, 분할 매수 대응")
  - `related_stocks`: 해당 추천 종목과 밀접한 연관이 있거나 같은 섹터/테마에 속해 함께 움직일 가능성이 높은 국내 관련 종목 리스트 (최대 2~3개 추천, 각각 `name`(종목명)과 `ticker`(6자리 종목코드)를 포함해야 함. 예: 삼성전자 추천 시 `[ {{"name": "SK하이닉스", "ticker": "000660"}}, {{"name": "한미반도체", "ticker": "042700"}} ]`)

---

**출력 형식 (MUST BE JSON):**
반드시 다음 구조의 JSON 객체로만 응답하십시오. 다른 텍스트는 포함하지 마십시오.

{{
  "summary": "마크다운 기호가 약간 가미된 증시 브리핑 텍스트 (반드시 {today_str}가 명시되어야 함)",
  "recommendations": [
    {{
      "name": "종목명",
      "ticker": "종목코드(6자리)",
      "sector": "업종",
      "reason": "추천 사유",
      "action_plan": "대응 전략",
      "related_stocks": [
        {{
          "name": "관련종목명",
          "ticker": "관련종목코드(6자리)"
        }}
      ]
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
