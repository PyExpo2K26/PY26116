Energy Load Balancer

The Smart Energy Balancer Dashboard is a real-time Decision Support System (DSS) designed to manage a household or small-grid energy ecosystem. It acts as an "intelligent brain" that sits between energy sources (Solar, Battery) and energy sinks (Household Demand) to optimize costs, efficiency, and hardware longevity.

Project Overview

At its core, the program is a Dynamic Resource Allocator. In modern "Green Homes," power management is no longer a one-way street. With fluctuating solar production and finite battery reserves, this program solves the "Who provides power now?" problem.
By utilizing Hysteresis logic, the system prevents "jitter" (rapid switching), protecting expensive electrical components like inverters and lithium batteries from unnecessary wear and tear.

Key Functions

1. Intelligent Load Balancing
   The system follows a strict priority hierarchy to ensure the cheapest and cleanest energy is utilized first:

    Priority 1: Solar – If solar power is available, it is used first to satisfy house demand.

    Priority 2: Battery – If solar is insufficient, the system checks battery health based on Hysteresis thresholds.

    Priority 3: Grid – The utility grid is treated as a last resort to bridge any remaining energy gap.

2. Hardware Protection (Hysteresis)

   To prevent "chattering" (rapid toggling) when a battery level hovers near a limit, the program implements a buffer zone:

   Engagement Threshold: The battery won't discharge until it reaches 40%.

   Disengagement Threshold: Once active, it stays on until it drops below 35%.

3. Peak Load Monitoring

   The system monitors total household demand against a safety threshold (default: $9.0$ kW). If exceeded, a "Peak Mode" warning is triggered, which can be used to shed non-essential loads (e.g., pool heaters) to avoid utility surcharges.

4. Real-Time Visualization & Logging

   Built on the Streamlit web framework, the dashboard provides a live energy "cockpit":

   Instant Metrics: Real-time kW usage displayed via high-visibility cards.

   Trend Tracking: Live line charts illustrating solar production vs. grid consumption.

   Audit Trail: Persistent logging of every system decision, exportable via CSV for monthly energy audits.
   
