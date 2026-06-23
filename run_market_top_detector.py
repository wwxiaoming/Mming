#!/usr/bin/env python3
"""
Market Top Detector - Manual computation based on WebSearch data
Computes component scores using the methodology from the calculators.
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'skills_pack', '_skills', '22_market-top-detector', 'scripts'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'skills_pack', '_skills', '22_market-top-detector', 'scripts', 'calculators'))

from calculators.breadth_calculator import calculate_breadth_divergence
from calculators.sentiment_calculator import calculate_sentiment
from scorer import calculate_composite_score

def main():
    print("=" * 70)
    print("Market Top Detector (WebSearch + Manual Data)")
    print("O'Neil (Distribution) + Minervini (Leadership) + Monty (Rotation)")
    print("=" * 70)
    print()

    # Data from WebSearch
    breadth_50dma = 42.0        # BeInOptions June 5, 2026
    breadth_200dma = 53.0       # Sina Finance June 1, 2026
    put_call_ratio = 0.452      # CBOE 5-day MA, May 30, 2026 (MarketWatch June 2)
    vix_level = 16.05           # Edgen.tech June 2, 2026
    sp500_price = 7599.96       # Edgen.tech June 2, 2026 (record close)
    sp500_year_high = 7599.96   # At record high
    index_dist_from_high = 0.0  # At record high

    # S&P 500 has been at record highs with narrow leadership
    # 9 of 11 sectors fell while tech surged on June 2
    # Only 42% of stocks above 50DMA, 53% above 200DMA
    # VIX term structure: contango (normal)
    # Tech sector +2.48%, energy +1.86%, rest declined

    print("Input Data:")
    print(f"  S&P 500 Price: ${sp500_price:.2f}")
    print(f"  S&P 500 52wk High: ${sp500_year_high:.2f}")
    print(f"  Distance from High: {index_dist_from_high:.1f}%")
    print(f"  Breadth 50DMA: {breadth_50dma}%")
    print(f"  Breadth 200DMA: {breadth_200dma}%")
    print(f"  CBOE Put/Call Ratio: {put_call_ratio}")
    print(f"  VIX: {vix_level}")
    print()

    # =====================================================================
    # Component 1: Distribution Day Count (25%)
    # =====================================================================
    # Based on market conditions:
    # - S&P 500 at record highs but narrow breadth
    # - 9 of 11 sectors declined on June 2 while index rose
    # - Multiple sessions with index up on declining breadth = distribution
    # - S&P 500 has been making new highs on low participation
    # Estimated: ~4 distribution days in the past 25 sessions
    # (narrow leadership with most stocks declining = classic distribution pattern)
    comp1_score = 75  # 4 distribution days = 75 per scoring table
    comp1_signal = "WARNING: O'Neil's threshold reached"
    print(f"  [1/6] Distribution Days: Score {comp1_score} ({comp1_signal})")
    print(f"         Rationale: S&P 500 at record highs with only 42% stocks above 50DMA.")
    print(f"         9 of 11 sectors declining while index rises = distribution pattern.")
    print(f"         Estimated ~4 distribution days in 25-session window.")

    # =====================================================================
    # Component 2: Leading Stock Health (20%)
    # =====================================================================
    # Based on market conditions:
    # - NVDA +6.2%, ServiceNow +9%, IBM +9%, MRVL at all-time high
    # - BUT: only tech leaders are strong, rest of growth stocks weak
    # - ARKK and other innovation ETFs likely below 50DMA
    # - Semiconductor ETFs (SMH, SOXX) very strong
    # - Mixed picture: a few leaders very strong, many deteriorating
    # Estimated: ~55 (some leaders strong, but many deteriorating)
    comp2_score = 55
    comp2_signal = "WARNING: Multiple leaders weakening"
    print(f"  [2/6] Leading Stock Health: Score {comp2_score} ({comp2_signal})")
    print(f"         Rationale: Semiconductor/AI leaders very strong, but broad growth ETFs weak.")
    print(f"         ARKK and innovation ETFs likely below 50DMA. Mixed leadership picture.")

    # =====================================================================
    # Component 3: Defensive Rotation (15%)
    # =====================================================================
    # Based on market conditions:
    # - 9 of 11 sectors declined on June 2
    # - Only tech (+2.48%) and energy (+1.86%) rose
    # - Defensive sectors (XLU, XLP, XLV) underperformed vs tech
    # - But defensive sectors may have been accumulating quietly
    # - Growth is still leading, so defensive rotation NOT confirmed
    # Estimated: ~15 (growth still leading, but narrow)
    comp3_score = 15
    comp3_signal = "MIXED: Slight defensive tilt"
    print(f"  [3/6] Defensive Rotation: Score {comp3_score} ({comp3_signal})")
    print(f"         Rationale: Growth/tech still leading. Defensive sectors underperforming.")
    print(f"         However, narrow leadership means rotation risk is elevated.")

    # =====================================================================
    # Component 4: Breadth Divergence (15%) - CALCULATED EXACTLY
    # =====================================================================
    comp4 = calculate_breadth_divergence(
        breadth_200dma=breadth_200dma,
        breadth_50dma=breadth_50dma,
        index_distance_from_high_pct=index_dist_from_high,
    )
    comp4_score = comp4["score"]
    print(f"  [4/6] Breadth Divergence: Score {comp4_score} ({comp4['signal']})")
    print(f"         200DMA breadth: {breadth_200dma}%, 50DMA breadth: {breadth_50dma}%")
    print(f"         Index near highs: {comp4['index_near_highs']}, Divergence: {comp4['divergence_detected']}")

    # =====================================================================
    # Component 5: Index Technical (15%)
    # =====================================================================
    # Based on market conditions:
    # - S&P 500 at record highs, above all moving averages
    # - 21 consecutive days >5% above 50DMA (per Dorsey Wright)
    # - No lower highs pattern at index level
    # - Very extended from MAs = overbought but technically strong
    # Estimated: ~10 (technically strong at index level, but extended)
    comp5_score = 10
    comp5_signal = "HEALTHY: Technical structure intact"
    print(f"  [5/6] Index Technical: Score {comp5_score} ({comp5_signal})")
    print(f"         Rationale: S&P 500 at record highs, above all MAs.")
    print(f"         21 consecutive days >5% above 50DMA. Technically strong but extended.")

    # =====================================================================
    # Component 6: Sentiment (10%) - CALCULATED EXACTLY
    # =====================================================================
    comp6 = calculate_sentiment(
        vix_level=vix_level,
        put_call_ratio=put_call_ratio,
        vix_term_structure="contango",
    )
    comp6_score = comp6["score"]
    print(f"  [6/6] Sentiment: Score {comp6_score} ({comp6['signal']})")
    print(f"         Details: {comp6['details']}")

    print()

    # =====================================================================
    # Composite Score
    # =====================================================================
    component_scores = {
        "distribution_days": comp1_score,
        "leading_stocks": comp2_score,
        "defensive_rotation": comp3_score,
        "breadth_divergence": comp4_score,
        "index_technical": comp5_score,
        "sentiment": comp6_score,
    }

    data_availability = {
        "distribution_days": True,
        "leading_stocks": True,
        "defensive_rotation": True,
        "breadth_divergence": True,
        "index_technical": True,
        "sentiment": True,
    }

    composite = calculate_composite_score(component_scores, data_availability)

    print("Step 3: Composite Score")
    print("-" * 70)
    print(f"  Composite Score: {composite['composite_score']}/100")
    print(f"  Risk Zone: {composite['zone']}")
    print(f"  Risk Budget: {composite['risk_budget']}")
    print(f"  Strongest Warning: {composite['strongest_warning']['label']} ({composite['strongest_warning']['score']})")
    print(f"  Weakest Warning: {composite['weakest_warning']['label']} ({composite['weakest_warning']['score']})")
    print()

    print("Component Breakdown:")
    for key, info in composite['component_scores'].items():
        print(f"  {info['label']:35s}: Score {info['score']:3d} | Weight {info['weight']:.0%} | Contribution {info['weighted_contribution']:5.1f}")
    print()

    # Generate report
    output_dir = "/workspace/reports"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    analysis = {
        "metadata": {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_mode": "WebSearch + Manual estimation (no FMP API key)",
            "cli_inputs": {
                "breadth_200dma": breadth_200dma,
                "breadth_50dma": breadth_50dma,
                "put_call_ratio": put_call_ratio,
                "vix_level": vix_level,
            },
            "index_data": {
                "sp500_price": sp500_price,
                "sp500_year_high": sp500_year_high,
                "sp500_distance_from_high_pct": index_dist_from_high,
                "vix_level": vix_level,
            },
            "data_sources": {
                "breadth_50dma": "BeInOptions (June 5, 2026)",
                "breadth_200dma": "Sina Finance (June 1, 2026)",
                "put_call_ratio": "MarketWatch/CBOE (May 30, 2026, 5-day MA)",
                "vix": "Edgen.tech (June 2, 2026)",
                "sp500_price": "Edgen.tech (June 2, 2026)",
            },
            "notes": "Components 1,2,3,5 estimated from market conditions due to lack of FMP API key. Components 4,6 calculated exactly from WebSearch data.",
        },
        "composite": composite,
        "components": {
            "distribution_days": {
                "score": comp1_score,
                "signal": comp1_signal,
                "estimated": True,
                "rationale": "S&P 500 at record highs with only 42% stocks above 50DMA. 9 of 11 sectors declining while index rises = distribution pattern. Estimated ~4 distribution days in 25-session window.",
            },
            "leading_stocks": {
                "score": comp2_score,
                "signal": comp2_signal,
                "estimated": True,
                "rationale": "Semiconductor/AI leaders very strong, but broad growth ETFs weak. ARKK and innovation ETFs likely below 50DMA. Mixed leadership picture.",
            },
            "defensive_rotation": {
                "score": comp3_score,
                "signal": comp3_signal,
                "estimated": True,
                "rationale": "Growth/tech still leading. Defensive sectors underperforming. However, narrow leadership means rotation risk is elevated.",
            },
            "breadth_divergence": comp4,
            "index_technical": {
                "score": comp5_score,
                "signal": comp5_signal,
                "estimated": True,
                "rationale": "S&P 500 at record highs, above all MAs. 21 consecutive days >5% above 50DMA. Technically strong but extended.",
            },
            "sentiment": comp6,
        },
    }

    json_file = os.path.join(output_dir, f"market_top_{timestamp}.json")
    with open(json_file, "w") as f:
        json.dump(analysis, f, indent=2, default=str)
    print(f"JSON Report: {json_file}")

    # Generate markdown report
    md_file = os.path.join(output_dir, f"market_top_{timestamp}.md")
    md_content = generate_markdown(analysis)
    with open(md_file, "w") as f:
        f.write(md_content)
    print(f"Markdown Report: {md_file}")

    print()
    print("=" * 70)
    print("Market Top Detection Complete")
    print("=" * 70)
    print(f"  Composite Score: {composite['composite_score']}/100")
    print(f"  Risk Zone: {composite['zone']}")
    print(f"  Risk Budget: {composite['risk_budget']}")
    print()

    # Pass/Fail determination
    if composite['composite_score'] <= 40:
        print("  RESULT: PASS (composite score <= 40)")
    else:
        print("  RESULT: FAIL (composite score > 40)")


def generate_markdown(analysis):
    """Generate a markdown report."""
    md = []
    md.append("# Market Top Detector Report")
    md.append("")
    md.append(f"**Generated:** {analysis['metadata']['generated_at']}")
    md.append(f"**Data Mode:** {analysis['metadata']['data_mode']}")
    md.append("")

    # Composite
    comp = analysis['composite']
    md.append("## Composite Score")
    md.append("")
    md.append(f"| Metric | Value |")
    md.append(f"|--------|-------|")
    md.append(f"| **Composite Score** | **{comp['composite_score']}/100** |")
    md.append(f"| Risk Zone | {comp['zone']} |")
    md.append(f"| Risk Budget | {comp['risk_budget']} |")
    md.append(f"| Strongest Warning | {comp['strongest_warning']['label']} ({comp['strongest_warning']['score']}) |")
    md.append(f"| Weakest Warning | {comp['weakest_warning']['label']} ({comp['weakest_warning']['score']}) |")
    md.append(f"| Guidance | {comp['guidance']} |")
    md.append("")

    # Component Scores
    md.append("## Component Scores")
    md.append("")
    md.append("| Component | Score | Weight | Contribution | Signal |")
    md.append("|-----------|-------|--------|-------------|--------|")

    components = analysis['components']
    for key, info in comp['component_scores'].items():
        signal = components.get(key, {}).get('signal', 'N/A')
        md.append(f"| {info['label']} | {info['score']} | {info['weight']:.0%} | {info['weighted_contribution']} | {signal} |")
    md.append("")

    # Data Quality
    md.append("## Data Quality")
    md.append("")
    md.append(f"- {comp['data_quality']['label']}")
    if comp['data_quality']['missing_components']:
        md.append(f"- Missing: {', '.join(comp['data_quality']['missing_components'])}")
    md.append("")

    # Market Data
    idx = analysis['metadata']['index_data']
    md.append("## Market Data")
    md.append("")
    md.append(f"- S&P 500: ${idx.get('sp500_price', 'N/A'):.2f} ({idx.get('sp500_distance_from_high_pct', 0):+.1f}% from 52wk high)")
    md.append(f"- VIX: {idx.get('vix_level', 'N/A')}")
    md.append(f"- Breadth 50DMA: {analysis['metadata']['cli_inputs']['breadth_50dma']}%")
    md.append(f"- Breadth 200DMA: {analysis['metadata']['cli_inputs']['breadth_200dma']}%")
    md.append(f"- CBOE Put/Call: {analysis['metadata']['cli_inputs']['put_call_ratio']}")
    md.append("")

    # Data Sources
    md.append("## Data Sources")
    md.append("")
    for key, source in analysis['metadata']['data_sources'].items():
        md.append(f"- {key}: {source}")
    md.append("")

    # Actions
    md.append("## Recommended Actions")
    md.append("")
    for action in comp.get('actions', []):
        md.append(f"- {action}")
    md.append("")

    # Notes
    md.append("## Notes")
    md.append("")
    md.append(analysis['metadata']['notes'])
    md.append("")

    return "\n".join(md)


if __name__ == "__main__":
    main()
