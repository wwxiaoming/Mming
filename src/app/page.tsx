'use client';

import { useState } from 'react';

const popularStocks = [
  { symbol: 'AAPL', name: 'Apple' },
  { symbol: 'MSFT', name: 'Microsoft' },
  { symbol: 'TSLA', name: 'Tesla' },
  { symbol: 'GOOGL', name: 'Google' },
  { symbol: 'AMZN', name: 'Amazon' },
  { symbol: 'NVDA', name: 'NVIDIA' },
];

export default function Home() {
  const [selectedStock, setSelectedStock] = useState(null);

  const handleStockClick = (stock) => {
    console.log('点击股票:', stock);
    setSelectedStock(stock);
    console.log('更新 selectedStock:', stock);
  };

  const handleReset = () => {
    console.log('重置选择');
    setSelectedStock(null);
  };

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
              <button
                key={stock.symbol}
                onClick={() => handleStockClick(stock)}
                onTouchStart={(e) => {
                  e.currentTarget.style.transform = 'scale(0.95)';
                  e.currentTarget.style.opacity = '0.8';
                }}
                onTouchEnd={(e) => {
                  e.currentTarget.style.transform = '';
                  e.currentTarget.style.opacity = '';
                }}
                style={{
                  padding: '20px 12px',
                  minHeight: '44px',
                  minWidth: '44px',
                  backgroundColor: selectedStock?.symbol === stock.symbol ? '#1d4ed8' : '#2563eb',
                  color: 'white',
                  border: 'none',
                  borderRadius: '12px',
                  fontSize: '18px',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  width: '100%',
                  touchAction: 'manipulation',
                  transition: 'transform 0.1s, opacity 0.1s'
                }}
              >
                {stock.symbol}
                <div style={{ fontSize: '13px', opacity: '0.9', marginTop: '4px' }}>
                  {stock.name}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* 股票详情区域 */}
        {selectedStock ? (
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
                  {selectedStock.symbol}
                </h2>
                <p style={{ color: '#666', margin: '4px 0 0 0' }}>
                  {selectedStock.name}
                </p>
              </div>
              <button
                onClick={handleReset}
                onTouchStart={(e) => {
                  e.currentTarget.style.transform = 'scale(0.95)';
                  e.currentTarget.style.opacity = '0.8';
                }}
                onTouchEnd={(e) => {
                  e.currentTarget.style.transform = '';
                  e.currentTarget.style.opacity = '';
                }}
                style={{
                  padding: '10px 20px',
                  minHeight: '44px',
                  minWidth: '44px',
                  backgroundColor: '#f3f4f6',
                  color: '#374151',
                  border: 'none',
                  borderRadius: '8px',
                  fontSize: '14px',
                  fontWeight: '500',
                  cursor: 'pointer',
                  touchAction: 'manipulation',
                  transition: 'transform 0.1s, opacity 0.1s'
                }}
              >
                返回选择
              </button>
            </div>

            {/* 模拟价格信息 */}
            <div style={{ 
              backgroundColor: selectedStock.symbol === 'AAPL' || selectedStock.symbol === 'MSFT' || selectedStock.symbol === 'NVDA' ? '#ecfdf5' : '#fef2f2',
              padding: '20px',
              borderRadius: '12px',
              marginBottom: '20px'
            }}>
              <div style={{ fontSize: '36px', fontWeight: 'bold', marginBottom: '8px' }}>
                ${(100 + Math.random() * 400).toFixed(2)}
              </div>
              <div style={{ 
                fontSize: '18px',
                color: selectedStock.symbol === 'AAPL' || selectedStock.symbol === 'MSFT' || selectedStock.symbol === 'NVDA' ? '#059669' : '#dc2626'
              }}>
                {selectedStock.symbol === 'AAPL' || selectedStock.symbol === 'MSFT' || selectedStock.symbol === 'NVDA' ? '+' : ''}
                {(Math.random() * 10 - 2).toFixed(2)} 
                ({selectedStock.symbol === 'AAPL' || selectedStock.symbol === 'MSFT' || selectedStock.symbol === 'NVDA' ? '+' : ''}
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
