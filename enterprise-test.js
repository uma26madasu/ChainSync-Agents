// enterprise-test.js - Comprehensive test suite for ChainSync Unified Agent v2.0
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
    const data = response.data;
    
    console.log(`Found ${data.total} facilities:`);
    data.facilities.forEach(facility => {
      console.log(`  - ${facility.id} (${facility.type}) [${facility.domain}]`);
    });
    console.log(`Cross-Domain Enabled: ${data.crossDomainEnabled ? 'YES' : 'NO'}`);
    console.log(`Available Domains: ${Object.keys(data.domains).join(', ')}`);
    
    return data;
  }

  async testFacilityAnalysis() {
    const response = await axios.get(`${AGENT_URL}/facility/water-treatment-1`);
    const data = response.data;
    
    console.log(`Facility: ${data.facility.facilityId}`);
    console.log(`Type: ${data.facility.facilityType}`);
    console.log(`Domain: ${data.facility.domain}`);
    console.log(`Risk Level: ${data.risk.level} (${data.risk.score}/10)`);
    console.log(`Risk Factors: ${data.risk.factors.join(', ') || 'None'}`);
    console.log(`Alert Status: ${data.alert ? data.alert.severity : 'No active alerts'}`);
    console.log(`Cross-Domain Impacts: ${data.crossDomainImpacts?.length || 0}`);
    console.log(`ChainSync Integration: ${data.chainSyncIntegration ? 'ENABLED' : 'DISABLED'}`);
    
    if (data.facility.parameters) {
      console.log('Real-Time Parameters:');
      Object.entries(data.facility.parameters).forEach(([key, value]) => {
        console.log(`  - ${key}: ${typeof value === 'number' ? value.toFixed(2) : value}`);
      });
    }
    
    if (data.crossDomainImpacts?.length > 0) {
      console.log('Cross-Domain Impact Analysis:');
      data.crossDomainImpacts.forEach((impact, i) => {
        console.log(`  ${i + 1}. ${impact.domain}: ${impact.impact} (${impact.priority})`);
      });
    }
    
    return data;
  }

  async testAIAnalysisWithDomain() {
    const response = await axios.post(`${AGENT_URL}/analyze/waste-processing-1`, {
      question: "What are the current environmental risks and what cross-domain actions should we take considering potential impacts on logistics and maintenance?",
      conversationId: "test-analysis-unified"
    });
    
    const data = response.data;
    console.log(`Facility: ${data.facilityData.facilityId}`);
    console.log(`Domain: ${data.facilityData.domain}`);
    console.log(`Risk Assessment: ${data.riskAssessment.level} (${data.riskAssessment.score}/10)`);
    console.log(`AI Analysis Source: ${data.aiAnalysis.source}`);
    console.log(`Cross-Domain Impacts: ${data.crossDomainImpacts?.length || 0}`);
    console.log(`AI Response Preview: ${data.aiAnalysis.response.substring(0, 200)}...`);
    console.log(`Recommendations: ${data.recommendations.length} items`);
    console.log(`ChainSync Integration: ${data.chainSyncIntegration ? 'ENABLED' : 'DISABLED'}`);
    
    return data;
  }

  async testDomainSpecificAnalysis() {
    const domains = ['environmental', 'logistics', 'maintenance', 'compliance', 'emergency'];
    const results = {};
    
    for (const domain of domains) {
      console.log(`\nTesting ${domain.toUpperCase()} domain:`);
      
      const response = await axios.post(`${AGENT_URL}/api/${domain}/analyze`, {
        message: `Analyze current ${domain} status and provide optimization recommendations`,
        conversationId: `domain-test-${domain}`,
        facilityId: this.getFacilityForDomain(domain)
      });
      
      const data = response.data;
      console.log(`  Domain: ${data.domain}`);
      console.log(`  Analysis: ${data.analysis.response.substring(0, 100)}...`);
      console.log(`  Cross-Domain Impacts: ${data.crossDomainImpacts?.length || 0}`);
      
      results[domain] = data;
    }
    
    return results;
  }

  async testChatConversation() {
    // Start conversation with general question
    const response1 = await axios.post(`${AGENT_URL}/chat`, {
      message: "What should I monitor for critical conditions across all my facilities?",
      conversationId: "test-chat-unified"
    });
    
    console.log(`Initial Response (${response1.data.domain}):`);
    console.log(response1.data.response.substring(0, 300) + '...');
    
    // Follow-up with facility context
    const response2 = await axios.post(`${AGENT_URL}/chat`, {
      message: "What if methane levels exceed 8% in our waste processing facility?",
      conversationId: "test-chat-unified", // Same conversation
      facilityContext: "waste-processing-1"
    });
    
    console.log(`\nContextual Response (${response2.data.domain}):`);
    console.log(response2.data.response.substring(0, 300) + '...');
    
    // Cross-domain follow-up
    const response3 = await axios.post(`${AGENT_URL}/chat`, {
      message: "How would this emergency affect our logistics and maintenance operations?",
      conversationId: "test-chat-unified", // Same conversation
      domain: "emergency"
    });
    
    console.log(`\nCross-Domain Response (${response3.data.domain}):`);
    console.log(response3.data.response.substring(0, 300) + '...');
    
    return { initial: response1.data, contextual: response2.data, crossDomain: response3.data };
  }

  async testEmergencyResponse() {
    const response = await axios.post(`${AGENT_URL}/emergency/energy-gen-1`, {
      emergencyType: "ENVIRONMENTAL_CRISIS",
      description: "Critical emissions spike detected, potential regulatory violation and multi-facility impact"
    });
    
    const data = response.data;
    console.log(`Emergency ID: ${data.emergency.id}`);
    console.log(`Domain: ${data.emergency.domain}`);
    console.log(`Severity: ${data.emergency.severity}`);
    console.log(`Cross-Domain Impacts: ${data.crossDomainImpacts?.length || 0}`);
    console.log(`Contact Authorities: ${data.contactAuthorities ? 'YES' : 'NO'}`);
    console.log(`Estimated Cost: ${data.estimatedCost}`);
    console.log(`Response Deadline: ${new Date(data.responseDeadline).toLocaleString()}`);
    console.log(`Immediate Actions: ${data.immediateActions.length} items`);
    console.log(`ChainSync Notified: ${data.emergency.chainSyncNotified ? 'YES' : 'NO'}`);
    
    if (data.crossDomainImpacts?.length > 0) {
      console.log(`Cross-Domain Emergency Coordination:`);
      data.crossDomainImpacts.forEach((impact, i) => {
        console.log(`  ${i + 1}. ${impact.domain}: ${impact.impact}`);
      });
    }
    
    return data;
  }

  async testMaintenanceScheduling() {
    const response = await axios.get(`${AGENT_URL}/maintenance/logistics-hub-1`);
    const data = response.data;
    
    console.log(`Facility: ${data.facilityId}`);
    console.log(`Domain: ${data.domain}`);
    console.log(`Current Risk: ${data.currentRisk}/10 (${data.urgency})`);
    console.log(`Last Maintenance: ${data.lastMaintenance}`);
    console.log(`ChainSync Integration: ${data.chainSyncIntegration ? 'ENABLED' : 'DISABLED'}`);
    console.log(`Maintenance Recommendations:`);
    
    data.recommendations.forEach((rec, index) => {
      console.log(`  ${index + 1}. ${rec.task} (${rec.priority})`);
      console.log(`     Deadline: ${new Date(rec.deadline).toLocaleString()}`);
      console.log(`     Duration: ${rec.estimatedDuration}`);
      console.log(`     Cost: ${rec.cost}`);
      console.log(`     Slotify Integration: ${rec.slotifyIntegration ? 'ENABLED' : 'DISABLED'}`);
      console.log(`     Required Skills: ${rec.requiredSkills?.join(', ') || 'General'}`);
    });
    
    return data;
  }

  async testComplianceStatus() {
    const response = await axios.get(`${AGENT_URL}/compliance/waste-processing-1`);
    const data = response.data;
    
    console.log(`Facility: ${data.facilityId}`);
    console.log(`Domain: ${data.domain}`);
    console.log(`Overall Status: ${data.overallStatus}`);
    console.log(`Required Reporting: ${data.requiredReporting ? 'YES' : 'NO'}`);
    console.log(`Next Inspection: ${data.nextInspection}`);
    console.log(`ChainSync Integration: ${data.chainSyncIntegration ? 'ENABLED' : 'DISABLED'}`);
    
    console.log(`Regulation Compliance:`);
    Object.entries(data.regulations).forEach(([reg, status]) => {
      const statusIcon = status === 'COMPLIANT' ? '✅' : 
                        status === 'WARNING' ? '⚠️' : '❌';
      console.log(`  ${statusIcon} ${reg}: ${status}`);
    });
    
    if (data.violations.length > 0) {
      console.log(`Active Violations: ${data.violations.join(', ')}`);
    }
    
    if (data.actions.length > 0) {
      console.log(`Required Actions:`);
      data.actions.forEach((action, i) => {
        console.log(`  ${i + 1}. ${action.action} (Deadline: ${new Date(action.deadline).toLocaleString()})`);
      });
    }
    
    return data;
  }

  async testCostAnalysis() {
    const response = await axios.get(`${AGENT_URL}/cost-analysis/maintenance-center-1`);
    const data = response.data;
    
    console.log(`Facility: ${data.facilityId}`);
    console.log(`Domain: ${data.domain}`);
    console.log(`Current Operating Cost: ${data.currentOperatingCost}`);
    console.log(`Risk Impact Cost: ${data.riskImpactCost}`);
    console.log(`Efficiency Rating: ${data.efficiencyRating}%`);
    console.log(`Potential Savings: ${data.potentialSavings}`);
    console.log(`Payback Period: ${data.paybackPeriod}`);
    console.log(`ChainSync Integration: ${data.chainSyncIntegration ? 'ENABLED' : 'DISABLED'}`);
    
    if (data.optimizationOpportunities.length > 0) {
      console.log(`Optimization Opportunities:`);
      data.optimizationOpportunities.forEach((opp, index) => {
        console.log(`  ${index + 1}. ${opp.opportunity} (${opp.domain})`);
        console.log(`     Investment: ${opp.investmentRequired}`);
        console.log(`     Annual Savings: ${opp.annualSavings || 'Risk reduction'}`);
      });
    }

    if (data.crossDomainSavings?.length > 0) {
      console.log(`Cross-Domain Cost Opportunities:`);
      data.crossDomainSavings.forEach((saving, i) => {
        console.log(`  ${i + 1}. ${saving.domain}: ${saving.opportunity} (${saving.estimatedSavings})`);
      });
    }
    
    return data;
  }

  async testAlertSystem() {
    // Generate some alerts by checking facilities
    await axios.get(`${AGENT_URL}/facility/water-treatment-1`);
    await axios.get(`${AGENT_URL}/facility/waste-processing-1`);
    await axios.get(`${AGENT_URL}/facility/energy-gen-1`);
    
    // Get all alerts
    const response = await axios.get(`${AGENT_URL}/alerts`);
    const data = response.data;
    
    console.log(`Total Alerts: ${data.total}`);
    console.log(`Active Facilities with Alerts: ${data.facilities.length}`);
    console.log(`Cross-Domain Enabled: ${data.crossDomainEnabled ? 'YES' : 'NO'}`);
    console.log(`ChainSync Integration: ${data.chainSyncIntegration ? 'ENABLED' : 'DISABLED'}`);
    
    if (data.byDomain) {
      console.log(`Alerts by Domain:`);
      Object.entries(data.byDomain).forEach(([domain, count]) => {
        console.log(`  - ${domain}: ${count}`);
      });
    }
    
    if (data.alerts.length > 0) {
      console.log(`Recent Alerts:`);
      data.alerts.slice(0, 3).forEach((alert, index) => {
        console.log(`  ${index + 1}. ${alert.message} (${alert.severity})`);
        console.log(`     Facility: ${alert.facilityId} [${alert.domain}]`);
        console.log(`     Time: ${new Date(alert.timestamp).toLocaleString()}`);
        console.log(`     ChainSync Status: ${alert.chainSyncStatus || 'pending'}`);
      });
    }
    
    return data;
  }

  async testChainSyncIntegration() {
    // Test webhook
    const webhookResponse = await axios.post(`${AGENT_URL}/chainsync/webhook`, {
      flowId: 'TEST-ENTERPRISE-001',
      domain: 'environmental',
      source: 'MuleSoft-Test-Gateway',
      facilityId: 'water-treatment-1',
      data: {
        ph: 8.8,
        turbidity: 1.1,
        chlorine: 0.15,
        temperature: 24,
        alert: 'Parameters approaching limits'
      }
    });
    
    console.log(`Webhook Processing:`);
    console.log(`  Flow ID: ${webhookResponse.data.flowId}`);
    console.log(`  Status: ${webhookResponse.data.status}`);
    console.log(`  Domain: ${webhookResponse.data.domain}`);
    console.log(`  Cross-Domain Impacts: ${webhookResponse.data.crossDomainImpacts?.length || 0}`);
    
    // Test Slotify
    const slotifyResponse = await axios.post(`${AGENT_URL}/slotify/schedule`, {
      taskType: 'COMPLIANCE_INSPECTION',
      priority: 'HIGH',
      facilityId: 'energy-gen-1',
      context: {
        issue: 'Regulatory compliance check required',
        urgency: 'Within 48 hours'
      }
    });
    
    console.log(`\nSlotify Integration:`);
    console.log(`  Task Type: ${slotifyResponse.data.slotifyRequest.taskType}`);
    console.log(`  Priority: ${slotifyResponse.data.slotifyRequest.priority}`);
    console.log(`  Domain: ${slotifyResponse.data.slotifyRequest.domain}`);
    console.log(`  Required Skills: ${slotifyResponse.data.slotifyRequest.requiredSkills.join(', ')}`);
    
    return { webhook: webhookResponse.data, slotify: slotifyResponse.data };
  }

  async testDashboardMetrics() {
    // Test overall dashboard
    const overallResponse = await axios.get(`${AGENT_URL}/dashboard/metrics`);
    const overall = overallResponse.data;
    
    console.log(`Dashboard Metrics (All Domains):`);
    console.log(`  Timestamp: ${overall.timestamp}`);
    console.log(`  Total Facilities: ${overall.facilities.total}`);
    console.log(`  Total Alerts: ${overall.alerts.total}`);
    console.log(`  Critical Alerts: ${overall.alerts.critical}`);
    console.log(`  Last 24h Alerts: ${overall.alerts.last24h}`);
    console.log(`  Cross-Domain Alerts: ${overall.crossDomainStatus.totalCrossDomainAlerts}`);
    console.log(`  ChainSync Integration: ${overall.chainSyncIntegration ? 'ENABLED' : 'DISABLED'}`);
    
    // Test domain-specific dashboard
    const envResponse = await axios.get(`${AGENT_URL}/dashboard/metrics/environmental`);
    const env = envResponse.data;
    
    console.log(`\nEnvironmental Domain Metrics:`);
    console.log(`  Domain: ${env.domain}`);
    console.log(`  Facilities: ${env.facilities.total}`);
    console.log(`  Alerts: ${env.alerts.total}`);
    console.log(`  Performance: ${env.performance.successRate}`);
    
    return { overall, environmental: env };
  }

  async testPerformance() {
    const tests = [
      () => axios.get(`${AGENT_URL}/health`),
      () => axios.get(`${AGENT_URL}/facilities`),
      () => axios.get(`${AGENT_URL}/facility/water-treatment-1`),
      () => axios.post(`${AGENT_URL}/api/environmental/analyze`, { 
        message: "Quick status check",
        facilityId: "water-treatment-1"
      }),
      () => axios.post(`${AGENT_URL}/chat`, { 
        message: "System status update please" 
      }),
      () => axios.get(`${AGENT_URL}/dashboard/metrics`)
    ];
    
    const results = [];
    
    for (let i = 0; i < tests.length; i++) {
      const startTime = Date.now();
      await tests[i]();
      const duration = Date.now() - startTime;
      results.push(duration);
    }
    
    const avgResponseTime = results.reduce((a, b) => a + b, 0) / results.length;
    const maxResponseTime = Math.max(...results);
    const minResponseTime = Math.min(...results);
    
    console.log(`Response Times: ${results.join('ms, ')}ms`);
    console.log(`Average Response Time: ${avgResponseTime.toFixed(1)}ms`);
    console.log(`Min/Max Response Time: ${minResponseTime}ms / ${maxResponseTime}ms`);
    console.log(`Performance Rating: ${avgResponseTime < 2000 ? 'EXCELLENT' : avgResponseTime < 5000 ? 'GOOD' : 'NEEDS_IMPROVEMENT'}`);
    
    return { individual: results, average: avgResponseTime, min: minResponseTime, max: maxResponseTime };
  }

  getFacilityForDomain(domain) {
    const facilityMap = {
      environmental: 'water-treatment-1',
      logistics: 'logistics-hub-1',
      maintenance: 'maintenance-center-1',
      compliance: 'waste-processing-1',
      emergency: 'energy-gen-1'
    };
    
    return facilityMap[domain] || 'water-treatment-1';
  }

  async runAllTests() {
    console.log('🚀 ChainSync Unified Agent v2.0 - Enterprise Test Suite');
    console.log('='.repeat(80));
    
    const startTime = Date.now();
    
    // Core functionality tests
    await this.runTest('Facility List with Domains', () => this.testFacilityList());
    await this.runTest('Facility Analysis with Cross-Domain', () => this.testFacilityAnalysis());
    await this.runTest('AI Analysis with Domain Context', () => this.testAIAnalysisWithDomain());
    await this.runTest('Domain-Specific Analysis', () => this.testDomainSpecificAnalysis());
    await this.runTest('Unified Chat Conversation', () => this.testChatConversation());
    
    // Advanced feature tests
    await this.runTest('Emergency Response with Cross-Domain', () => this.testEmergencyResponse());
    await this.runTest('Maintenance Scheduling with Slotify', () => this.testMaintenanceScheduling());
    await this.runTest('Compliance Status by Domain', () => this.testComplianceStatus());
    await this.runTest('Cost Analysis with Cross-Domain', () => this.testCostAnalysis());
    await this.runTest('Alert System with Cross-Domain', () => this.testAlertSystem());
    
    // ChainSync integration tests
    await this.runTest('ChainSync Integration (Webhook + Slotify)', () => this.testChainSyncIntegration());
    await this.runTest('Dashboard Metrics by Domain', () => this.testDashboardMetrics());
    
    // Performance test
    await this.runTest('Performance & Response Times', () => this.testPerformance());
    
    const totalTime = Date.now() - startTime;
    
    // Summary
    console.log('\n📊 ENTERPRISE TEST SUMMARY');
    console.log('='.repeat(80));
    
    const passed = this.results.filter(r => r.status === 'PASSED').length;
    const failed = this.results.filter(r => r.status === 'FAILED').length;
    
    console.log(`✅ Passed: ${passed}`);
    console.log(`❌ Failed: ${failed}`);
    console.log(`⏱️  Total Time: ${totalTime}ms`);
    console.log(`🎯 Success Rate: ${((passed / this.results.length) * 100).toFixed(1)}%`);
    
    if (failed === 0) {
      console.log('\n🎉 ALL ENTERPRISE TESTS PASSED!');
      console.log('🚀 ChainSync Unified Agent v2.0 is ready for production deployment.');
      console.log('\n✅ Verified Features:');
      console.log('  • Multi-domain intelligence across 5 domains');
      console.log('  • Cross-domain impact analysis and coordination');
      console.log('  • Real-time ChainSync API integration');
      console.log('  • MuleSoft webhook processing');
      console.log('  • Slotify task scheduling and orchestration');
      console.log('  • Unified conversation context');
      console.log('  • Dashboard metrics and monitoring');
      console.log('  • Emergency response coordination');
      console.log('  • Automated compliance reporting');
      console.log('  • Cost optimization with cross-domain analysis');
    } else {
      console.log('\n⚠️  Some tests failed. Please review the errors above.');
      console.log('\nFailed Tests:');
      this.results.filter(r => r.status === 'FAILED').forEach(result => {
        console.log(`  - ${result.test}: ${result.error}`);
      });
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
    console.error('Enterprise test suite failed:', error);
    process.exit(1);
  });
}

module.exports = { EnterpriseAgentTester };
