class Performance {
    constructor(config = {}) {
        this.config = {
            trackingEnabled: config.trackingEnabled || true,
            metricTypes: config.metricTypes || ['time', 'memory']
        };
    }

    async trackStep(stepName, stepFunction) {
        const startTime = Date.now();
        const startMemory = process.memoryUsage().heapUsed;

        try {
            const result = await stepFunction();

            const endTime = Date.now();
            const endMemory = process.memoryUsage().heapUsed;

            return {
                stepName,
                duration: endTime - startTime,
                memoryUsed: endMemory - startMemory,
                success: true,
                result
            };
        } catch (error) {
            return {
                stepName,
                duration: 0,
                memoryUsed: 0,
                success: false,
                error: error.message
            };
        }
    }

    // Simplified performance tracking method
    measurePerformance(fn, context = {}) {
        return async (...args) => {
            const start = Date.now();
            try {
                const result = await fn(...args);
                const duration = Date.now() - start;

                return {
                    result,
                    performance: {
                        duration,
                        timestamp: new Date().toISOString(),
                        context
                    }
                };
            } catch (error) {
                return {
                    error: error.message,
                    performance: {
                        duration: 0,
                        timestamp: new Date().toISOString(),
                        context,
                        failed: true
                    }
                };
            }
        };
    }
}

module.exports = { Performance };