import { Express } from 'express';
import { server } from './server';

export const setupCoreService = (app: Express): void => {
  // Initialize core service routes
  app.post('/api/core/execute', async (req: Express.Request, res: Express.Response) => {
    try {
      const { command } = req.body;
      const result = await server.execute(command);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: 'Command execution failed' });
    }
  });
};