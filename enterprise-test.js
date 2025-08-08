// enterprise-test.js - Comprehensive test suite for ChainSync Enterprise Agent
const axios = require('axios');

const AGENT_URL = 'http://localhost:3000';

class EnterpriseAgentTester {
  constructor() {
    this.results = [];
  }

  async runTest(testName, testFn) {
    console.log(`\n🧪 ${testName}`);
    console.log('━'.repeat(60));
    
    try {
      const startTime = Date.now();
      const result = await testFn();
      const duration = Date.now() - startTime;
      
      console.log(`✅ PASSED (${duration}ms)`);
      this.results.push({ test: testName, status: 'PASSED', duration });
      return result;
    } catch (error) {
      console.log(`❌ FAILED: ${error.message}`);
      this.results.push({ test: testName, status: 'FAILED', error: error.message });
      return null;
    }
  }

  async testFacilityList() {
    const response = await axios.get(`${AGENT_URL}/facilities`);
    console.log(`Found ${response.data.total} facilities:`);
    response.data.facilities.forEach(facility => {
      console.log(`  - ${facility.id} (${facility.type})`);
    });
    return response.data;
  }

  async testFacilityAnalysis() {
    const response = await axios.get(`${AGENT_URL}/facility/water-treatment-1`);
    const data = response.data;
    
    console.log(`Facility: ${data.facility.facilityId}`);
    console.log(`Type: ${data.facility.facilityType}`);
    console.log(`Risk Level: ${data.risk.level} (${data.risk.score}/10)`);
    console.log(`Risk Factors: ${data.risk.factors.join(', ') || 'None'}`);
    console.log(`Alert Status: ${data.alert ? data.alert.severity : 'No active alerts'}`);
    
    if (data.facility.parameters) {
      console.log('Parameters:');
      Object.entries(data.facility.parameters).forEach(([key, value]) => {
        console.log(`  - ${key}: ${typeof value === 'number' ? value.toFixed(2) : value}`);
      });
    }
    
    return data;
  }

  async testAIAnalysis() {
    const response = await axios.post(`${AGENT_URL}/analyze/waste-processing-1`, {
      question: "What are the current environmental risks and what actions should we take?",
      conversationId: "test-analysis-1"
    });
    
    const data = response.data;
    console.log(`Risk Assessment: ${data.riskAssessment.level} (${data.riskAssessment.score}/10)`);
    console.log(`AI Analysis Source: ${data.aiAnalysis.source}`);
    console.log(`AI Response Preview: ${data.aiAnalysis.response.substring(0, 200)}...`);
    console.log(`Recommendations: ${data.recommendations.length} items`);
    
    return data;
  }

  async testChatConversation() {
    // Start conversation
    const response1 = await axios.post(`${AGENT_URL}/chat`, {
      message: "What should I monitor for critical environmental conditions?",
      conversationId: "test-chat-1",
      agentType: "supervisor"
    });
    
    console.log(`Initial Response (${response1.data.source}):`);
    console.log(response1.data.response.substring(0, 300) + '...');
    
    // Follow-up question
    const response2 = await axios.post(`${AGENT_URL}/chat`, {
      message: "What if the temperature exceeds 60°C in our waste processing facility?",
      conversationId: "test-chat-1", // Same conversation
      facilityContext: "waste-processing-1"
    });
    
    console.log(`\nFollow-up Response:`);
    console.log(response2.data.response.substring(0, 300) + '...');
    
    return { initial: response1.data, followUp: response2.data };
  }

  async testEmergencyResponse() {
    const response = await axios.post(`${AGENT_URL}/emergency/energy-gen-1`, {
      emergencyType: "TOXIC_GAS_LEAK",
      description: "High levels of hydrogen sulfide detected in processing area",
      conversationId: "emergency-test-1"
    });
    
    const data = response.data;
    console.log(`Emergency ID: ${data.emergency.id}`);
    console.log(`Severity: ${data.emergency.severity}`);
    console.log(`Contact Authorities: ${data.contactAuthorities ? 'YES' : 'NO'}`);
    console.log(`Estimated Cost: ${data.estimatedCost}`);
    console.log(`Response Deadline: ${new Date(data.responseDeadline).toLocaleString()}`);
    console.log(`Immediate Actions: ${data.immediateActions.length} items`);
    
    return data;
  }

  async testMaintenanceScheduling() {
    const response = await axios.get(`${AGENT_URL}/maintenance/water-treatment-1`);
    const data = response.data;
    
    console.log(`Facility: ${data.facilityId}`);
    console.log(`Current Risk: ${data.currentRisk}/10 (${data.urgency})`);
    console.log(`Last Maintenance: ${data.lastMaintenance}`);
    console.log(`Maintenance Recommendations:`);
    
    data.recommendations.forEach((rec, index) => {
      console.log(`  ${index + 1}. ${rec.task} (${rec.priority})`);
      console.log(`     Deadline: ${new Date(rec.deadline).toLocaleString()}`);
      console.log(`     Duration: ${rec.estimatedDuration}`);
      console.log(`     Cost: ${rec.cost}`);
    });
    
    return data;
  }

  async testComplianceStatus() {
    const response = await axios.get(`${AGENT_URL}/compliance/waste-processing-1`);
    const data = response.data;
    
    console.log(`Facility: ${data.facilityId}`);
    console.log(`Overall Status: ${data.overallStatus}`);
    console.log(`Required Reporting: ${data.requiredReporting ? 'YES' : 'NO'}`);
    console.log(`Next Inspection: ${data.nextInspection}`);
    
    console.log(`Regulation Compliance:`);
    Object.entries(data.regulations).forEach(([reg, status]) => {
      const statusIcon = status === 'COMPLIANT' ? '✅' : 
                        status === 'WARNING' ? '⚠️' : '❌';
      console.log(`  ${statusIcon} ${reg}: ${status}`);
    });
    
    if (data.violations.length > 0) {
      console.log(`Active Violations: ${data.violations.join(', ')}`);
    }
    
    return data;
  }

  async testCostAnalysis() {
    const response = await axios.get(`${AGENT_URL}/cost-analysis/energy-gen-1`);
    const data = response.data;
    
    console.log(`Facility: ${data.facilityId}`);
    console.log(`Current Operating Cost: ${data.currentOperatingCost}`);
    console.log(`Risk Impact Cost: ${data.riskImpactCost}`);
    console.log(`Efficiency Rating: ${data.efficiencyRating}%`);
    console.log(`Potential Savings: ${data.potentialSavings}`);
    console.log(`Payback Period: ${data.paybackPeriod}`);
    
    if (data.optimizationOpportunities.length > 0) {
      console.log(`Optimization Opportunities:`);
      data.optimizationOpportunities.forEach((opp, index) => {
        console.log(`  ${index + 1}. ${opp.opportunity}`);
        console.log(`     Investment: ${opp.investmentRequired}`);
        console.log(`     Annual Savings: ${opp.annualSavings || 'Risk reduction'}`);
      });
    }
    
    return data;
  }

  async testAlertSystem() {
    // First generate some alerts by checking facilities
    await axios.get(`${AGENT_URL}/facility/water-treatment-1`);
    await axios.get(`${AGENT_URL}/facility/waste-processing-1`);
    await axios.get(`${AGENT_URL}/facility/energy-gen-1`);
    
    // Get all alerts
    const response = await axios.get(`${AGENT_URL}/alerts`);
    const data = response.data;
    
    console.log(`Total Alerts: ${data.total}`);
    console.log(`Active Facilities with Alerts: ${data.facilities.length}`);
    
    if (data.alerts.length > 0) {
      console.log(`Recent Alerts:`);
      data.alerts.slice(0, 3).forEach((alert, index) => {
        console.log(`  ${index + 1}. ${alert.message} (${alert.severity})`);
        console.log(`     Facility: ${alert.facilityId}`);
        console.log(`     Time: ${new Date(alert.timestamp).toLocaleString()}`);
      });
    }
    
    return data;
  }

  async testPerformance() {
    const tests = [
      () => axios.get(`${AGENT_URL}/health`),
      () => axios.get(`${AGENT_URL}/facilities`),
      () => axios.get(`${AGENT_URL}/facility/water-treatment-1`),
      () => axios.post(`${AGENT_URL}/chat`, { message: "Status update please" })
    ];
    
    const results = [];
    
    for (let i = 0; i < tests.length; i++) {
      const startTime = Date.now();
      await tests[i]();
      const duration = Date.now() - startTime;
      results.push(duration);
    }
    
    const avgResponseTime = results.reduce((a, b) => a + b, 0) / results.length;
    console.log(`Response Times: ${results.join('ms, ')}ms`);
    console.log(`Average Response Time: ${avgResponseTime.toFixed(1)}ms`);
    
    return { individual: results, average: avgResponseTime };
  }

  async runAllTests() {
    console.log('🚀 ChainSync Enterprise Agent - Comprehensive Test Suite');
    console.log('='.repeat(80));
    
    const startTime = Date.now();
    
    // Core functionality tests
    await this.runTest('Facility List', () => this.testFacilityList());
    await this.runTest('Facility Analysis', () => this.testFacilityAnalysis());
    await this.runTest('AI Analysis', () => this.testAIAnalysis());
    await this.runTest('Chat Conversation', () => this.testChatConversation());
    
    // Advanced feature tests
    await this.runTest('Emergency Response', () => this.testEmergencyResponse());
    await this.runTest('Maintenance Scheduling', () => this.testMaintenanceScheduling());
    await this.runTest('Compliance Status', () => this.testComplianceStatus());
    await this.runTest('Cost Analysis', () => this.testCostAnalysis());
    await this.runTest('Alert System', () => this.testAlertSystem());
    
    // Performance test
    await this.runTest('Performance Metrics', () => this.testPerformance());
    
    const totalTime = Date.now() - startTime;
    
    // Summary
    console.log('\n📊 TEST SUMMARY');
    console.log('='.repeat(80));
    
    const passed = this.results.filter(r => r.status === 'PASSED').length;
    const failed = this.results.filter(r => r.status === 'FAILED').length;
    
    console.log(`✅ Passed: ${passed}`);
    console.log(`❌ Failed: ${failed}`);
    console.log(`⏱️  Total Time: ${totalTime}ms`);
    console.log(`🎯 Success Rate: ${((passed / this.results.length) * 100).toFixed(1)}%`);
    
    if (failed === 0) {
      console.log('\n🎉 ALL TESTS PASSED! ChainSync Enterprise Agent is ready for production.');
    } else {
      console.log('\n⚠️  Some tests failed. Please review the errors above.');
    }
    
    return {
      passed,
      failed,
      totalTime,
      successRate: (passed / this.results.length) * 100,
      results: this.results
    };
  }
}

// Run tests if called directly
if (require.main === module) {
  const tester = new EnterpriseAgentTester();
  tester.runAllTests().then(results => {
    process.exit(results.failed > 0 ? 1 : 0);
  }).catch(error => {
    console.error('Test suite failed:', error);
    process.exit(1);
  });
}

module.exports = { EnterpriseAgentTester };