// 主力净流入 (Net Inflow) — 自定义 KLineCharts 指标
//
// 公式: net = volume * (close - open) / (high - low)
//       当 high === low (一字板) 时返回 0
//
// 与 Mming 量化 / jzhu-quant 资金流向 tab 口径一致：
//  - 收盘 > 开盘 (涨) → 净流入 > 0 → 红色柱
//  - 收盘 < 开盘 (跌) → 净流入 < 0 → 绿色柱
//
// 图例: "主力净流入" / 数值格式化为 "X.X亿" (1e8)

import { registerIndicator } from 'klinecharts'

const NET_INFLOW_NAME = 'NET_INFLOW'
const NET_INFLOW_SHORT = '主力净流入'

function formatYi (value) {
  // value 单位: 股(1)  vs  手(100)  vs  元(>0) — 后端返回的 volume 单位是"股"还是"手"由数据源决定
  // 中文 A 股成交量通常是"手" (1手=100股), 1亿 = 1e8
  if (value == null || isNaN(value)) return '--'
  const yi = value / 1e8
  if (Math.abs(yi) >= 1) return `${yi.toFixed(2)}亿`
  const wan = value / 1e4
  if (Math.abs(wan) >= 1) return `${wan.toFixed(2)}万`
  return value.toFixed(0)
}

registerIndicator({
  name: NET_INFLOW_NAME,
  shortName: NET_INFLOW_SHORT,
  description: '基于 (close-open)/(high-low) 估算的主力资金净流入',
  // 1 周期:不需要参数
  calcParams: [],
  // 每个数据点计算出的数值数组
  calc: (dataList) => {
    return dataList.map((k) => {
      const { open, close, high, low, volume } = k
      if (high === low || !volume) return { net: 0 }
      const net = (volume * (close - open)) / (high - low)
      return { net }
    })
  },
  // 柱状图
  figures: [
    {
      key: 'net',
      type: 'bar',
      baseValue: 0,
      // 涨红跌绿 (与 jzhu-quant 资金流向 tab 一致)
      styles: (data, indicator, defaultStyles) => {
        const v = data.net || 0
        return {
          color: v >= 0 ? '#ef4444' : '#10b981',
          borderColor: v >= 0 ? '#ef4444' : '#10b981'
        }
      }
    }
  ],
  // tooltip 数据源
  createTooltipDataSource: ({ indicator }) => {
    const data = indicator.result
    return {
      name: NET_INFLOW_SHORT,
      calcParams: indicator.calcParams,
      values: data.net == null ? [] : [{ title: NET_INFLOW_SHORT, value: formatYi(data.net), color: data.net >= 0 ? '#ef4444' : '#10b981' }]
    }
  }
})

export { NET_INFLOW_NAME, NET_INFLOW_SHORT, formatYi }
export default NET_INFLOW_NAME
