⚡ Smart Energy Load Balancer

The Smart Energy Balancer is a real-time Decision Support System (DSS) designed to manage a household or small-grid energy ecosystem. It acts as an "intelligent brain" positioned between energy sources (Solar, Battery) and energy sinks (Household Demand) to optimize costs, efficiency, and hardware longevity.

🚀 Key Features

1. Intelligent Load Balancing

   The system operates on a hierarchical priority logic to ensure the lowest possible utility cost:

   Priority 1: Solar – Maximum self-consumption. Solar is used first to satisfy demand.

   Priority 2: Battery – Utilized when solar is insufficient, governed by health-conscious hysteresis thresholds.

   Priority 3: Grid – The utility grid acts as a fail-safe to bridge any remaining energy gaps.

2. Hardware Protection (Hysteresis)

   To prevent "chattering" (rapid toggling) which degrades inverters and lithium cells, the system implements a "Deadband" buffer:

   Engagement Threshold: The battery won't discharge until it reaches 40%.

   Disengagement Threshold: Once active, the battery remains the source until it drops below 35%.

3. Peak Load Monitoring & Smoothing

   Demand Smoothing: Uses a deque (double-ended queue) to create a rolling average, preventing system overreaction to momentary spikes (e.g., a motor starting).

   Peak Alerts: Triggers a "Peak Mode" warning if demand exceeds 9.0 kW, allowing for manual or automated load shedding.

⚙️ Configuration

The system parameters can be adjusted within the config.py (or top-level constants) to match your specific hardware:

BATTERY_UPPER_LIMIT: Default 40% (Start using battery).

BATTERY_LOWER_LIMIT: Default 35% (Stop using battery).

MAX_GRID_THRESHOLD: Default 9.0 kW (Peak alarm trigger).

SMOOTHING_WINDOW: Number of data points for the rolling average.

📊 Technical Specifications

The logic is governed by the following energy balance equation

$$P_{grid} = P_{demand} - (P_{solar} + P_{battery})$$

Where:

$P_{solar}$ is prioritized until $P_{solar} \ge P_{demand}$.

$P_{battery}$ is only available if $SoC > Threshold_{Hysteresis}$.

$P_{grid}$ is the remainder, ensuring the load is always met.

📝 Future Roadmap

 Machine Learning: Predict solar generation based on weather API data.

 Multi-Battery Support: Manage multiple battery banks with independent health stats.

IoT Expansion: Native integration with smart plugs for automated non-essential load shedding.
