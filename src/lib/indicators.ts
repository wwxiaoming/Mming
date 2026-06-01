export function calcMA(data: number[], period: number): (number | null)[] {
  const result: (number | null)[] = [];
  for (let i = 0; i < data.length; i++) {
    if (i < period - 1) {
      result.push(null);
    } else {
      let sum = 0;
      for (let j = i - period + 1; j <= i; j++) {
        sum += data[j];
      }
      result.push(sum / period);
    }
  }
  return result;
}

export function calcEMA(data: number[], period: number): (number | null)[] {
  const result: (number | null)[] = [];
  const multiplier = 2 / (period + 1);

  for (let i = 0; i < data.length; i++) {
    if (i < period - 1) {
      result.push(null);
    } else if (i === period - 1) {
      let sum = 0;
      for (let j = 0; j < period; j++) {
        sum += data[j];
      }
      result.push(sum / period);
    } else {
      const prevEMA = result[i - 1]!;
      result.push((data[i] - prevEMA) * multiplier + prevEMA);
    }
  }
  return result;
}

export function calcMACD(closePrices: number[]): {
  dif: (number | null)[];
  dea: (number | null)[];
  histogram: (number | null)[];
} {
  const ema12 = calcEMA(closePrices, 12);
  const ema26 = calcEMA(closePrices, 26);

  const dif: (number | null)[] = [];
  for (let i = 0; i < closePrices.length; i++) {
    if (ema12[i] === null || ema26[i] === null) {
      dif.push(null);
    } else {
      dif.push(ema12[i]! - ema26[i]!);
    }
  }

  const difValues = dif.filter((v) => v !== null) as number[];
  const deaRaw = calcEMA(difValues, 9);

  const dea: (number | null)[] = [];
  let deaIdx = 0;
  for (let i = 0; i < dif.length; i++) {
    if (dif[i] === null) {
      dea.push(null);
    } else {
      dea.push(deaRaw[deaIdx]);
      deaIdx++;
    }
  }

  const histogram: (number | null)[] = [];
  for (let i = 0; i < dif.length; i++) {
    if (dif[i] === null || dea[i] === null) {
      histogram.push(null);
    } else {
      histogram.push(dif[i]! - dea[i]!);
    }
  }

  return { dif, dea, histogram };
}

export function calcRSI(closePrices: number[], period: number): (number | null)[] {
  const result: (number | null)[] = [];

  let avgGain = 0;
  let avgLoss = 0;

  for (let i = 0; i < closePrices.length; i++) {
    if (i < period) {
      result.push(null);
    } else if (i === period) {
      let sumGain = 0;
      let sumLoss = 0;
      for (let j = 1; j <= period; j++) {
        const change = closePrices[j] - closePrices[j - 1];
        if (change > 0) sumGain += change;
        else sumLoss += Math.abs(change);
      }
      avgGain = sumGain / period;
      avgLoss = sumLoss / period;

      if (avgLoss === 0) {
        result.push(100);
      } else {
        result.push(100 - 100 / (1 + avgGain / avgLoss));
      }
    } else {
      const change = closePrices[i] - closePrices[i - 1];
      const gain = change > 0 ? change : 0;
      const loss = change < 0 ? -change : 0;
      avgGain = (avgGain * (period - 1) + gain) / period;
      avgLoss = (avgLoss * (period - 1) + loss) / period;

      if (avgLoss === 0) {
        result.push(100);
      } else {
        result.push(100 - 100 / (1 + avgGain / avgLoss));
      }
    }
  }

  return result;
}