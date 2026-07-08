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
  Info
} from 'lucide-react';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      // public/data.json 파일 로드
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

  // 지수 상승/하락에 따른 정보(색상, 아이콘) 반환 헬퍼
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
      <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-10 pb-6 border-b border-white/5">
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

      {/* 1. Market Indices Grid */}
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

      {/* 1.5 AI Pick Recommendations Section */}
      {data?.recommendations && data.recommendations.length > 0 && (
        <section className="mb-10">
          <h2 className="text-lg font-bold text-gray-300 mb-4 flex items-center gap-2">
            <Sparkles className="text-indigo-400 w-5 h-5 animate-pulse-slow" /> 💡 오늘의 AI Pick 국내 추천 종목
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.recommendations.map((rec, index) => (
              <div 
                key={index} 
                className="glass-card p-6 flex flex-col justify-between border-indigo-500/20 glow-indigo"
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className="px-3 py-1 text-xs font-semibold text-white rounded-full recommendation-badge">
                      {rec.sector}
                    </span>
                    <span className="text-xs font-mono text-gray-500">
                      {rec.ticker}
                    </span>
                  </div>
                  <h3 className="text-xl font-extrabold text-white mb-3">
                    {rec.name}
                  </h3>
                  <div className="space-y-3">
                    <div>
                      <span className="text-xs font-bold text-indigo-400 block mb-1">💡 추천 사유</span>
                      <p className="text-sm text-gray-300 leading-relaxed">{rec.reason}</p>
                    </div>
                    <div>
                      <span className="text-xs font-bold text-emerald-400 block mb-1">🎯 대응 전략</span>
                      <p className="text-sm text-gray-300 leading-relaxed">{rec.action_plan}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* 2. Main content split layout (Briefing & News) */}
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
