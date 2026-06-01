"use client";

import { useState } from "react";

export default function Home() {
  const [clicked, setClicked] = useState("");

  function handleClick(name) {
    setClicked(`你点击了：${name}`);
  }

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '24px', marginBottom: '20px' }}>测试点击</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
        <button
          onClick={() => handleClick("AAPL")}
          style={{
            padding: '20px',
            backgroundColor: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '10px',
            fontSize: '18px',
            cursor: 'pointer'
          }}
        >
          AAPL
        </button>
        
        <button
          onClick={() => handleClick("MSFT")}
          style={{
            padding: '20px',
            backgroundColor: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '10px',
            fontSize: '18px',
            cursor: 'pointer'
          }}
        >
          MSFT
        </button>
        
        <button
          onClick={() => handleClick("TSLA")}
          style={{
            padding: '20px',
            backgroundColor: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '10px',
            fontSize: '18px',
            cursor: 'pointer'
          }}
        >
          TSLA
        </button>
        
        <button
          onClick={() => handleClick("GOOGL")}
          style={{
            padding: '20px',
            backgroundColor: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '10px',
            fontSize: '18px',
            cursor: 'pointer'
          }}
        >
          GOOGL
        </button>
      </div>
      
      {clicked && (
        <div style={{
          marginTop: '30px',
          padding: '20px',
          backgroundColor: '#dcfce7',
          borderRadius: '10px',
          fontSize: '20px',
          textAlign: 'center'
        }}>
          {clicked}
        </div>
      )}
      
      <p style={{ marginTop: '20px', color: '#666' }}>
        请点击上面的蓝色按钮测试
      </p>
    </div>
  );
}
