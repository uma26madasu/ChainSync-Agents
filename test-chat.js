// test-chat.js
const axios = require('axios');

const AGENT_URL = 'http://localhost:3000';

async function testAgent() {
  console.log('🧪 Testing ChainSync Environmental Agent...\n');

  try {
    // Test 1: Get environmental data
    console.log('📊 Test 1: Getting environmental data...');
    const dataResponse = await axios.get(`${AGENT_URL}/data`);
    console.log('Environmental Data:', JSON.stringify(dataResponse.data, null, 2));
    console.log('\n---\n');

    // Test 2: Simple chat
    console.log('💬 Test 2: Chatting with agent...');
    const chatResponse = await axios.post(`${AGENT_URL}/chat`, {
      message: "What should I monitor for air quality safety?",
      conversationId: "test-session-1"
    });
    console.log('Agent Response:', chatResponse.data.response);
    console.log('Source:', chatResponse.data.source);
    console.log('\n---\n');

    // Test 3: Environmental analysis
    console.log('🔍 Test 3: Environmental analysis...');
    const analysisResponse = await axios.post(`${AGENT_URL}/analyze`, {
      location: "water-treatment-facility",
      conversationId: "test-session-2"
    });
    console.log('Risk Level:', analysisResponse.data.riskLevel);
    console.log('Risk Score:', analysisResponse.data.riskScore + '/10');
    console.log('Analysis:', analysisResponse.data.analysis);
    console.log('\n---\n');

    // Test 4: Follow-up question
    console.log('🔄 Test 4: Follow-up question...');
    const followUpResponse = await axios.post(`${AGENT_URL}/chat`, {
      message: "What immediate actions should we take if the risk becomes CRITICAL?",
      conversationId: "test-session-2" // Same conversation
    });
    console.log('Follow-up Response:', followUpResponse.data.response);

    console.log('\n✅ All tests completed successfully!');

  } catch (error) {
    console.error('❌ Test failed:', error.response?.data || error.message);
  }
}

// Run the tests
testAgent();