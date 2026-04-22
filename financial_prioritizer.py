import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class MarketData:
    """Represents real-time or historical market data relevant to a financial task."""
    trend_multiplier: float = 1.0  # > 1.0 for uptrend, < 1.0 for downtrend
    volatility_index: float = 0.0  # 0.0 to 1.0, where 1.0 is extremely volatile/risky
    sector_growth_rate: float = 0.0 # Expected growth rate for the sector (e.g., 0.05 for 5%)

@dataclass
class FinancialTask:
    """Represents a single financial task or investment opportunity."""
    task_id: str
    name: str
    profit_potential: float       # Expected absolute profit in currency
    urgency: float                # 1.0 (low) to 10.0 (critical)
    resources_required: float    # Capital, manpower, or time required
    market_data: Optional[MarketData] = None
    dependencies: List[str] = field(default_factory=list) # IDs of tasks that must be completed first

class FinancialPrioritizer:
    """
    Identifies and prioritizes financial tasks based on profit potential, 
    urgency, resource constraints, and market data.
    """

    URGENCY_WEIGHT: float = 1.5
    MARKET_WEIGHT: float = 1.2
    RESOURCE_EFFICIENCY_WEIGHT: float = 2.0

    def __init__(self, risk_tolerance: float = 0.5):
        """
        Initializes the prioritizer.
        
        :param risk_tolerance: 0.0 (risk-averse) to 1.0 (risk-seeking). 
                               Affects how volatility impacts the score.
        """
        self.risk_tolerance = max(0.0, min(1.0, risk_tolerance))

    def _calculate_market_adjustment(self, market_data: Optional[MarketData]) -> float:
        """Calculates a multiplier based on market conditions."""
        if market_data is None:
            return 1.0

        # Adjust profit potential based on trend and sector growth
        trend_adjustment = market_data.trend_multiplier * (1.0 + market_data.sector_growth_rate)

        # Adjust for volatility based on risk tolerance
        # High risk tolerance means volatility penalizes the score less
        volatility_penalty = market_data.volatility_index * (1.0 - self.risk_tolerance)
        
        adjusted_multiplier = trend_adjustment * (1.0 - volatility_penalty)
        return max(0.0, adjusted_multiplier)

    def _calculate_priority_score(self, task: FinancialTask) -> float:
        """
        Calculates the priority score for a single task.
        Score = (Profit * Market_Adj * Urgency_Factor) / (Resources + Epsilon)
        """
        if task.resources_required <= 0:
            logger.warning(f"Task '{task.task_id}' has zero or negative resources required. Defaulting to minimal resource cost.")
            resource_cost = 0.001
        else:
            resource_cost = task.resources_required

        market_adjustment = self._calculate_market_adjustment(task.market_data)
        
        # Urgency factor scales non-linearly to prioritize critical tasks
        urgency_factor = 1.0 + (task.urgency / 10.0) ** 2

        # Core ROI calculation
        base_roi = (task.profit_potential * market_adjustment * urgency_factor) / resource_cost

        # Apply strategic weights
        weighted_score = (
            base_roi * 
            (1.0 + (urgency_factor - 1.0) * self.URGENCY_WEIGHT) * 
            (1.0 + (market_adjustment - 1.0) * self.MARKET_WEIGHT) *
            self.RESOURCE_EFFICIENCY_WEIGHT
        )

        return weighted_score

    def prioritize_tasks(
        self, 
        tasks: List[FinancialTask], 
        available_resources: float
    ) -> List[FinancialTask]:
        """
        Prioritizes and selects the most profitable tasks given resource constraints.
        Uses a Greedy approach based on weighted ROI scoring, respecting dependencies.
        
        :param tasks: List of FinancialTask objects to evaluate.
        :param available_resources: Total resources (capital/time) currently available.
        :return: Ordered list of selected tasks representing the optimal execution plan.
        """
        if not tasks:
            logger.info("No tasks provided for prioritization.")
            return []

        logger.info(f"Starting prioritization for {len(tasks)} tasks with {available_resources} available resources.")

        # Calculate scores for all tasks
        scored_tasks: Dict[str, tuple] = {}
        for task in tasks:
            score = self._calculate_priority_score(task)
            scored_tasks[task.task_id] = (task, score)
            logger.debug(f"Task '{task.name}' (ID: {task.task_id}) calculated score: {score:.4f}")

        # Sort tasks by score descending
        sorted_tasks = sorted(scored_tasks.values(), key=lambda x: x[1], reverse=True)

        selected_tasks: List[FinancialTask] = []
        remaining_resources = available_resources
        selected_ids = set()

        # Iterative selection respecting dependencies and resource constraints
        changed = True
        while changed:
            changed = False
            for task, score in sorted_tasks:
                if task.task_id in selected_ids:
                    continue

                # Check if dependencies are met
                dependencies_met = all(dep_id in selected_ids for dep_id in task.dependencies)
                if not dependencies_met:
                    continue

                # Check if we have enough resources
                if task.resources_required <= remaining_resources:
                    selected_ids.add(task.task_id)
                    selected_tasks.append(task)
                    remaining_resources -= task.resources_required
                    changed = True
                    
                    logger.info(f"Selected Task: '{task.name}' (Score: {score:.2f}, Cost: {task.resources_required:.2f}). Remaining resources: {remaining_resources:.2f}")

        logger.info(f"Prioritization complete. Selected {len(selected_tasks)} tasks. Unallocated resources: {remaining_resources:.2f}")
        return selected_tasks


if __name__ == "__main__":
    # Example Usage and Validation
    
    # 1. Define Market Data
    bull_market = MarketData(trend_multiplier=1.2, volatility_index=0.2, sector_growth_rate=0.08)
    bear_market = MarketData(trend_multiplier=0.7, volatility_index=0.8, sector_growth_rate=-0.05)
    stable_market = MarketData(trend_multiplier=1.0, volatility_index=0.1, sector_growth_rate=0.02)

    # 2. Define Financial Tasks
    task_list = [
        FinancialTask(
            task_id="T1",
            name="High-Frequency Trading Algorithm Deployment",
            profit_potential=50000.0,
            urgency=9.0,
            resources_required=20000.0,
            market_data=bull_market
        ),
        FinancialTask(
            task_id="T2",
            name="Long-Term Bond Acquisition",
            profit_potential=15000.0,
            urgency=3.0,
            resources_required=50000.0,
            market_data=stable_market
        ),
        FinancialTask(
            task_id="T3",
            name="Distressed Asset Buyout",
            profit_potential=120000.0,
            urgency=7.0,
            resources_required=80000.0,
            market_data=bear_market,
            dependencies=["T1"]
        ),
        FinancialTask(
            task_id="T4",
            name="Internal Compliance Audit",
            profit_potential=0.0,
            urgency=10.0,
            resources_required=5000.0,
            market_data=None
        ),
        FinancialTask(
            task_id="T5",
            name="Crypto Yield Farming Exploration",
            profit_potential=30000.0,
            urgency=5.0,
            resources_required=10000.0,
            market_data=MarketData(trend_multiplier=1.5, volatility_index=0.9, sector_growth_rate=0.2)
        )
    ]

    # 3. Initialize Prioritizer (Moderate risk tolerance)
    prioritizer = FinancialPrioritizer(risk_tolerance=0.4)

    # 4. Execute Prioritization with 35,000 available resources
    total_available_capital = 35000.0
    optimal_plan = prioritizer.prioritize_tasks(task_list, total_available_capital)

    # 5. Output Results
    print("\n" + "="*60)
    print("OPTIMAL FINANCIAL TASK EXECUTION PLAN")
    print("="*60)
    for i, task in enumerate(optimal_plan, 1):
        print(f"{i}. {task.name} (ID: {task.task_id})")
        print(f"   - Expected Profit: ${task.profit_potential:,.2f}")
        print(f"   - Resource Cost:  ${task.resources_required:,.2f}")
        print(f"   - Urgency:        {task.urgency}/10")
        if task.market_data:
            print(f"   - Market Trend:   {task.market_data.trend_multiplier}x")
        print()
    print("="*60)
