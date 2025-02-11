import { Express } from 'express';
import { providerSelector } from './provider-selector';

export const setupMLService = (app: Express): void => {
  // Initialize ML service routes
  app.post('/api/ml/predict', async (req: Express.Request, res: Express.Response) => {
    try {
      const { input, model } = req.body;
      const result = await providerSelector.predict(input, model);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: 'Prediction failed' });
    }
  });
};