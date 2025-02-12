interface CommandResult {
    stdout: string;
    stderr: string;
    exitCode: number;
}
declare class CoreServer {
    private config;
    constructor();
    execute(command: string): Promise<CommandResult>;
    getStatus(): Promise<{
        status: 'running' | 'error';
        uptime: number;
        memory: NodeJS.MemoryUsage;
    }>;
}
export declare const server: CoreServer;
export {};
