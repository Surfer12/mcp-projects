"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.server = void 0;
const child_process_1 = require("child_process");
const util_1 = require("util");
const execAsync = (0, util_1.promisify)(child_process_1.exec);
class CoreServer {
    constructor() {
        this.config = {
            maxExecutionTime: parseInt(process.env.MAX_EXECUTION_TIME || '30000', 10),
            allowedCommands: (process.env.ALLOWED_COMMANDS || 'ls,pwd,echo').split(','),
        };
    }
    async execute(command) {
        // Validate command
        const baseCommand = command.split(' ')[0];
        if (!this.config.allowedCommands.includes(baseCommand)) {
            throw new Error(`Command '${baseCommand}' is not allowed`);
        }
        try {
            // Execute command with timeout
            const { stdout, stderr } = await Promise.race([
                execAsync(command),
                new Promise((_, reject) => setTimeout(() => reject(new Error('Command execution timed out')), this.config.maxExecutionTime)),
            ]);
            return {
                stdout: stdout.trim(),
                stderr: stderr.trim(),
                exitCode: 0,
            };
        }
        catch (error) {
            console.error('Command execution failed:', error);
            return {
                stdout: '',
                stderr: error.message || 'Unknown error occurred',
                exitCode: error.code || 1,
            };
        }
    }
    async getStatus() {
        return {
            status: 'running',
            uptime: process.uptime(),
            memory: process.memoryUsage(),
        };
    }
}
exports.server = new CoreServer();
//# sourceMappingURL=server.js.map