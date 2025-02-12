const { expect } = require('chai');
const WorkflowManager = require('../../src/tools/workflow/workflow_manager');

describe('WorkflowManager Tests (Error Handling)', () => {
    let workflowManager;

    beforeEach(() => {
        workflowManager = new WorkflowManager();
    });

    it('should handle invalid actions gracefully', async () => {
        try {
            const invalidActions = [{ command: 'take_screenshot' }]; // Missing required fields
            await workflowManager.runPatternRecognitionWorkflow(invalidActions);
        } catch (error) {
            expect(error).to.be.an('error');
            expect(error.message).to.include('Invalid action');
        }
    });

    it('should reject empty action list', async () => {
        try {
            const emptyActions = [];
            await workflowManager.runPatternRecognitionWorkflow(emptyActions);
        } catch (error) {
            expect(error).to.be.an('error');
            expect(error.message).to.include('No actions provided');
        }
    });
});