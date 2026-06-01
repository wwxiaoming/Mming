import Link from 'next/link';

const popularStocks = [
  { symbol: 'AAPL', name: 'Apple' },
  { symbol: 'MSFT', name: 'Microsoft' },
  { symbol: 'TSLA', name: 'Tesla' },
  { symbol: 'GOOGL', name: 'Google' },
  { symbol: 'AMZN', name: 'Amazon' },
  { symbol: 'NVDA', name: 'NVIDIA' },
];

export default function Home({ searchParams }) {
  const selected = searchParams?.stock || '';
  
  return (
    <div style={{ 
      minHeight: '100vh',
      backgroundColor: '#f5f5f5',
      padding: '20px'
    }}>
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        <h1 style={{ 
          fontSize: '28px', 
          fontWeight: 'bold', 
          marginBottom: '24px',
          textAlign: 'center'
        }}>
          📊 股票分析工具
        </h1>

        {/* 热门股票选择区域 */}
        <div style={{ 
          backgroundColor: 'white',
          padding: '20px',
          borderRadius: '16px',
          marginBottom: '24px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.08)'
        }}>
          <h2 style={{ fontSize: '18px', marginBottom: '16px', fontWeight: 'bold' }}>
            热门股票（点击选择）
          </h2>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(3, 1fr)', 
            gap: '12px'
          }}>
            {popularStocks.map((stock) => (
              <Link
                key={stock.symbol}
                href={`?stock=${stock.symbol}`}
                style={{
                  padding: '20px 12px',
                  backgroundColor: selected === stock.symbol ? '#1d4ed8' : '#2563eb',
                  color: 'white',
                  borderRadius: '12px',
                  fontSize: '18px',
                  textDecoration: 'none',
                  textAlign: 'center',
                  fontWeight: 'bold',
                  display: 'block'
                }}
              >
                {stock.symbol}
                <div style={{ fontSize: '13px', opacity: '0.9', marginTop: '4px' }}>
                  {stock.name}
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* 股票详情区域 */}
        {selected ? (
          <div style={{ 
            backgroundColor: 'white',
            padding: '24px',
            borderRadius: '16px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.08)'
          }}>
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '20px'
            }}>
              <div>
                <h2 style={{ fontSize: '24px', fontWeight: 'bold', margin: 0 }}>
                  {selected}
                </h2>
                <p style={{ color: '#666', margin: '4px 0 0 0' }}>
                  {popularStocks.find(s => s.symbol === selected)?.name || '股票'}
                </p>
              </div>
              <Link
                href="/"
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#f3f4f6',
                  color: '#374151',
                  borderRadius: '8px',
                  textDecoration: 'none',
                  fontSize: '14px',
                  fontWeight: '500'
                }}
              >
                返回选择
              </Link>
            </div>

            {/* 模拟价格信息 */}
            <div style={{ 
              backgroundColor: selected === 'AAPL' || selected === 'MSFT' || selected === 'NVDA' ? '#ecfdf5' : '#fef2f2',
              padding: '20px',
              borderRadius: '12px',
              marginBottom: '20px'
            }}>
              <div style={{ fontSize: '36px', fontWeight: 'bold', marginBottom: '8px' }}>
                ${(100 + Math.random() * 400).toFixed(2)}
              </div>
              <div style={{ 
                fontSize: '18px',
                color: selected === 'AAPL' || selected === 'MSFT' || selected === 'NVDA' ? '#059669' : '#dc2626'
              }}>
                {selected === 'AAPL' || selected === 'MSFT' || selected === 'NVDA' ? '+' : ''}
                {(Math.random() * 10 - 2).toFixed(2)} 
                ({selected === 'AAPL' || selected === 'MSFT' || selected === 'NVDA' ? '+' : ''}
                {(Math.random() * 5 - 1).toFixed(2)}%)
              </div>
            </div>

            {/* 模拟图表区域 */}
            <div style={{ 
              backgroundColor: '#f9fafb',
              padding: '20px',
              borderRadius: '12px',
              marginBottom: '20px',
              minHeight: '200px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#9ca3af',
              fontSize: '16px'
            }}>
              📈 图表区域（真实数据需要API）
            </div>

            {/* 关键指标 */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div style={{ 
                backgroundColor: '#f9fafb',
                padding: '16px',
                borderRadius: '8px'
              }}>
                <div style={{ fontSize: '14px', color: '#666', marginBottom: '4px' }}>市值</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                  ${((Math.random() * 2000) + 100).toFixed(0)}B
                </div>
              </div>
              <div style={{ 
                backgroundColor: '#f9fafb',
                padding: '16px',
                borderRadius: '8px'
              }}>
                <div style={{ fontSize: '14px', color: '#666', marginBottom: '4px' }}>成交量</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                  {((Math.random() * 50) + 10).toFixed(0)}M
                </div>
              </div>
              <div style={{ 
                backgroundColor: '#f9fafb',
                padding: '16px',
                borderRadius: '8px'
              }}>
                <div style={{ fontSize: '14px', color: '#666', marginBottom: '4px' }}>52周最高</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                  ${(200 + Math.random() * 400).toFixed(2)}
                </div>
              </div>
              <div style={{ 
                backgroundColor: '#f9fafb',
                padding: '16px',
                borderRadius: '8px'
              }}>
                <div style={{ fontSize: '14px', color: '#666', marginBottom: '4px' }}>52周最低</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                  ${(50 + Math.random() * 150).toFixed(2)}
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div style={{ 
            backgroundColor: 'white',
            padding: '40px 20px',
            borderRadius: '16px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '64px', marginBottom: '16px' }}>👆</div>
            <h2 style={{ fontSize: '20px', marginBottom: '8px' }}>
              请选择一支股票
            </h2>
            <p style={{ color: '#666', margin: 0 }}>
              点击上方的蓝色卡片来查看股票详情
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
