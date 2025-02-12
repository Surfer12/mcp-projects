const logger = require('winston');

async function orchestrateMCPServices({ response, services }) {
    for (const service of services) {
        try {
            await service.execute(response);
            logger.info(`Service ${service.constructor.name} executed successfully.`);
        } catch (error) {
            logger.error(`Service ${service.constructor.name} failed: ${error.message}`);
            throw error; // Stop execution on failure
        }
    }
}

module.exports = orchestrateMCPServices;