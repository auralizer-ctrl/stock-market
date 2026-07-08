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
            # yfinance에서 최근 2일 데이터 가져와 변동률 계산
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
    # 네이버 금융 해외 증시 뉴스 리스트
    url = "https://finance.naver.com/news/news_list.naver?mode=LSS3D&section_id=101&section_id2=258&section_id3=403"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    news_list = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        res.encoding = 'ms949'  # euc-kr의 확장인 ms949로 디코딩
        
        soup = BeautifulSoup(res.text, 'html.parser')
        subjects = soup.select('.articleSubject a, dd.articleSubject a')
        
        for idx, sub in enumerate(subjects):
            if idx >= 10:  # 상위 10개만 가져옴
                break
            title = sub.get_text(strip=True)
            # URL에 특수문자가 섞여서 깨지는 현상 방지
            link = "https://finance.naver.com" + sub['href']
            news_list.append({"title": title, "link": link})
    except Exception as e:
        print(f"Error crawling news: {e}")
        
    return news_list

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
