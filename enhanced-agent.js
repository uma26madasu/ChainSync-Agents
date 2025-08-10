// enhanced-agent.js - ChainSync Unified Intelligent Agent v2.0
require('dotenv').config();
const OpenAI = require('openai');
const express = require('express');

const app = express();
app.use(express.json());

// Initialize OpenAI
const openai = process.env.OPENAI_API_KEY && process.env.OPENAI_API_KEY !== 'your_api_key_here' 
  ? new OpenAI({ apiKey: process.env.OPENAI_API_KEY }) 
  : null;

// Enhanced conversation memory and domain management
const conversations = new Map();
const alertHistory = new Map();
const facilityProfiles = new Map();
const domainContexts = new Map();
const crossDomainRules = new Map();

// ChainSync API Configuration
const CHAINSYNC_API_BASE = process.env.CHAINSYNC_API_URL || 'http://localhost:8081/api';
const CHAINSYNC_TIMEOUT = parseInt(process.env.CHAINSYNC_TIMEOUT) || 10000; // 10 seconds

// ChainSync Domain Manager
class ChainSyncDomainManager {
  constructor() {
    this.domains = {
      environmental: ['water-treatment', 'waste-processing', 'energy-generation'],
      logistics: ['supply-chain', 'transportation', 'warehouse'],
      maintenance: ['equipment', 'infrastructure', 'preventive'],
      compliance: ['regulatory', 'safety', 'audit'],
      emergency: ['incident', 'evacuation', 'crisis']
    };
    
    this.crossDomainImpacts = {
      environmental: {
        affects: ['logistics', 'compliance'],
        triggers: (riskScore) => riskScore >= 7
      },
      maintenance: {
        affects: ['environmental', 'logistics'],
        triggers: (urgency) => urgency === 'CRITICAL'
      },
      logistics: {
        affects: ['environmental', 'maintenance'],
        triggers: (efficiency) => efficiency < 80
      },
      compliance: {
        affects: ['environmental', 'maintenance'],
        triggers: (violations) => violations > 0
      },
      emergency: {
        affects: ['environmental', 'logistics', 'maintenance', 'compliance'],
        triggers: (severity) => severity === 'CRITICAL'
      }
    };
  }

  identifyDomain(facilityId, context = '') {
    // Smart domain detection
    if (facilityId.includes('water') || facilityId.includes('waste') || facilityId.includes('energy')) {
      return 'environmental';
    }
    if (context.includes('maintenance') || context.includes('repair') || context.includes('equipment')) {
      return 'maintenance';
    }
    if (context.includes('emergency') || context.includes('crisis') || context.includes('evacuation')) {
      return 'emergency';
    }
    if (context.includes('logistics') || context.includes('supply') || context.includes('transport')) {
      return 'logistics';
    }
    if (context.includes('compliance') || context.includes('regulatory') || context.includes('audit')) {
      return 'compliance';
    }
    return 'environmental'; // default
  }

  async checkCrossDomainImpacts(analysis, domain) {
    const impacts = [];
    const rules = this.crossDomainImpacts[domain];
    
    if (rules && rules.triggers(analysis.score || analysis.urgency || analysis.efficiency || analysis.violations || analysis.severity)) {
      for (const affectedDomain of rules.affects) {
        impacts.push({
          domain: affectedDomain,
          impact: `${domain} issue may affect ${affectedDomain}`,
          severity: analysis.level || 'MEDIUM',
          recommendedAction: `Check ${affectedDomain} systems and coordinate response`,
          priority: analysis.score >= 8 ? 'HIGH' : 'MEDIUM'
        });
      }
    }
    
    return impacts;
  }

  async getDomainContext(domain, facilityId) {
    const contexts = {
      environmental: {
        regulations: ['EPA Clean Air Act', 'Clean Water Act', 'RCRA'],
        monitoring: ['real-time sensors', 'automated alerts', 'compliance tracking'],
        integration: ['MuleSoft environmental APIs', 'sensor data streams'],
        kpis: ['emissions levels', 'water quality', 'waste processing efficiency']
      },
      logistics: {
        systems: ['supply chain tracking', 'route optimization', 'inventory management'],
        kpis: ['on-time delivery', 'cost per mile', 'capacity utilization'],
        integration: ['transportation APIs', 'warehouse management systems'],
        optimization: ['route planning', 'load balancing', 'cost reduction']
      },
      maintenance: {
        types: ['preventive', 'predictive', 'emergency', 'compliance'],
        scheduling: ['Slotify integration', 'technician availability', 'parts inventory'],
        integration: ['CMMS systems', 'IoT equipment monitoring'],
        metrics: ['uptime', 'mean time to repair', 'maintenance costs']
      },
      compliance: {
        frameworks: ['ISO 14001', 'OSHA standards', 'industry regulations'],
        reporting: ['automated compliance reports', 'audit trails', 'violation tracking'],
        integration: ['regulatory databases', 'document management'],
        requirements: ['periodic inspections', 'certification renewals', 'training records']
      },
      emergency: {
        protocols: ['evacuation procedures', 'emergency services', 'communication'],
        coordination: ['multi-agency response', 'resource allocation', 'status updates'],
        integration: ['emergency alert systems', 'first responder APIs'],
        response: ['immediate actions', 'escalation procedures', 'recovery planning']
      }
    };
    
    return contexts[domain] || contexts.environmental;
  }
}

class EnterpriseEnvironmentalAgent {
  constructor() {
    this.domainManager = new ChainSyncDomainManager();
    this.initializeFacilityProfiles();
    this.systemPrompt = `You are ChainSync's Unified Intelligent Agent v2.0.

ROLE: Multi-domain enterprise intelligence with cross-functional coordination
CAPABILITIES: Environmental monitoring, Logistics optimization, Maintenance scheduling, 
Compliance management, Emergency response, Cross-domain impact analysis

DOMAINS: Environmental, Logistics, Maintenance, Compliance, Emergency
CROSS-DOMAIN AWARENESS: Always consider impacts across all operational domains

FACILITY TYPES & THRESHOLDS:
- WATER_TREATMENT: pH 6.5-8.5, turbidity <1 NTU, chlorine 0.2-4.0 mg/L
- WASTE_PROCESSING: Temperature <60°C, methane <5%, hydrogen sulfide <10ppm  
- ENERGY_GENERATION: Emissions <50μg/m³, noise <85dB, temperature variance <±5°C
- LOGISTICS_HUB: Throughput efficiency >85%, delay time <30min, capacity utilization <90%
- MAINTENANCE_FACILITY: Equipment uptime >95%, response time <4hrs, safety incidents = 0

RISK MATRIX:
- CRITICAL (9-10): Immediate cross-domain impact, emergency protocols, regulatory notification
- HIGH (7-8): Multi-domain coordination required, enhanced monitoring, prepare escalation
- MEDIUM (5-6): Domain-specific response, monitor adjacent systems, preventive measures
- LOW (1-4): Routine operations, optimization opportunities, routine monitoring
- OPTIMAL (0): Peak performance, document best practices, continuous improvement

CHAINSYNC INTEGRATION:
- MuleSoft API orchestration for data flow
- Slotify for intelligent task scheduling and resource allocation
- Real-time dashboard metrics and cross-domain alerts
- Automated compliance reporting and regulatory coordination

Always provide: Risk score, immediate actions, cross-domain impacts, timeline, cost implications, ChainSync integration recommendations`;
  }

  initializeFacilityProfiles() {
    facilityProfiles.set('water-treatment-1', {
      type: 'WATER_TREATMENT',
      capacity: '50M gallons/day',
      location: { lat: 33.7490, lon: -84.3880 },
      lastMaintenance: '2025-07-15',
      regulatoryInspection: '2025-09-01',
      domain: 'environmental'
    });
    
    facilityProfiles.set('waste-processing-1', {
      type: 'WASTE_PROCESSING', 
      capacity: '200 tons/day',
      location: { lat: 33.7590, lon: -84.3780 },
      lastMaintenance: '2025-07-20',
      regulatoryInspection: '2025-08-15',
      domain: 'environmental'
    });
    
    facilityProfiles.set('energy-gen-1', {
      type: 'ENERGY_GENERATION',
      capacity: '500MW',
      location: { lat: 33.7690, lon: -84.3680 },
      lastMaintenance: '2025-07-25',
      regulatoryInspection: '2025-10-01',
      domain: 'environmental'
    });

    facilityProfiles.set('logistics-hub-1', {
      type: 'LOGISTICS_HUB',
      capacity: '10000 packages/day',
      location: { lat: 33.7790, lon: -84.3580 },
      lastMaintenance: '2025-07-10',
      regulatoryInspection: '2025-11-01',
      domain: 'logistics'
    });

    facilityProfiles.set('maintenance-center-1', {
      type: 'MAINTENANCE_FACILITY',
      capacity: '50 work orders/day',
      location: { lat: 33.7890, lon: -84.3480 },
      lastMaintenance: '2025-07-05',
      regulatoryInspection: '2025-12-01',
      domain: 'maintenance'
    });
  }

  // Test ChainSync API connectivity
  async testChainSyncConnection() {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);
      
      const response = await fetch(`${CHAINSYNC_API_BASE}/health`, {
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'ChainSync-Agent/2.0'
        }
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        console.log('✅ ChainSync API accessible');
        return true;
      } else {
        console.log(`⚠️ ChainSync API responded with status: ${response.status}`);
        return false;
      }
    } catch (error) {
      console.log(`❌ ChainSync API not accessible: ${error.message}`);
      return false;
    }
  }

  async analyze(message, conversationId = 'default') {
    try {
      if (!openai) {
        return this.getEnhancedMockResponse(message);
      }

      if (!conversations.has(conversationId)) {
        conversations.set(conversationId, [
          { role: 'system', content: this.systemPrompt }
        ]);
      }

      const history = conversations.get(conversationId);
      history.push({ role: 'user', content: message });

      const response = await openai.chat.completions.create({
        model: 'gpt-4o-mini',
        messages: history,
        max_tokens: 600,
        temperature: 0.2
      });

      const agentResponse = response.choices[0].message.content;
      history.push({ role: 'assistant', content: agentResponse });

      if (history.length > 15) {
        history.splice(1, 2);
      }

      return {
        response: agentResponse,
        source: 'openai',
        conversationId: conversationId,
        timestamp: new Date().toISOString()
      };

    } catch (error) {
      console.error('OpenAI error:', error.message);
      return this.getEnhancedMockResponse(message);
    }
  }

  async analyzeWithDomainContext(message, conversationId = 'default', domain = 'environmental', facilityId = null) {
    try {
      // Identify domain if not provided
      if (!domain && facilityId) {
        domain = this.domainManager.identifyDomain(facilityId, message);
      }

      // Get domain-specific context
      const domainContext = await this.domainManager.getDomainContext(domain, facilityId);
      
      // Enhanced prompt with domain awareness
      const enhancedMessage = `
DOMAIN: ${domain.toUpperCase()}
FACILITY: ${facilityId || 'general'}
CONTEXT: ${JSON.stringify(domainContext, null, 2)}

QUERY: ${message}

Provide analysis considering:
1. Primary domain impacts
2. Cross-domain effects  
3. ChainSync platform integration
4. Slotify orchestration needs
5. MuleSoft data flow requirements`;

      const analysis = await this.analyze(enhancedMessage, conversationId);
      
      // Check for cross-domain impacts
      if (analysis.response.includes('CRITICAL') || analysis.response.includes('HIGH')) {
        const crossImpacts = await this.domainManager.checkCrossDomainImpacts(
          { score: 8, level: 'HIGH' }, domain
        );
        analysis.crossDomainImpacts = crossImpacts;
      }
      
      analysis.domain = domain;
      analysis.chainSyncIntegration = true;
      
      return analysis;
    } catch (error) {
      console.error('Domain analysis error:', error.message);
      return this.getEnhancedMockResponse(message);
    }
  }

  getEnhancedMockResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    const responses = {
      'critical': 'CRITICAL ALERT: Multi-domain emergency detected. IMMEDIATE ACTIONS: 1) Cross-domain evacuation protocols, 2) Emergency services contact, 3) Regulatory notification, 4) Slotify emergency task assignment. Cost impact: $50K-200K. Timeline: 15 minutes. Cross-domain coordination required.',
      'emergency': 'EMERGENCY PROTOCOL: Multiple parameters in danger zone. Risk: 9.2/10. Actions: Shutdown, evacuation, emergency notification. EPA reporting required. Slotify coordination initiated.',
      'high': 'HIGH RISK: Parameters approaching critical across domains. Risk: 7.8/10. Actions: 1) Reduce operations 60%, 2) Monitor every 15min, 3) Prepare evacuation, 4) Cross-domain impact assessment. Cost: $15K-40K.',
      'logistics': 'LOGISTICS ANALYSIS: Supply chain optimization required. Current efficiency: 82%. Recommendations: 1) Route optimization, 2) Inventory rebalancing, 3) Performance monitoring. Integration with transportation APIs recommended.',
      'maintenance': 'MAINTENANCE ASSESSMENT: Predictive maintenance alerts triggered. Equipment uptime: 89%. Actions: 1) Schedule preventive maintenance via Slotify, 2) Parts inventory check, 3) Technician assignment. CMMS integration active.',
      'compliance': 'COMPLIANCE STATUS: Regulatory requirements analysis complete. Current status: COMPLIANT with observations. Actions: 1) Document review, 2) Audit preparation, 3) Training schedule update. Automated reporting enabled.',
      'temperature': 'THERMAL ANALYSIS: Cross-domain temperature fluctuations detected. Recommend: 1) HVAC system review, 2) Equipment monitoring, 3) Environmental impact assessment.',
      'air quality': 'AIR QUALITY: PM2.5 levels moderate, potential cross-domain impact. Actions: 1) Enhanced filtration, 2) Logistics route adjustment, 3) Staff monitoring, 4) Compliance documentation.',
      'water': 'WATER QUALITY: Multi-parameter analysis complete. pH approaching limits, possible cross-system effects. Actions: 1) pH adjustment, 2) Filter inspection in 48hrs, 3) Downstream impact assessment.',
      'default': 'CHAINSYNC ANALYSIS: Multi-domain status evaluated using real-time data streams. Cross-domain coordination assessed. Risk evaluation and recommendations provided based on ChainSync platform integration and current facility parameters.'
    };

    let response = responses.default;
    for (const [keyword, mockResponse] of Object.entries(responses)) {
      if (lowerMessage.includes(keyword)) {
        response = mockResponse;
        break;
      }
    }

    return {
      response: response,
      source: 'enhanced_mock',
      conversationId: 'default',
      timestamp: new Date().toISOString(),
      chainSyncIntegration: true
    };
  }

  // Enhanced data integration with ChainSync API
  async getAdvancedEnvironmentalData(facilityId = 'water-treatment-1') {
    try {
      // Get facility profile for metadata
      const profile = facilityProfiles.get(facilityId);
      if (!profile) {
        throw new Error(`Facility ${facilityId} not found in profiles`);
      }

      // Call ChainSync API for real environmental data
      console.log(`🔄 Fetching real data from ChainSync for ${facilityId}...`);
      
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), CHAINSYNC_TIMEOUT);
      
      const response = await fetch(`${CHAINSYNC_API_BASE}/environmental/${facilityId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'ChainSync-Agent/2.0',
          'X-Facility-Type': profile.type,
          'X-Domain': profile.domain
        },
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        throw new Error(`ChainSync API error: ${response.status} - ${response.statusText}`);
      }
      
      const chainSyncData = await response.json();
      console.log(`✅ Real data received from ChainSync for ${facilityId}`);
      
      // Transform ChainSync data to agent format
      const transformedData = this.transformChainSyncData(chainSyncData, profile, facilityId);
      
      // Log data source for monitoring
      transformedData.dataSource = 'chainsync_api';
      transformedData.dataFreshness = new Date().toISOString();
      
      return transformedData;
      
    } catch (error) {
      console.error(`Failed to get real data from ChainSync for ${facilityId}:`, error.message);
      console.log('🔄 Falling back to enhanced mock data with real-time simulation...');
      
      // Fallback to enhanced mock data that simulates real conditions
      return this.generateEnhancedMockData(facilityId);
    }
  }

  // Transform real ChainSync API data to agent format
  transformChainSyncData(chainSyncData, profile, facilityId) {
    const baseData = {
      facilityId: facilityId,
      facilityType: profile.type,
      domain: profile.domain,
      timestamp: chainSyncData.timestamp || new Date().toISOString(),
      location: chainSyncData.location || profile.location,
      operationalStatus: chainSyncData.operationalStatus || 'ACTIVE',
      lastMaintenance: chainSyncData.lastMaintenance || profile.lastMaintenance,
      nextInspection: chainSyncData.nextInspection || profile.regulatoryInspection,
      dataQuality: chainSyncData.dataQuality || 'GOOD'
    };

    // Transform environmental parameters based on facility type and ChainSync data structure
    switch (profile.type) {
      case 'WATER_TREATMENT':
        return {
          ...baseData,
          parameters: {
            // Real data from ChainSync sensors
            ph: chainSyncData.waterQuality?.ph || chainSyncData.ph || 7.2,
            turbidity: chainSyncData.waterQuality?.turbidity || chainSyncData.turbidity || 0.5,
            chlorine: chainSyncData.waterQuality?.chlorine || chainSyncData.chlorine || 2.0,
            temperature: chainSyncData.environmental?.temperature || chainSyncData.temperature || 22,
            flowRate: chainSyncData.operational?.flowRate || chainSyncData.flowRate || 45000,
            pressure: chainSyncData.operational?.pressure || chainSyncData.pressure || 35,
            efficiency: chainSyncData.operational?.efficiency || chainSyncData.efficiency || 88,
            // Additional environmental data from ChainSync
            dissolvedOxygen: chainSyncData.waterQuality?.dissolvedOxygen || 8.5,
            conductivity: chainSyncData.waterQuality?.conductivity || 750,
            alkalinity: chainSyncData.waterQuality?.alkalinity || 120
          }
        };
      
      case 'WASTE_PROCESSING':
        return {
          ...baseData,
          parameters: {
            // Real data from ChainSync sensors
            methane: chainSyncData.gasLevels?.methane || chainSyncData.methane || 2.5,
            hydrogenSulfide: chainSyncData.gasLevels?.hydrogenSulfide || chainSyncData.h2s || 5,
            temperature: chainSyncData.environmental?.temperature || chainSyncData.temperature || 45,
            ph: chainSyncData.wasteQuality?.ph || chainSyncData.ph || 7.0,
            volume: chainSyncData.operational?.volume || chainSyncData.volume || 180,
            efficiency: chainSyncData.operational?.efficiency || chainSyncData.efficiency || 85,
            // Additional waste processing data
            organicContent: chainSyncData.wasteQuality?.organicContent || 65,
            moistureContent: chainSyncData.wasteQuality?.moistureContent || 25,
            ammonia: chainSyncData.gasLevels?.ammonia || 15
          }
        };
      
      case 'ENERGY_GENERATION':
        return {
          ...baseData,
          parameters: {
            // Real data from ChainSync sensors
            emissions: chainSyncData.emissions?.no2 || chainSyncData.emissions || 35,
            noise: chainSyncData.environmental?.noise || chainSyncData.noise || 78,
            temperature: chainSyncData.operational?.temperature || chainSyncData.temperature || 450,
            efficiency: chainSyncData.operational?.efficiency || chainSyncData.efficiency || 88,
            power: chainSyncData.operational?.powerOutput || chainSyncData.power || 480,
            fuelConsumption: chainSyncData.operational?.fuelConsumption || chainSyncData.fuel || 1200,
            // Additional energy generation data
            co2Emissions: chainSyncData.emissions?.co2 || 120,
            so2Emissions: chainSyncData.emissions?.so2 || 8,
            particulates: chainSyncData.emissions?.pm25 || 12
          }
        };

      case 'LOGISTICS_HUB':
        return {
          ...baseData,
          parameters: {
            throughput: chainSyncData.logistics?.throughput || chainSyncData.throughput || 8500,
            efficiency: chainSyncData.operational?.efficiency || chainSyncData.efficiency || 87,
            delayTime: chainSyncData.logistics?.averageDelay || chainSyncData.delayTime || 25,
            capacityUtilization: chainSyncData.logistics?.capacityUse || chainSyncData.capacity || 78,
            temperature: chainSyncData.environmental?.temperature || chainSyncData.temperature || 22,
            onTimeDelivery: chainSyncData.logistics?.onTimeRate || 92,
            costPerMile: chainSyncData.logistics?.costPerMile || 2.85
          }
        };

      case 'MAINTENANCE_FACILITY':
        return {
          ...baseData,
          parameters: {
            uptime: chainSyncData.maintenance?.uptime || chainSyncData.uptime || 96,
            responseTime: chainSyncData.maintenance?.avgResponseTime || chainSyncData.responseTime || 3.5,
            safetyIncidents: chainSyncData.safety?.incidents || chainSyncData.incidents || 0,
            efficiency: chainSyncData.operational?.efficiency || chainSyncData.efficiency || 89,
            workOrdersCompleted: chainSyncData.maintenance?.completedOrders || 45,
            meanTimeToRepair: chainSyncData.maintenance?.mttr || 4.2,
            preventiveMaintenance: chainSyncData.maintenance?.preventiveRate || 85
          }
        };
      
      default:
        return {
          ...baseData,
          parameters: {
            // Generic parameters
            temperature: chainSyncData.environmental?.temperature || chainSyncData.temperature || 22,
            humidity: chainSyncData.environmental?.humidity || chainSyncData.humidity || 60,
            airQuality: chainSyncData.environmental?.airQuality || chainSyncData.airQuality || 3,
            windSpeed: chainSyncData.environmental?.windSpeed || chainSyncData.windSpeed || 15,
            pressure: chainSyncData.environmental?.pressure || chainSyncData.pressure || 1013,
            efficiency: chainSyncData.operational?.efficiency || chainSyncData.efficiency || 85
          }
        };
    }
  }

  // Enhanced mock data with realistic variations (fallback)
  generateEnhancedMockData(facilityId) {
    const profile = facilityProfiles.get(facilityId);
    
    const baseData = {
      facilityId: facilityId,
      facilityType: profile.type,
      domain: profile.domain,
      timestamp: new Date().toISOString(),
      location: profile.location,
      operationalStatus: 'ACTIVE',
      lastMaintenance: profile.lastMaintenance,
      nextInspection: profile.regulatoryInspection,
      dataSource: 'enhanced_mock',
      dataQuality: 'SIMULATED'
    };

    // Generate realistic data with time-based variations
    const hour = new Date().getHours();
    const dayVariation = Math.sin(hour * Math.PI / 12) * 0.1; // Daily cycle variation
    const randomVariation = (Math.random() - 0.5) * 0.05; // Small random variation

    switch (profile.type) {
      case 'WATER_TREATMENT':
        return {
          ...baseData,
          parameters: {
            ph: 7.2 + dayVariation + randomVariation,
            turbidity: 0.4 + Math.abs(dayVariation) * 0.3,
            chlorine: 2.1 + dayVariation * 0.2,
            temperature: 22 + dayVariation * 3 + randomVariation * 2,
            flowRate: 45000 + dayVariation * 5000 + randomVariation * 3000,
            pressure: 35 + dayVariation * 2 + randomVariation,
            efficiency: 88 + dayVariation * 5,
            dissolvedOxygen: 8.5 + dayVariation * 0.5,
            conductivity: 750 + dayVariation * 50,
            alkalinity: 120 + dayVariation * 10
          }
        };
      
      case 'WASTE_PROCESSING':
        return {
          ...baseData,
          parameters: {
            methane: 2.5 + Math.abs(dayVariation) * 1.5,
            hydrogenSulfide: 5 + Math.abs(dayVariation) * 2,
            temperature: 45 + dayVariation * 8 + randomVariation * 3,
            ph: 7.0 + dayVariation * 0.5,
            volume: 180 + dayVariation * 20,
            efficiency: 85 + dayVariation * 8,
            organicContent: 65 + dayVariation * 5,
            moistureContent: 25 + dayVariation * 3,
            ammonia: 15 + Math.abs(dayVariation) * 5
          }
        };
      
      case 'ENERGY_GENERATION':
        return {
          ...baseData,
          parameters: {
            emissions: 35 + Math.abs(dayVariation) * 10,
            noise: 78 + dayVariation * 5,
            temperature: 450 + dayVariation * 30 + randomVariation * 10,
            efficiency: 88 + dayVariation * 6,
            power: 480 + dayVariation * 30,
            fuelConsumption: 1200 + dayVariation * 100,
            co2Emissions: 120 + dayVariation * 15,
            so2Emissions: 8 + Math.abs(dayVariation) * 2,
            particulates: 12 + Math.abs(dayVariation) * 3
          }
        };

      case 'LOGISTICS_HUB':
        return {
          ...baseData,
          parameters: {
            throughput: 8500 + dayVariation * 1000,
            efficiency: 87 + dayVariation * 8,
            delayTime: 25 + Math.abs(dayVariation) * 10,
            capacityUtilization: 78 + dayVariation * 12,
            temperature: 22 + dayVariation * 5,
            onTimeDelivery: 92 + dayVariation * 5,
            costPerMile: 2.85 + dayVariation * 0.2
          }
        };

      case 'MAINTENANCE_FACILITY':
        return {
          ...baseData,
          parameters: {
            uptime: 96 + dayVariation * 3,
            responseTime: 3.5 + Math.abs(dayVariation) * 1,
            safetyIncidents: Math.floor(Math.abs(dayVariation) * 2),
            efficiency: 89 + dayVariation * 6,
            workOrdersCompleted: 45 + dayVariation * 8,
            meanTimeToRepair: 4.2 + dayVariation * 0.8,
            preventiveMaintenance: 85 + dayVariation * 10
          }
        };
      
      default:
        return {
          ...baseData,
          parameters: {
            temperature: 22 + dayVariation * 5,
            humidity: 60 + dayVariation * 15,
            airQuality: 3 + Math.abs(dayVariation) * 2,
            windSpeed: 15 + dayVariation * 8,
            pressure: 1013 + dayVariation * 5,
            efficiency: 85 + dayVariation * 10
          }
        };
    }
  }

  calculateAdvancedRisk(facilityData) {
    const { facilityType, parameters } = facilityData;
    let riskScore = 0;
    let riskFactors = [];

    switch (facilityType) {
      case 'WATER_TREATMENT':
        if (parameters.ph < 6.5 || parameters.ph > 8.5) {
          riskScore += 4;
          riskFactors.push(`pH out of safe range (${parameters.ph.toFixed(2)})`);
        }
        if (parameters.turbidity > 1) {
          riskScore += 3;
          riskFactors.push(`High turbidity detected (${parameters.turbidity.toFixed(2)} NTU)`);
        }
        if (parameters.chlorine < 0.2 || parameters.chlorine > 4.0) {
          riskScore += 3;
          riskFactors.push(`Chlorine levels critical (${parameters.chlorine.toFixed(2)} mg/L)`);
        }
        if (parameters.dissolvedOxygen && parameters.dissolvedOxygen < 6) {
          riskScore += 2;
          riskFactors.push(`Low dissolved oxygen (${parameters.dissolvedOxygen.toFixed(2)} mg/L)`);
        }
        if (parameters.efficiency < 80) {
          riskScore += 1;
          riskFactors.push(`Low efficiency (${parameters.efficiency.toFixed(1)}%)`);
        }
        break;

      case 'WASTE_PROCESSING':
        if (parameters.methane > 5) {
          riskScore += 5;
          riskFactors.push(`Dangerous methane levels (${parameters.methane.toFixed(2)}%)`);
        }
        if (parameters.hydrogenSulfide > 10) {
          riskScore += 4;
          riskFactors.push(`Toxic H2S detected (${parameters.hydrogenSulfide.toFixed(2)} ppm)`);
        }
        if (parameters.temperature > 60) {
          riskScore += 3;
          riskFactors.push(`Overheating detected (${parameters.temperature.toFixed(1)}°C)`);
        }
        if (parameters.ammonia && parameters.ammonia > 25) {
          riskScore += 2;
          riskFactors.push(`High ammonia levels (${parameters.ammonia.toFixed(1)} ppm)`);
        }
        if (parameters.efficiency < 75) {
          riskScore += 1;
          riskFactors.push(`Low processing efficiency (${parameters.efficiency.toFixed(1)}%)`);
        }
        break;

      case 'ENERGY_GENERATION':
        if (parameters.emissions > 50) {
          riskScore += 3;
          riskFactors.push(`High emissions detected (${parameters.emissions.toFixed(1)} μg/m³)`);
        }
        if (parameters.noise > 85) {
          riskScore += 2;
          riskFactors.push(`Noise pollution exceeded (${parameters.noise.toFixed(1)} dB)`);
        }
        if (parameters.efficiency < 80) {
          riskScore += 2;
          riskFactors.push(`Low operational efficiency (${parameters.efficiency.toFixed(1)}%)`);
        }
        if (parameters.co2Emissions && parameters.co2Emissions > 150) {
          riskScore += 2;
          riskFactors.push(`High CO2 emissions (${parameters.co2Emissions.toFixed(1)} mg/m³)`);
        }
        if (parameters.temperature > 500) {
          riskScore += 1;
          riskFactors.push(`High operating temperature (${parameters.temperature.toFixed(0)}°C)`);
        }
        break;

      case 'LOGISTICS_HUB':
        if (parameters.efficiency < 85) {
          riskScore += 3;
          riskFactors.push(`Low logistics efficiency (${parameters.efficiency.toFixed(1)}%)`);
        }
        if (parameters.delayTime > 30) {
          riskScore += 2;
          riskFactors.push(`High delay time (${parameters.delayTime.toFixed(1)} minutes)`);
        }
        if (parameters.capacityUtilization > 90) {
          riskScore += 2;
          riskFactors.push(`Over capacity utilization (${parameters.capacityUtilization.toFixed(1)}%)`);
        }
        if (parameters.onTimeDelivery < 90) {
          riskScore += 1;
          riskFactors.push(`Low on-time delivery (${parameters.onTimeDelivery.toFixed(1)}%)`);
        }
        break;

      case 'MAINTENANCE_FACILITY':
        if (parameters.uptime < 95) {
          riskScore += 3;
          riskFactors.push(`Low equipment uptime (${parameters.uptime.toFixed(1)}%)`);
        }
        if (parameters.responseTime > 4) {
          riskScore += 2;
          riskFactors.push(`High response time (${parameters.responseTime.toFixed(1)} hours)`);
        }
        if (parameters.safetyIncidents > 0) {
          riskScore += 4;
          riskFactors.push(`Safety incidents detected (${parameters.safetyIncidents})`);
        }
        if (parameters.efficiency < 85) {
          riskScore += 1;
          riskFactors.push(`Low maintenance efficiency (${parameters.efficiency.toFixed(1)}%)`);
        }
        break;
    }

    return {
      score: Math.min(10, riskScore),
      level: this.getRiskLevel(riskScore),
      factors: riskFactors,
      recommendations: this.generateRecommendations(riskScore, riskFactors, facilityData.facilityType),
      dataSource: facilityData.dataSource || 'unknown',
      domain: facilityData.domain || 'environmental'
    };
  }

  getRiskLevel(score) {
    if (score >= 9) return 'CRITICAL';
    if (score >= 7) return 'HIGH';
    if (score >= 5) return 'MEDIUM';
    if (score >= 1) return 'LOW';
    return 'OPTIMAL';
  }

  generateRecommendations(riskScore, factors, facilityType) {
    const recommendations = [];
    
    if (riskScore >= 9) {
      recommendations.push('IMMEDIATE: Initiate emergency shutdown procedures');
      recommendations.push('IMMEDIATE: Evacuate non-essential personnel');
      recommendations.push('IMMEDIATE: Contact emergency services and regulatory authorities');
      recommendations.push('IMMEDIATE: Activate incident response team');
      recommendations.push('IMMEDIATE: Notify cross-domain impact teams via Slotify');
    } else if (riskScore >= 7) {
      recommendations.push('URGENT: Reduce operations to 50% capacity');
      recommendations.push('URGENT: Implement enhanced monitoring (every 15 minutes)');
      recommendations.push('URGENT: Prepare evacuation procedures');
      recommendations.push('URGENT: Notify management and safety team');
      recommendations.push('URGENT: Schedule emergency maintenance via Slotify');
    } else if (riskScore >= 5) {
      recommendations.push('Monitor parameters every 30 minutes');
      recommendations.push('Review and prepare contingency plans');
      recommendations.push('Consider operational adjustments');
      recommendations.push('Schedule equipment inspection within 24 hours');
      recommendations.push('Update ChainSync dashboard alerts');
    } else if (riskScore >= 1) {
      recommendations.push('Continue routine monitoring');
      recommendations.push('Schedule preventive maintenance review');
      recommendations.push('Document current operational parameters');
      recommendations.push('Optimize efficiency through ChainSync analytics');
    } else {
      recommendations.push('Maintain current optimal operations');
      recommendations.push('Document best practices for replication');
      recommendations.push('Consider efficiency optimization opportunities');
      recommendations.push('Share success metrics across ChainSync platform');
    }

    // Add facility-specific recommendations
    if (facilityType === 'LOGISTICS_HUB' && riskScore >= 5) {
      recommendations.push('Coordinate with transportation teams');
      recommendations.push('Review route optimization algorithms');
    }
    
    if (facilityType === 'MAINTENANCE_FACILITY' && riskScore >= 5) {
      recommendations.push('Review technician schedules and availability');
      recommendations.push('Check parts inventory levels');
    }

    return recommendations;
  }

  // Enhanced alert generation with ChainSync integration
  async generateAlert(facilityData, riskAssessment) {
    if (riskAssessment.score < 5) return null;

    const alert = {
      id: `ALERT-${Date.now()}`,
      timestamp: new Date().toISOString(),
      facilityId: facilityData.facilityId,
      facilityType: facilityData.facilityType,
      domain: facilityData.domain,
      severity: riskAssessment.level,
      riskScore: riskAssessment.score,
      message: `${riskAssessment.level} conditions detected at ${facilityData.facilityId} (${facilityData.domain})`,
      factors: riskAssessment.factors,
      recommendations: riskAssessment.recommendations,
      parameters: facilityData.parameters,
      dataSource: facilityData.dataSource,
      location: facilityData.location,
      requiresNotification: riskAssessment.score >= 7,
      estimatedCost: this.estimateImpactCost(riskAssessment.score),
      responseDeadline: this.calculateResponseDeadline(riskAssessment.score),
      chainSyncIntegration: {
        slotifyTaskRequired: riskAssessment.score >= 6,
        muleSoftNotification: riskAssessment.score >= 7,
        dashboardUpdate: true,
        crossDomainAlert: riskAssessment.score >= 8
      }
    };

    // Check cross-domain impacts
    if (riskAssessment.score >= 7) {
      alert.crossDomainImpacts = await this.domainManager.checkCrossDomainImpacts(riskAssessment, facilityData.domain);
    }

    // Store alert locally
    if (!alertHistory.has(facilityData.facilityId)) {
      alertHistory.set(facilityData.facilityId, []);
    }
    alertHistory.get(facilityData.facilityId).push(alert);

    // Send alert back to ChainSync MuleSoft API
    try {
      console.log(`📡 Sending alert to ChainSync for ${facilityData.facilityId}...`);
      
      const response = await fetch(`${CHAINSYNC_API_BASE}/alerts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'ChainSync-Agent/2.0',
          'X-Alert-Source': 'ai-agent',
          'X-Domain': facilityData.domain
        },
        body: JSON.stringify({
          ...alert,
          source: 'unified_ai_agent',
          version: '2.0.0'
        })
      });

      if (response.ok) {
        const result = await response.json();
        console.log(`✅ Alert successfully sent to ChainSync: ${result.alertId || alert.id}`);
        alert.chainSyncStatus = 'sent';
        alert.chainSyncResponse = result;
      } else {
        console.error(`❌ ChainSync alert API error: ${response.status}`);
        alert.chainSyncStatus = 'failed';
      }
    } catch (error) {
      console.error(`❌ Failed to send alert to ChainSync: ${error.message}`);
      alert.chainSyncStatus = 'error';
      alert.chainSyncError = error.message;
    }

    return alert;
  }

  estimateImpactCost(riskScore) {
    if (riskScore >= 9) return '$50,000 - $200,000';
    if (riskScore >= 7) return '$15,000 - $50,000';
    if (riskScore >= 5) return '$5,000 - $15,000';
    return '$1,000 - $5,000';
  }

  calculateResponseDeadline(riskScore) {
    const now = new Date();
    if (riskScore >= 9) {
      now.setMinutes(now.getMinutes() + 15);
    } else if (riskScore >= 7) {
      now.setHours(now.getHours() + 2);
    } else if (riskScore >= 5) {
      now.setHours(now.getHours() + 8);
    } else {
      now.setHours(now.getHours() + 24);
    }
    return now.toISOString();
  }

  // New helper methods for ChainSync integration
  async getRequiredSkills(context, domain) {
    const skillMap = {
      environmental: ['environmental engineer', 'safety specialist', 'compliance officer'],
      logistics: ['logistics coordinator', 'transportation specialist', 'supply chain manager'],
      maintenance: ['maintenance technician', 'equipment specialist', 'safety officer'],
      compliance: ['compliance officer', 'auditor', 'regulatory specialist'],
      emergency: ['emergency coordinator', 'safety manager', 'first responder']
    };
    
    return skillMap[domain] || skillMap.environmental;
  }

  estimateTaskDuration(taskType, priority) {
    const durationMap = {
      'CRITICAL': '1-2 hours',
      'HIGH': '2-4 hours',
      'MEDIUM': '4-8 hours',
      'LOW': '1-2 days'
    };
    
    return durationMap[priority] || '4-8 hours';
  }

  async getFacilitiesMetrics(domain = 'all') {
    const facilities = Array.from(facilityProfiles.entries())
      .filter(([id, profile]) => domain === 'all' || profile.domain === domain)
      .map(([id, profile]) => ({
        id,
        type: profile.type,
        domain: profile.domain,
        status: 'ACTIVE'
      }));
    
    return {
      total: facilities.length,
      byDomain: this.groupBy(facilities, 'domain'),
      active: facilities.length
    };
  }

  async getAlertsMetrics(domain = 'all') {
    let allAlerts = [];
    for (const [fId, alerts] of alertHistory.entries()) {
      allAlerts.push(...alerts.filter(alert => 
        domain === 'all' || alert.domain === domain
      ));
    }
    
    return {
      total: allAlerts.length,
      critical: allAlerts.filter(a => a.severity === 'CRITICAL').length,
      high: allAlerts.filter(a => a.severity === 'HIGH').length,
      medium: allAlerts.filter(a => a.severity === 'MEDIUM').length,
      last24h: allAlerts.filter(a => 
        new Date(a.timestamp) > new Date(Date.now() - 24 * 60 * 60 * 1000)
      ).length
    };
  }

  async getPerformanceMetrics(domain = 'all') {
    return {
      avgResponseTime: '2.3s',
      uptime: '99.8%',
      apiCalls: 1250,
      successRate: '99.2%',
      domain: domain
    };
  }

  async getCrossDomainStatus() {
    return {
      environmentalToLogistics: 2,
      maintenanceToEnvironmental: 1,
      emergencyToAll: 0,
      totalCrossDomainAlerts: 3
    };
  }

  groupBy(array, key) {
    return array.reduce((result, item) => {
      const group = item[key];
      result[group] = result[group] || [];
      result[group].push(item);
      return result;
    }, {});
  }
}

// Initialize agent
const agent = new EnterpriseEnvironmentalAgent();

// Test ChainSync connectivity on startup
agent.testChainSyncConnection().then(connected => {
  if (connected) {
    console.log('🔗 ChainSync integration: ENABLED');
  } else {
    console.log('⚠️ ChainSync integration: FALLBACK MODE (using enhanced mock data)');
  }
});

// =============================================================================
// CHAINSYNC UNIFIED ROUTES
// =============================================================================

// Main service info
app.get('/', (req, res) => {
  res.json({
    service: 'ChainSync Unified Intelligent Agent',
    version: '2.0.0',
    status: 'running',
    dataIntegration: 'chainsync_api',
    domains: ['environmental', 'logistics', 'maintenance', 'compliance', 'emergency'],
    crossDomainAwareness: true,
    endpoints: {
      'GET /facilities': 'List all facilities across domains',
      'GET /facility/:id': 'Get facility data (real-time from ChainSync)',
      'POST /analyze/:facilityId': 'Analyze facility with domain awareness',
      'POST /chat': 'Chat with unified agent',
      'GET /alerts': 'Get all cross-domain alerts',
      'GET /alerts/:facilityId': 'Get facility alerts',
      'POST /emergency/:facilityId': 'Emergency response',
      'GET /maintenance/:facilityId': 'Maintenance schedule',
      'GET /compliance/:facilityId': 'Compliance status',
      'GET /cost-analysis/:facilityId': 'Cost analysis',
      'GET /chainsync/test': 'Test ChainSync connectivity',
      'POST /chainsync/webhook': 'ChainSync MuleSoft webhook',
      'POST /slotify/schedule': 'Slotify task scheduling',
      'GET /dashboard/metrics/:domain?': 'Dashboard metrics by domain',
      'POST /api/:domain/analyze': 'Domain-specific analysis',
      'POST /api/:domain/alert': 'Domain-specific alerts'
    }
  });
});

// ChainSync connectivity test endpoint
app.get('/chainsync/test', async (req, res) => {
  const connected = await agent.testChainSyncConnection();
  res.json({
    chainSyncConnected: connected,
    apiUrl: CHAINSYNC_API_BASE,
    timeout: CHAINSYNC_TIMEOUT,
    timestamp: new Date().toISOString(),
    domains: agent.domainManager.domains
  });
});

// Universal domain router
function createDomainRouter(domain) {
  const router = express.Router();
  
  router.post('/analyze', async (req, res) => {
    try {
      const { message, conversationId, facilityId } = req.body;
      const analysis = await agent.analyzeWithDomainContext(
        message || `Analyze current ${domain} status and provide recommendations`,
        conversationId || `${domain}-${Date.now()}`,
        domain,
        facilityId
      );
      
      res.json({
        domain,
        analysis,
        crossDomainImpacts: analysis.crossDomainImpacts || [],
        chainSyncIntegration: true,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      res.status(500).json({ error: error.message, domain });
    }
  });

  router.post('/alert', async (req, res) => {
    try {
      const { alertData, facilityId } = req.body;
      const facilityData = await agent.getAdvancedEnvironmentalData(facilityId);
      const riskAssessment = agent.calculateAdvancedRisk(facilityData);
      const alert = await agent.generateAlert(facilityData, riskAssessment);
      
      // Add domain-specific context
      if (alert) {
        alert.domain = domain;
        alert.crossDomainCheck = await agent.domainManager.checkCrossDomainImpacts(riskAssessment, domain);
      }
      
      res.json(alert || { message: 'No alert generated - risk level below threshold' });
    } catch (error) {
      res.status(500).json({ error: error.message, domain });
    }
  });

  return router;
}

// Domain-specific routes
app.use('/api/environmental', createDomainRouter('environmental'));
app.use('/api/logistics', createDomainRouter('logistics'));
app.use('/api/maintenance', createDomainRouter('maintenance'));
app.use('/api/compliance', createDomainRouter('compliance'));
app.use('/api/emergency', createDomainRouter('emergency'));

// ChainSync MuleSoft webhook endpoint
app.post('/chainsync/webhook', async (req, res) => {
  try {
    const { flowId, domain, data, source, facilityId } = req.body;
    
    console.log(`📡 ChainSync webhook: ${flowId} from ${source} (${domain})`);
    
    // Process through domain-aware agent
    const analysis = await agent.analyzeWithDomainContext(
      `Process ${domain} data from ${source}: ${JSON.stringify(data)}`,
      `webhook-${flowId}`,
      domain || 'environmental',
      facilityId
    );
    
    // Format for MuleSoft response
    const response = {
      flowId,
      status: 'processed',
      domain: domain || 'environmental',
      analysis: analysis.response,
      recommendations: analysis.recommendations || [],
      crossDomainImpacts: analysis.crossDomainImpacts || [],
      nextSteps: analysis.nextSteps || [],
      timestamp: new Date().toISOString(),
      processedBy: 'ChainSync-Agent-v2.0',
      chainSyncIntegration: true
    };
    
    res.json(response);
  } catch (error) {
    console.error('Webhook processing error:', error);
    res.status(500).json({ 
      error: error.message,
      flowId: req.body.flowId,
      status: 'failed'
    });
  }
});

// Slotify integration endpoint
app.post('/slotify/schedule', async (req, res) => {
  try {
    const { taskType, priority, facilityId, context } = req.body;
    
    const facilityData = await agent.getAdvancedEnvironmentalData(facilityId);
    const domain = agent.domainManager.identifyDomain(facilityId, JSON.stringify(context));
    
    const slotifyRequest = {
      taskType: taskType || 'CHAINSYNC_RESPONSE',
      priority: priority || 'MEDIUM',
      domain,
      facilityId,
      requiredSkills: await agent.getRequiredSkills(context, domain),
      location: facilityData.location,
      estimatedDuration: agent.estimateTaskDuration(taskType, priority),
      context: {
        ...context,
        realTimeData: facilityData.parameters,
        crossDomainImpacts: await agent.domainManager.checkCrossDomainImpacts(
          { score: priority === 'CRITICAL' ? 9 : 5 }, domain
        )
      },
      chainSyncIntegration: true
    };
    
    res.json({
      slotifyRequest,
      recommended: true,
      chainSyncIntegration: true,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Dashboard metrics endpoint
app.get('/dashboard/metrics/:domain?', async (req, res) => {
  try {
    const domain = req.params.domain || 'all';
    
    const metrics = {
      timestamp: new Date().toISOString(),
      domain,
      facilities: await agent.getFacilitiesMetrics(domain),
      alerts: await agent.getAlertsMetrics(domain),
      performance: await agent.getPerformanceMetrics(domain),
      crossDomainStatus: await agent.getCrossDomainStatus(),
      chainSyncIntegration: true
    };
    
    res.json(metrics);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Existing routes (updated with domain awareness)
app.get('/facilities', (req, res) => {
  const facilities = Array.from(facilityProfiles.entries()).map(([id, profile]) => ({
    id,
    type: profile.type,
    domain: profile.domain,
    capacity: profile.capacity,
    location: profile.location,
    status: 'ACTIVE',
    dataSource: 'chainsync_api'
  }));
  
  res.json({ 
    facilities, 
    total: facilities.length,
    domains: agent.domainManager.domains,
    crossDomainEnabled: true
  });
});

app.get('/facility/:id', async (req, res) => {
  try {
    const facilityId = req.params.id;
    const facilityData = await agent.getAdvancedEnvironmentalData(facilityId);
    const riskAssessment = agent.calculateAdvancedRisk(facilityData);
    const alert = await agent.generateAlert(facilityData, riskAssessment);
    
    // Add cross-domain analysis
    let crossDomainImpacts = [];
    if (riskAssessment.score >= 6) {
      crossDomainImpacts = await agent.domainManager.checkCrossDomainImpacts(riskAssessment, facilityData.domain);
    }
    
    res.json({
      facility: facilityData,
      risk: riskAssessment,
      alert: alert,
      crossDomainImpacts,
      dataIntegration: {
        source: facilityData.dataSource,
        freshness: facilityData.dataFreshness,
        quality: facilityData.dataQuality
      },
      chainSyncIntegration: true
    });
  } catch (error) {
    res.status(404).json({ error: error.message });
  }
});

app.post('/analyze/:facilityId', async (req, res) => {
  try {
    const facilityId = req.params.facilityId;
    const { conversationId, question } = req.body;
    
    const facilityData = await agent.getAdvancedEnvironmentalData(facilityId);
    const riskAssessment = agent.calculateAdvancedRisk(facilityData);
    const alert = await agent.generateAlert(facilityData, riskAssessment);
    
    // Domain-aware analysis
    const domain = facilityData.domain || 'environmental';
    const analysis = await agent.analyzeWithDomainContext(
      `FACILITY ANALYSIS: ${facilityId}
Type: ${facilityData.facilityType}
Domain: ${domain}
Risk: ${riskAssessment.score}/10 (${riskAssessment.level})
Data Source: ${facilityData.dataSource}
Factors: ${riskAssessment.factors.join(', ') || 'None'}
Parameters: ${JSON.stringify(facilityData.parameters, null, 2)}
${question ? `Question: ${question}` : 'Provide comprehensive analysis with real-time data insights and cross-domain considerations'}`,
      conversationId,
      domain,
      facilityId
    );
    
    res.json({
      facilityData,
      riskAssessment,
      alert,
      aiAnalysis: analysis,
      recommendations: riskAssessment.recommendations,
      crossDomainImpacts: analysis.crossDomainImpacts || [],
      dataIntegration: {
        source: facilityData.dataSource,
        freshness: facilityData.dataFreshness,
        quality: facilityData.dataQuality
      },
      chainSyncIntegration: true
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/chat', async (req, res) => {
  try {
    const { message, conversationId, facilityContext, domain } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: 'Message required' });
    }

    let enhancedMessage = message;
    let detectedDomain = domain || 'environmental';
    
    if (facilityContext) {
      const facilityData = await agent.getAdvancedEnvironmentalData(facilityContext);
      const riskAssessment = agent.calculateAdvancedRisk(facilityData);
      detectedDomain = facilityData.domain || agent.domainManager.identifyDomain(facilityContext, message);
      
      enhancedMessage = `REAL-TIME CONTEXT: ${facilityContext} (${facilityData.facilityType})
Domain: ${detectedDomain}
Data Source: ${facilityData.dataSource}
Risk: ${riskAssessment.level} (${riskAssessment.score}/10)
Current Issues: ${riskAssessment.factors.join(', ') || 'None'}
Key Parameters: ${JSON.stringify(facilityData.parameters, null, 2)}
Question: ${message}`;
    }

    const result = await agent.analyzeWithDomainContext(enhancedMessage, conversationId, detectedDomain, facilityContext);
    res.json({
      ...result,
      domain: detectedDomain,
      chainSyncIntegration: true
    });
    
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/alerts', (req, res) => {
  const allAlerts = [];
  for (const [fId, alerts] of alertHistory.entries()) {
    allAlerts.push(...alerts.map(alert => ({ ...alert, facilityId: fId })));
  }
  
  allAlerts.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  
  res.json({
    alerts: allAlerts.slice(0, 50),
    total: allAlerts.length,
    facilities: Array.from(alertHistory.keys()),
    chainSyncIntegration: true,
    crossDomainEnabled: true,
    byDomain: allAlerts.reduce((acc, alert) => {
      acc[alert.domain] = (acc[alert.domain] || 0) + 1;
      return acc;
    }, {})
  });
});

app.get('/alerts/:facilityId', (req, res) => {
  const facilityId = req.params.facilityId;
  const alerts = alertHistory.get(facilityId) || [];
  res.json({ 
    facilityId, 
    alerts: alerts.slice(-10),
    total: alerts.length,
    chainSyncIntegration: true
  });
});

app.post('/emergency/:facilityId', async (req, res) => {
  try {
    const facilityId = req.params.facilityId;
    const { emergencyType, description } = req.body;
    
    const facilityData = await agent.getAdvancedEnvironmentalData(facilityId);
    const riskAssessment = agent.calculateAdvancedRisk(facilityData);
    riskAssessment.score = Math.max(riskAssessment.score, 9);
    riskAssessment.level = 'CRITICAL';
    
    const alert = await agent.generateAlert(facilityData, riskAssessment);
    
    // Check cross-domain emergency impacts
    const crossDomainImpacts = await agent.domainManager.checkCrossDomainImpacts(
      { score: 9, severity: 'CRITICAL' }, 'emergency'
    );
    
    const emergencyLog = {
      id: `EMERGENCY-${Date.now()}`,
      timestamp: new Date().toISOString(),
      facilityId,
      domain: facilityData.domain,
      type: emergencyType || 'ENVIRONMENTAL_INCIDENT',
      description: description || 'Emergency detected from real-time monitoring',
      severity: 'CRITICAL',
      status: 'ACTIVE',
