import yfinance as yf
import requests
from bs4 import BeautifulSoup
import datetime

def get_market_indices():
    """
    yfinance를 이용해 미국/한국 주요 지수 및 환율을 수집합니다.
    """
    tickers = {
        "S&P 500": "^GSPC",
        "Nasdaq": "^IXIC",
        "Dow Jones": "^DJI",
        "KOSPI": "^KS11",
        "KOSDAQ": "^KQ11",
        "USD/KRW": "USDKRW=X"
    }
    
    results = {}
    for name, ticker in tickers.items():
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="2d")
            if len(hist) >= 2:
                prev_close = float(hist['Close'].iloc[-2])
                curr_close = float(hist['Close'].iloc[-1])
                change = curr_close - prev_close
                change_percent = (change / prev_close) * 100
                results[name] = {
                    "price": round(curr_close, 2),
                    "change": round(change, 2),
                    "percent": round(change_percent, 2)
                }
            elif len(hist) == 1:
                curr_close = float(hist['Close'].iloc[-1])
                results[name] = {
                    "price": round(curr_close, 2),
                    "change": 0.0,
                    "percent": 0.0
                }
        except Exception as e:
            print(f"Error fetching {name} ({ticker}): {e}")
            results[name] = None
            
    return results

def get_global_news():
    """
    네이버 금융 해외증시 뉴스 섹션에서 헤드라인을 크롤링합니다.
    """
    url = "https://finance.naver.com/news/news_list.naver?mode=LSS3D&section_id=101&section_id2=258&section_id3=403"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    news_list = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        res.encoding = 'ms949'
        
        soup = BeautifulSoup(res.text, 'html.parser')
        subjects = soup.select('.articleSubject a, dd.articleSubject a')
        
        for idx, sub in enumerate(subjects):
            if idx >= 10:
                break
            title = sub.get_text(strip=True)
            link = "https://finance.naver.com" + sub['href']
            news_list.append({"title": title, "link": link})
    except Exception as e:
        print(f"Error crawling news: {e}")
        
    return news_list

def get_latest_youtube_videos():
    """
    추천 금융 유튜브 채널의 비디오 탭 HTML을 조회하여 가장 최근 업로드된 비디오 ID를 정규식으로 안전하게 추출합니다.
    """
    channels = [
        {
            "id": "ytn",
            "name": "YTN 실시간 경제 뉴스",
            "desc": "24시간 생방송 경제/시황 속보 라이브 방송",
            "logo": "📰",
            "handle": "@ytnnews"
        },
        {
            "id": "sampro",
            "name": "삼프로TV",
            "desc": "실시간 국내외 금융 시황 & 라이브 경제 뉴스",
            "logo": "🎙️",
            "handle": "@3protv"
        },
        {
            "id": "syuka",
            "name": "슈카월드",
            "desc": "경제 시사 이슈를 쉽고 재밌게 요약 분석",
            "logo": "🦁",
            "handle": "@syukaworld"
        },
        {
            "id": "hong",
            "name": "홍춘욱의 쉬운 경제",
            "desc": "이코노미스트의 시장 분석 및 투자 경제학",
            "logo": "📈",
            "handle": "@chunukhong"
        }
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    import re
    results = []
    
    for ch in channels:
        url = f"https://www.youtube.com/{ch['handle']}/videos"
        embed_url = ""
        origin_url = ""
        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            
            # HTML 내용에서 videoId 매칭
            video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', res.text)
            if video_ids:
                # 중복 제거 및 첫 번째 아이템이 가장 최신 비디오
                unique_ids = []
                for vid in video_ids:
                    if vid not in unique_ids:
                        unique_ids.append(vid)
                video_id = unique_ids[0]
                embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1"
                origin_url = f"https://www.youtube.com/watch?v={video_id}"
            else:
                raise Exception("HTML에서 videoId 매칭 결과 없음")
                
        except Exception as e:
            print(f"Error scraping YouTube HTML for {ch['name']}: {e}")
            # 크롤링 에러 시 고정 안전 폴백 주소 매핑
            if ch['id'] == 'ytn':
                embed_url = "https://www.youtube.com/embed/goTpDq2GKy4?autoplay=1&mute=1"
                origin_url = "https://www.youtube.com/watch?v=goTpDq2GKy4"
            elif ch['id'] == 'sampro':
                embed_url = "https://www.youtube.com/embed/live_stream?channel=UC7R22eOqN9hWd7zB67482_g"
                origin_url = "https://www.youtube.com/@samprotv/live"
            elif ch['id'] == 'syuka':
                embed_url = "https://www.youtube.com/embed/videoseries?list=PL_JbQp6wQc_t7wVj8jD87D9aI_B4H0vU9"
                origin_url = "https://www.youtube.com/@syukaworld"
            else:
                embed_url = "https://www.youtube.com/embed/videoseries?list=PL9XzO49l7bM1pD38vHkM3kHhN5O3nJ62o"
                origin_url = "https://www.youtube.com/@DrHong-economy"
                
        results.append({
            "id": ch['id'],
            "name": ch['name'],
            "desc": ch['desc'],
            "logo": ch['logo'],
            "embedUrl": embed_url,
            "originUrl": origin_url
        })
        
    return results

if __name__ == "__main__":
    import sys
    import io
    if sys.platform.startswith('win'):
        sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

    print("Market Indices:")
    indices = get_market_indices()
    for k, v in indices.items():
        print(f"{k}: {v}")
    
    print("\nGlobal News:")
    news = get_global_news()
    for n in news:
        print(f"- {n['title']} ({n['link']})")
        
    print("\nYouTube RSS Video Feeds:")
    videos = get_latest_youtube_videos()
    for v in videos:
        print(f"- {v['name']}: {v['embedUrl']} (Origin: {v['originUrl']})")
