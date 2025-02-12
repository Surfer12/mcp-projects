interface IDECommand {
    type: 'edit' | 'navigate' | 'search' | 'execute';
    target?: string;
    content?: string;
    position?: {
        line: number;
        column: number;
    };
}
interface CommandResult {
    success: boolean;
    data?: any;
    error?: string;
}
declare class IDEPlugin {
    private supportedCommands;
    executeCommand(command: string, params: IDECommand): Promise<CommandResult>;
    private handleEdit;
    private handleNavigation;
    private handleSearch;
    private handleExecution;
}
export declare const plugin: IDEPlugin;
export {};
