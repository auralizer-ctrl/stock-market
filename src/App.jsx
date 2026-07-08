import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { 
  TrendingUp, 
  TrendingDown, 
  Minus,
  Clock, 
  Newspaper, 
  Sparkles,
  RefreshCw,
  LineChart,
  ChevronRight,
  Info,
  Play
} from 'lucide-react';

const YOUTUBE_CHANNELS = [
  {
    id: 'sampro',
    name: '삼프로TV',
    desc: '실시간 국내외 금융 시황 & 라이브 뉴스',
    logo: '🎙️',
    // 삼프로TV 채널 ID 기반 라이브 스트림 연동
    embedUrl: 'https://www.youtube.com/embed/live_stream?channel=UC8GD-S95Qc5-m_AEXW4WvAg'
  },
  {
    id: 'syuka',
    name: '슈카월드',
    desc: '경제 시사 이슈를 쉽고 재밌게 요약 분석',
    logo: '🦁',
    // 슈카월드 업로드 비디오 재생목록 연동
    embedUrl: 'https://www.youtube.com/embed/videoseries?list=PL_JbQp6wQc_t7wVj8jD87D9aI_B4H0vU9'
  },
  {
    id: 'saimdang',
    name: '경제전파사',
    desc: '글로벌 경제 리포트 및 트렌드 인사이트',
    logo: '🔔',
    // 경제전파사 경제 이슈 리스트 연동
    embedUrl: 'https://www.youtube.com/embed/videoseries?list=PL6U2qX9gCsq2sV6p0hJsn9C3v9U1K5x_y'
  },
  {
    id: 'hong',
    name: '홍춘욱의 쉬운 경제',
    desc: '이코노미스트의 시장 분석 및 투자 경제학',
    logo: '📈',
    // 홍춘욱 채널 대표 목록 연동
    embedUrl: 'https://www.youtube.com/embed/videoseries?list=PL9XzO49l7bM1pD38vHkM3kHhN5O3nJ62o'
  }
];

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeChannel, setActiveChannel] = useState(YOUTUBE_CHANNELS[0]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('./data.json');
      if (!response.ok) {
        throw new Error('데이터를 찾을 수 없습니다. 파이썬 스크립트(main.py)를 먼저 작동시켜주세요.');
      }
      const jsonData = await response.json();
      setData(jsonData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const getIndexStatus = (percent) => {
    if (percent > 0) {
      return {
        colorClass: 'text-red-400',
        glowClass: 'glow-red',
        bgClass: 'bg-red-500/10',
        Icon: TrendingUp,
        sign: '+'
      };
    } else if (percent < 0) {
      return {
        colorClass: 'text-blue-400',
        glowClass: 'glow-blue',
        bgClass: 'bg-blue-500/10',
        Icon: TrendingDown,
        sign: ''
      };
    } else {
      return {
        colorClass: 'text-gray-400',
        glowClass: '',
        bgClass: 'bg-gray-500/10',
        Icon: Minus,
        sign: ''
      };
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen text-indigo-200">
        <RefreshCw className="w-12 h-12 animate-spin mb-4 text-indigo-400" />
        <p className="text-lg animate-pulse-slow">글로벌 증시 시황 데이터를 불러오는 중입니다...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-6 text-center">
        <div className="glass-card max-w-md p-8 border-red-500/30 glow-red">
          <Info className="w-16 h-16 text-red-400 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-red-200 mb-2">데이터 로드 실패</h2>
          <p className="text-gray-400 mb-6">{error}</p>
          <button 
            onClick={fetchData}
            className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-500 transition-colors text-white font-medium rounded-xl flex items-center justify-center gap-2 mx-auto"
          >
            <RefreshCw className="w-4 h-4" /> 다시 시도
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 md:py-12">
      {/* Header Area */}
      <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8 pb-6 border-b border-white/5">
        <div>
          <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-indigo-200 to-indigo-400 bg-clip-text text-transparent flex items-center gap-2">
            <LineChart className="text-indigo-400 w-8 h-8 md:w-10 md:h-10" /> Global Market Hub
          </h1>
          <p className="text-gray-400 mt-2 text-sm md:text-base">
            미국 증시와 연동한 오늘의 국내 주식 시장 핵심 인사이트 대시보드
          </p>
        </div>
        <div className="flex items-center gap-3 self-start md:self-center bg-white/3 border border-white/5 px-4 py-2 rounded-2xl text-xs md:text-sm">
          <Clock className="w-4 h-4 text-indigo-400" />
          <span className="text-gray-400">최근 업데이트:</span>
          <span className="text-white font-semibold">{data?.updated_at}</span>
          <button 
            onClick={fetchData}
            className="ml-2 p-1.5 hover:bg-white/5 rounded-lg transition-colors text-gray-400 hover:text-white"
            title="새로고침"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>
      </header>

      {/* [NEW] 1. YouTube Financial Media Station */}
      <section className="mb-10">
        <h2 className="text-lg font-bold text-gray-300 mb-4 flex items-center gap-2">
          <svg className="text-red-500 w-5 h-5 fill-current" viewBox="0 0 24 24">
            <path d="M23.498 6.163c-.272-1.016-1.07-1.817-2.084-2.09C19.57 3.792 12 3.792 12 3.792s-7.57 0-9.414.482c-1.013.273-1.812 1.074-2.084 2.09C0 8.002 0 12 0 12s0 3.998.502 5.837c.272 1.016 1.07 1.817 2.084 2.09C4.43 20.208 12 20.208 12 20.208s7.57 0 9.414-.482c1.013-.273 1.812-1.074 2.084-2.09C24 15.998 24 12 24 12s0-3.998-.502-5.837zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
          </svg>
          실시간 추천 금융 방송
        </h2>
        <div className="glass-card p-4 md:p-6 grid grid-cols-1 lg:grid-cols-3 gap-6 border-indigo-500/10 shadow-indigo-950/20">
          
          {/* YouTube Video Screen */}
          <div className="lg:col-span-2">
            <div className="video-responsive rounded-xl overflow-hidden border border-white/5 bg-black/40">
              <iframe
                title={activeChannel.name}
                src={activeChannel.embedUrl}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowFullScreen
                className="absolute top-0 left-0 w-full h-full border-0"
              ></iframe>
            </div>
          </div>

          {/* Channel Selection Tab Panel */}
          <div className="flex flex-col justify-between">
            <div>
              <p className="text-xs font-bold text-indigo-400 tracking-wider uppercase mb-3">
                채널 선택하기
              </p>
              
              {/* Horizontal scroll chips on mobile, vertical list on desktop */}
              <div className="flex lg:flex-col gap-3 overflow-x-auto lg:overflow-x-visible pb-3 lg:pb-0 scrollbar-thin">
                {YOUTUBE_CHANNELS.map((ch) => {
                  const isActive = activeChannel.id === ch.id;
                  return (
                    <button
                      key={ch.id}
                      onClick={() => setActiveChannel(ch)}
                      className={`flex items-center gap-3 p-3 text-left rounded-xl transition-all border whitespace-nowrap lg:whitespace-normal flex-shrink-0 lg:flex-shrink ${
                        isActive 
                          ? 'bg-indigo-500/10 border-indigo-500/40 text-white shadow-md shadow-indigo-500/5' 
                          : 'bg-white/2 border-white/5 hover:bg-white/5 text-gray-400 hover:text-gray-200'
                      }`}
                    >
                      <span className="text-xl flex-shrink-0">{ch.logo}</span>
                      <div className="overflow-hidden">
                        <span className="font-bold text-sm block tracking-tight">{ch.name}</span>
                        <span className="text-[11px] text-gray-400 hidden md:block lg:line-clamp-1">
                          {ch.desc}
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
            
            {/* Info Message Box */}
            <div className="mt-4 lg:mt-0 p-3 bg-white/2 border border-white/5 rounded-xl text-xs text-gray-500 flex items-start gap-2">
              <Play className="w-3.5 h-3.5 text-indigo-400 mt-0.5 flex-shrink-0" />
              <p className="leading-relaxed">
                해당 채널이 실시간 방송 중일 경우 플레이어에 라이브 스트리밍이 즉시 로드됩니다.
              </p>
            </div>
          </div>

        </div>
      </section>

      {/* 2. Market Indices Grid */}
      <section className="mb-10">
        <h2 className="text-lg font-bold text-gray-300 mb-4 flex items-center gap-2">
          📊 실시간 주요 증시 지표
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {data?.indices && Object.entries(data.indices).map(([name, info]) => {
            if (!info) return null;
            const { colorClass, glowClass, bgClass, Icon, sign } = getIndexStatus(info.percent);
            
            return (
              <div 
                key={name} 
                className={`glass-card p-5 flex flex-col justify-between min-h-[125px] ${glowClass}`}
              >
                <div>
                  <span className="text-xs md:text-sm font-semibold text-gray-400 block mb-1">{name}</span>
                  <span className="text-lg md:text-xl font-bold tracking-tight text-white block">
                    {info.price.toLocaleString()}
                  </span>
                </div>
                <div className={`flex items-center gap-1.5 mt-3 px-2.5 py-1 rounded-xl w-fit ${bgClass} ${colorClass}`}>
                  <Icon className="w-4 h-4" />
                  <span className="text-xs font-bold">
                    {sign}{info.percent}%
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* 3. Main content split layout (Briefing & News) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* AI Briefing Section (Left & Center 2 Columns) */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          <section className="glass-card p-6 md:p-8 flex-1 border-indigo-500/10 shadow-indigo-950/10">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2 border-b border-white/5 pb-4">
              <Sparkles className="text-indigo-400 w-5 h-5 animate-pulse-slow" /> Gemini AI 시황 종합 브리핑
            </h2>
            <div className="markdown-body text-gray-300">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {data?.summary || '요약 리포트를 찾을 수 없습니다.'}
              </ReactMarkdown>
            </div>
          </section>
        </div>

        {/* Global News Section (Right 1 Column) */}
        <div className="flex flex-col gap-6">
          <section className="glass-card p-6 flex-1 flex flex-col border-white/5">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2 border-b border-white/5 pb-4">
              <Newspaper className="text-indigo-400 w-5 h-5" /> 실시간 헤드라인 뉴스
            </h2>
            <div className="flex flex-col gap-4 overflow-y-auto max-h-[600px] pr-2">
              {data?.news && data.news.length > 0 ? (
                data.news.map((item, index) => (
                  <a 
                    key={index} 
                    href={item.link} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="glass-card p-4 hover:bg-white/5 hover:translate-y-0 hover:border-white/10 flex flex-col justify-between gap-3 text-gray-300 hover:text-white"
                  >
                    <p className="text-sm md:text-base font-semibold leading-snug line-clamp-2">
                      {item.title}
                    </p>
                    <span className="text-xs text-indigo-400 font-medium flex items-center gap-1 self-end">
                      자세히 보기 <ChevronRight className="w-3 h-3" />
                    </span>
                  </a>
                ))
              ) : (
                <p className="text-gray-500 text-center py-10">오늘 등록된 주요 해외 증시 뉴스가 없습니다.</p>
              )}
            </div>
          </section>
        </div>

      </div>

      {/* Footer area */}
      <footer className="mt-16 pt-8 border-t border-white/5 text-center text-xs text-gray-500">
        <p>© 2026 Global Market Hub. Designed with Glassmorphic Premium Dark Mode.</p>
        <p className="mt-1">해당 프로그램은 투자 참고용 리포트를 생성하며, 모든 투자 결정에 대한 책임은 투자자 본인에게 있습니다.</p>
      </footer>
    </div>
  );
}

export default App;
