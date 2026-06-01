import Link from 'next/link';

const stocks = [
  { symbol: 'AAPL', name: 'Apple' },
  { symbol: 'MSFT', name: 'Microsoft' },
  { symbol: 'TSLA', name: 'Tesla' },
  { symbol: 'GOOGL', name: 'Google' },
];

export default function Home({ searchParams }) {
  const selected = searchParams.stock;

  return (
    <div style={{ padding: '20px', maxWidth: '500px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '24px', marginBottom: '20px' }}>股票选择器</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '30px' }}>
        {stocks.map((stock) => (
          <Link 
            key={stock.symbol}
            href={`/?stock=${stock.symbol}`}
            style={{
              padding: '24px 16px',
              backgroundColor: '#2563eb',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              fontSize: '20px',
              textDecoration: 'none',
              textAlign: 'center',
              fontWeight: 'bold'
            }}
          >
            {stock.symbol}
            <div style={{ fontSize: '14px', opacity: '0.9', marginTop: '4px' }}>{stock.name}</div>
          </Link>
        ))}
      </div>
      
      {selected && (
        <div style={{
          padding: '24px',
          backgroundColor: '#dcfce7',
          borderRadius: '12px',
          fontSize: '22px',
          textAlign: 'center',
          fontWeight: 'bold'
        }}>
          ✓ 你选择了：{selected}
        </div>
      )}
      
      <p style={{ marginTop: '24px', color: '#666', textAlign: 'center' }}>
        请点击上面的蓝色卡片来选择股票
      </p>
    </div>
  );
}
