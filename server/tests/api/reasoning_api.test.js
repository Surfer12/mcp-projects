const request = require('supertest');
const app = require('../../src/main'); // Express app import

describe('API /api/reasoning Tests', () => {
    it('should process a prompt with MCP orchestrator successfully', async () => {
        const payload = {
            prompt: 'Test AI integration with quality checks',
            mcpServices: [
                { type: 'developer', execute: async (response) => console.log('Developer executed:', response) },
                { type: 'qa', execute: async (response) => console.log('QA executed on:', response) },
            ],
        };

        const response = await request(app).post('/api/reasoning').send(payload);

        expect(response.status).to.equal(200);
        expect(response.body.success).to.be.true;
        expect(response.body).to.have.property('response').that.is.a('string');
        expect(response.body.mcpServicesProcessed).to.equal(2);
    });
});