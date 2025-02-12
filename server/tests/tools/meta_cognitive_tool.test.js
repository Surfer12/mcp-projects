const { expect } = require('chai');
const MetaCognitiveTool = require('../../src/tools/meta/meta_cognitive_tool');

describe('MetaCognitiveTool Tests', () => {
    let metaCognitiveTool;

    beforeEach(() => {
        metaCognitiveTool = new MetaCognitiveTool();
    });

    it('should analyze a basic action', async () => {
        const action = { command: 'take_screenshot', params: { x: 100, y: 100 } };
        const result = await metaCognitiveTool.analyze(action);

        expect(result).to.be.an('object');
        expect(result).to.have.property('state');
        expect(result.state).to.have.property('patterns');
    });

    it('should provide adaptations for complex actions', async () => {
        const actions = [
            { command: 'click', params: { x: 200, y: 200 } },
            { command: 'drag', params: { from: [100, 100], to: [200, 200] } }
        ];
        const adaptations = await metaCognitiveTool.adapt(actions);

        expect(adaptations).to.be.an('array');
    });

    it('should track cognitive effort accurately', async () => {
        metaCognitiveTool.trackCognitiveEffort(10); // Add 10 units of effort
        metaCognitiveTool.trackCognitiveEffort(5); // Add 5 more units of effort

        const effort = metaCognitiveTool.getCognitiveEffort();
        expect(effort).to.equal(15);
    });
});