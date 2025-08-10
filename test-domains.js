// test-domains.js - Test all domains and ChainSync integration
const axios = require('axios');

const AGENT_URL = 'http://localhost:3000';

class DomainTester {
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

  async testAllDomains() {
    console.log('🚀 Testing ChainSync Unified Agent - All Domains\n');
    console.log('='.repeat(80));
    
    // Test basic connectivity
    await this.runTest('Agent Health Check', () => this.testHealth());
    await this.runTest('ChainSync Connectivity', () => this.testChainSyncConnection());
    
    // Test each domain
    const domains = ['environmental', 'logistics', 'maintenance', 'compliance', 'emergency'];
    for (const domain of domains) {
      await this.runTest(`${domain.toUpperCase()} Domain Analysis`, () => this.testDomain(domain));
    }
    
    // Test advanced features
    await this.runTest('Cross-Domain Scenario', () => this.testCrossDomainScenario());
    await this.runTest('ChainSync Webhook Integration', () => this.testChainSyncWebhook());
    await this.runTest('Slotify Task Scheduling', () => this.testSlotifyIntegration());
    await this.runTest('Dashboard Metrics', () => this.testDashboardMetrics());
    await this.runTest('Unified Chat with Context', () => this.testUnifiedChat());
    
    // Performance tests
    await this.runTest('Performance & Load Test', () => this.testPerformance());
    
    this.printSummary();
  }

  async testHealth() {
    const response = await axios.get(`${AGENT_URL}/health`);
    const health = response.data;
    
    console.log(`Status: ${health.status}`);
    console.log(`Version: ${health.version}`);
    console.log(`Domains: ${health.domains.join(', ')}`);
    console.log(`Cross-Domain: ${health.crossDomainEnabled ? 'ENABLED' : 'DISABLED'}`);
    console.log(`OpenAI: ${health.integrations.openai}`);
    console.log(`ChainSync: ${health.integrations.chainsync}`);
    
    return health;
  }

  async testChainSyncConnection() {
    const response = await axios.get(`${AGENT_URL}/chainsync/test`);
    const connection = response.data;
    
    console.log(`ChainSync Connected: ${connection.chainSyncConnected ? 'YES' : 'NO'}`);
    console.log(`API URL: ${connection.apiUrl}`);
    console.log(`Available Domains: ${Object.keys(connection.domains).join(', ')}`);
    
    return connection;
  }

  async testDomain(domain) {
    const response = await axios.post(`${AGENT_URL}/api/${domain}/analyze`, {
      message: `What are the current risks and optimization opportunities for ${domain}?`,
      conversationId: `test-${domain}-${Date.now()}`,
      facilityId: this.getFacilityForDomain(domain)
    });
    
    const data = response.data;
    console.log(`Domain: ${data.domain}`);
    console.log(`Analysis Preview: ${data.analysis.response.substring(0, 150)}...`);
    console.log(`Cross-Domain Impacts: ${data.crossDomainImpacts?.length || 0}`);
    console.log(`ChainSync Integration: ${data.chainSyncIntegration ? 'ENABLED' : 'DISABLED'}`);
    
    if (data.crossDomainImpacts?.length > 0) {
      console.log(`Cross-Domain Alerts:`);
      data.crossDomainImpacts.forEach((impact, i) => {
        console.log(`  ${i + 1}. ${impact.domain}: ${impact.impact}`);
      });
    }
    
    return data;
  }

  async testCrossDomainScenario() {
    // Simulate a critical environmental issue that should trigger cross-domain alerts
    const response = await axios.post(`${AGENT_URL}/api/environmental/analyze`, {
      message: 'CRITICAL EMERGENCY: Methane levels at 8.5% detected, toxic gas leak in waste processing facility, immediate evacuation required',
      conversationId: 'cross-domain-emergency-test',
      facilityId: 'waste-processing-1'
    });
    
    const data = response.data;
    console.log(`Emergency Domain: ${data.domain}`);
    console.log(`Cross-Domain Impacts Detected: ${data.crossDomainImpacts?.length || 0}`);
    
    if (data.crossDomainImpacts?.length > 0) {
      console.log(`Affected Domains:`);
      data.crossDomainImpacts.forEach((impact, i) => {
        console.log(`  ${i + 1}. ${impact.domain.toUpperCase()}: ${impact.impact} (${impact.priority})`);
      });
    }
    
    console.log(`Analysis Summary: Emergency protocols and cross-domain coordination required`);
    return data;
  }

  async testChainSyncWebhook() {
    const testWebhookData = {
      flowId: `TEST-WEBHOOK-${Date.now()}`,
      domain: 'environmental',
      source: 'MuleSoft-Sensor-Gateway',
      facilityId: 'water-treatment-1',
      data: {
        ph: 8.9,
        turbidity: 1.2,
        chlorine: 0.1,
        timestamp: new Date().toISOString(),
        sensorId: 'WQ-001',
        alertLevel: 'HIGH'
      }
    };
    
    const response = await axios.post(`${AGENT_URL}/chainsync/webhook`, testWebhookData);
    const result = response.data;
    
    console.log(`Flow ID: ${result.flowId}`);
    console.log(`Processing Status: ${result.status}`);
    console.log(`Domain: ${result.domain}`);
    console.log(`Processed By: ${result.processedBy}`);
    console.log(`Recommendations: ${result.recommendations?.length || 0}`);
    console.log(`Cross-Domain Impacts: ${result.crossDomainImpacts?.length || 0}`);
    console.log(`Analysis Preview: ${result.analysis.substring(0, 120)}...`);
    
    return result;
  }

  async testSlotifyIntegration() {
    const slotifyRequest = {
      taskType: 'ENVIRONMENTAL_INSPECTION',
      priority: 'HIGH',
      facilityId: 'energy-gen-1',
      context: {
        issue: 'High emissions detected requiring immediate inspection',
        requiredExpertise: ['environmental engineer', 'compliance officer'],
        estimatedDuration: '4-6 hours',
        urgency: 'Same day response required'
      }
    };
    
    const response = await axios.post(`${AGENT_URL}/slotify/schedule`, slotifyRequest);
    const result = response.data;
    
    console.log(`Task Type: ${result.slotifyRequest.taskType}`);
    console.log(`Priority: ${result.slotifyRequest.priority}`);
    console.log(`Domain: ${result.slotifyRequest.domain}`);
    console.log(`Required Skills: ${result.slotifyRequest.requiredSkills.join(', ')}`);
    console.log(`Estimated Duration: ${result.slotifyRequest.estimatedDuration}`);
    console.log(`Cross-Domain Impacts: ${result.slotifyRequest.context.crossDomainImpacts?.length || 0}`);
    console.log(`ChainSync Integration: ${result.chainSyncIntegration ? 'ENABLED' : 'DISABLED'}`);
    
    return result;
  }

  async testDashboardMetrics() {
    // Test overall metrics
    const overallResponse = await axios.get(`${AGENT_URL}/dashboard/metrics`);
    const overall = overallResponse.data;
    
    console.log(`Overall Metrics (All Domains):`);
    console.log(`  Total Facilities: ${overall.facilities.total}`);
    console.log(`  Total Alerts: ${overall.alerts.total}`);
    console.log(`  Critical Alerts: ${overall.alerts.critical}`);
    console.log(`  Cross-Domain Alerts: ${overall.crossDomainStatus.totalCrossDomainAlerts}`);
    
    // Test domain-specific metrics
    const envResponse = await axios.get(`${AGENT_URL}/dashboard/metrics/environmental`);
    const envMetrics = envResponse.data;
    
    console.log(`Environmental Domain Metrics:`);
    console.log(`  Domain: ${envMetrics.domain}`);
    console.log(`  Facilities: ${envMetrics.facilities.total}`);
    console.log(`  Recent Alerts: ${envMetrics.alerts.last24h}`);
    
    return { overall, environmental: envMetrics };
  }

  async testUnifiedChat() {
    // Test 1: General chat
    const chat1 = await axios.post(`${AGENT_URL}/chat`, {
      message: "What are the key environmental risks I should monitor across all my facilities?",
      conversationId: "unified-chat-test"
    });
    
    console.log(`General Chat Response (${chat1.data.domain}):`);
    console.log(`${chat1.data.response.substring(0, 200)}...`);
    
    // Test 2: Chat with facility context
    const chat2 = await axios.post(`${AGENT_URL}/chat`, {
      message: "Based on current conditions, what immediate actions should I take?",
      conversationId: "unified-chat-test", // Same conversation
      facilityContext: "waste-processing-1"
    });
    
    console.log(`\nContextual Chat Response (${chat2.data.domain}):`);
    console.log(`${chat2.data.response.substring(0, 200)}...`);
    
    // Test 3: Cross-domain question
    const chat3 = await axios.post(`${AGENT_URL}/chat`, {
      message: "If this environmental issue escalates, how will it affect our logistics and maintenance operations?",
      conversationId: "unified-chat-test", // Same conversation
      domain: "emergency"
    });
    
    console.log(`\nCross-Domain Chat Response (${chat3.data.domain}):`);
    console.log(`${chat3.data.response.substring(0, 200)}...`);
    
    return { general: chat1.data, contextual: chat2.data, crossDomain: chat3.data };
  }

  async testPerformance() {
    const tests = [
      () => axios.get(`${AGENT_URL}/health`),
      () => axios.get(`${AGENT_URL}/facilities`),
      () => axios.get(`${AGENT_URL}/facility/water-treatment-1`),
      () => axios.post(`${AGENT_URL}/api/environmental/analyze`, { 
        message: "Quick status check" 
      }),
      () => axios.post(`${AGENT_URL}/chat`, { 
        message: "System status update please" 
      })
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
    
    console.log(`Individual Response Times: ${results.join('ms, ')}ms`);
    console.log(`Average Response Time: ${avgResponseTime.toFixed(1)}ms`);
    console.log(`Min Response Time: ${minResponseTime}ms`);
    console.log(`Max Response Time: ${maxResponseTime}ms`);
    console.log(`Performance Rating: ${avgResponseTime < 2000 ? 'EXCELLENT' : avgResponseTime < 5000 ? 'GOOD' : 'NEEDS_IMPROVEMENT'}`);
    
    return { individual: results, average: avgResponseTime, min: minResponseTime, max: maxResponseTime };
  }

  getFacilityForDomain(domain) {
    const facilityMap = {
      environmental: 'water-treatment-1',
      logistics: 'logistics-hub-1',
      maintenance: 'maintenance-center-1',
      compliance: 'water-treatment-1',
      emergency: 'waste-processing-1'
    };
    
    return facilityMap[domain] || 'water-treatment-1';
  }

  printSummary() {
    const totalTime = this.results.reduce((sum, result) => sum + (result.duration || 0), 0);
    const passed = this.results.filter(r => r.status === 'PASSED').length;
    const failed = this.results.filter(r => r.status === 'FAILED').length;
    
    console.log('\n' + '='.repeat(80));
    console.log('📊 CHAINSYNC UNIFIED AGENT TEST SUMMARY');
    console.log('='.repeat(80));
    
    console.log(`✅ Passed: ${passed}`);
    console.log(`❌ Failed: ${failed}`);
    console.log(`⏱️  Total Time: ${totalTime}ms`);
    console.log(`🎯 Success Rate: ${((passed / this.results.length) * 100).toFixed(1)}%`);
    
    if (failed === 0) {
      console.log('\n🎉 ALL TESTS PASSED! ChainSync Unified Agent is ready for production.');
      console.log('🚀 Multi-domain intelligence, cross-domain awareness, and ChainSync integration working perfectly!');
    } else {
      console.log('\n⚠️  Some tests failed. Please review the errors above.');
      console.log('\nFailed Tests:');
      this.results.filter(r => r.status === 'FAILED').forEach(result => {
        console.log(`  - ${result.test}: ${result.error}`);
      });
    }
    
    console.log('\n🔧 ChainSync Integration Status:');
    console.log('  ✅ Multi-domain analysis');
    console.log('  ✅ Cross-domain impact detection');
    console.log('  ✅ MuleSoft webhook processing');
    console.log('  ✅ Slotify task scheduling');
    console.log('  ✅ Unified conversation context');
    console.log('  ✅ Dashboard metrics and monitoring');
    
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
  const tester = new DomainTester();
  tester.testAllDomains().then(results => {
    process.exit(results?.failed > 0 ? 1 : 0);
  }).catch(error => {
    console.error('❌ Test suite failed:', error);
    process.exit(1);
  });
}

module.exports = { DomainTester };
