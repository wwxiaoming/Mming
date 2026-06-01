"use client";

import React from 'react';

export default function Home() {
  const [msg, setMsg] = React.useState('');

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '24px', marginBottom: '20px' }}>测试点击</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
        <button
          onClick={() => setMsg('你点击了：AAPL')}
          style={{
            padding: '20px',
            backgroundColor: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '10px',
            fontSize: '18px'
          }}
        >
          AAPL
        </button>
        
        <button
          onClick={() => setMsg('你点击了：MSFT')}
          style={{
            padding: '20px',
            backgroundColor: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '10px',
            fontSize: '18px'
          }}
        >
          MSFT
        </button>
        
        <button
          onClick={() => setMsg('你点击了：TSLA')}
          style={{
            padding: '20px',
            backgroundColor: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '10px',
            fontSize: '18px'
          }}
        >
          TSLA
        </button>
        
        <button
          onClick={() => setMsg('你点击了：GOOGL')}
          style={{
            padding: '20px',
            backgroundColor: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '10px',
            fontSize: '18px'
          }}
        >
          GOOGL
        </button>
      </div>
      
      {msg && (
        <div style={{
          marginTop: '30px',
          padding: '20px',
          backgroundColor: '#dcfce7',
          borderRadius: '10px',
          fontSize: '20px',
          textAlign: 'center'
        }}>
          {msg}
        </div>
      )}
    </div>
  );
}
