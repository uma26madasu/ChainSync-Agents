"""
ChainSync AI Agent - Main Application Entry Point
"""
import asyncio
import logging
from chainsync.config import Config
from chainsync.ai_agent import ChainSyncAIAgent

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def main():
    """Main application entry point"""
    print(" ChainSync Unified AI Agent v2.0")
    print("=" * 60)
    
    # Validate configuration
    if not Config.validate():
        return
    
    # Initialize AI Agent
    agent = ChainSyncAIAgent()
    
    # Run demo tests
    print("\n Running AI Agent Demo...")
    
    # Test 1: Domain Analysis
    result = await agent.analyze_with_domain_context(
        "Analyze current environmental risks and provide cross-domain recommendations",
        conversation_id="demo-1",
        domain="environmental",
        facility_id="water-treatment-1"
    )
    
    print(f"AI Agent Response: {result['source']}")
    print(f"Analysis Preview: {result['response'][:200]}...")
    
    # Test 2: Risk Assessment
    facility_data = await agent.get_facility_data_from_chainsync("water-treatment-1")
    risk_assessment = agent.calculate_risk_assessment(facility_data)
    
    print(f"\n Risk Assessment:")
    print(f"   Level: {risk_assessment['level']} ({risk_assessment['score']}/10)")
    print(f"   Factors: {len(risk_assessment['factors'])} identified")
    print(f"   Python Analysis: {risk_assessment.get('pythonAnalysis', False)}")
    
    print("\n ChainSync AI Agent is ready!")
    print(" Python AI component successfully initialized")
    print(" Ready for MuleSoft integration layer")

if __name__ == "__main__":
    asyncio.run(main())