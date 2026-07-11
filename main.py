import os
import sys
import json
import datetime
from dotenv import load_dotenv
import collector
import summarizer

# UTF-8 출력 설정 (Windows 환경 대응)
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

load_dotenv()

def main():
    print("=================== 증시 알림 프로그램 시작 ===================")
    
    # 1. 환경 변수 검증
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("[오류] .env 파일의 GEMINI_API_KEY 설정을 확인해주세요.")
        sys.exit(1)
        
    # 2. 데이터 수집
    print("\n[1/3] 증시 데이터 및 뉴스 수집 중...")
    indices = collector.get_market_indices()
    news = collector.get_global_news()
    
    print("유튜브 최신 동영상 피드 수집 중...")
    youtube_videos = collector.get_latest_youtube_videos()
    
    if not indices and not news:
        print("[오류] 수집된 데이터가 없습니다. 중단합니다.")
        sys.exit(1)
        
    # 3. Gemini 요약 생성
    print("[2/3] Gemini AI 요약 생성 중...")
    result = summarizer.generate_summary(indices, news)
    
    # 4. JSON 파일 저장 (React public 폴더 타겟)
    print("[3/3] 웹앱용 JSON 데이터 저장 중...")
    
    # 한국 표준시(KST = UTC+9) 기준 현재 시각 (GitHub Actions 서버는 UTC 사용)
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_kst = now_utc + datetime.timedelta(hours=9)
    now = now_kst.strftime("%Y-%m-%d %H:%M:%S")
    
    output_data = {
        "updated_at": now,
        "indices": indices,
        "news": news,
        "youtube": youtube_videos,
        "summary": result.get("summary", ""),
        "recommendations": result.get("recommendations", [])
    }
    
    public_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
    if not os.path.exists(public_dir):
        os.makedirs(public_dir)
        
    json_path = os.path.join(public_dir, "data.json")
    
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"📢 JSON 데이터가 성공적으로 저장되었습니다: {json_path}")
    except Exception as e:
        print(f"❌ JSON 데이터 저장 실패: {e}")
        sys.exit(1)
        
    print("=================== 증시 알림 프로그램 종료 ===================")

if __name__ == "__main__":
    main()
