import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

interface CommandResult {
  stdout: string;
  stderr: string;
  exitCode: number;
}

interface ServerConfig {
  maxExecutionTime: number;
  allowedCommands: string[];
}

class CoreServer {
  private config: ServerConfig;

  constructor() {
    this.config = {
      maxExecutionTime: parseInt(process.env.MAX_EXECUTION_TIME || '30000', 10),
      allowedCommands: (process.env.ALLOWED_COMMANDS || 'ls,pwd,echo').split(','),
    };
  }

  async execute(command: string): Promise<CommandResult> {
    // Validate command
    const baseCommand = command.split(' ')[0];
    if (!this.config.allowedCommands.includes(baseCommand)) {
      throw new Error(`Command '${baseCommand}' is not allowed`);
    }

    try {
      // Execute command with timeout
      const { stdout, stderr } = await Promise.race([
        execAsync(command),
        new Promise<never>((_, reject) =>
          setTimeout(() => reject(new Error('Command execution timed out')), this.config.maxExecutionTime)
        ),
      ]);

      return {
        stdout: stdout.trim(),
        stderr: stderr.trim(),
        exitCode: 0,
      };
    } catch (error: any) {
      console.error('Command execution failed:', error);
      return {
        stdout: '',
        stderr: error.message || 'Unknown error occurred',
        exitCode: error.code || 1,
      };
    }
  }

  async getStatus(): Promise<{
    status: 'running' | 'error';
    uptime: number;
    memory: NodeJS.MemoryUsage;
  }> {
    return {
      status: 'running',
      uptime: process.uptime(),
      memory: process.memoryUsage(),
    };
  }
}

export const server = new CoreServer();
