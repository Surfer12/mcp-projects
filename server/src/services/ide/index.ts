import { Express, Request, Response } from 'express';
import { plugin } from './plugin';

export const setupIDEService = (app: Express): void => {
  // Initialize IDE integration routes
  app.post('/api/ide/command', async (req: Request, res: Response) => {
    try {
      const { command, params } = req.body;
      const result = await plugin.executeCommand(command, params);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: 'IDE command execution failed' });
    }
  });
};