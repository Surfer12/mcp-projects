import { Express, Request, Response } from 'express';
import { ProviderSelector } from './provider-selector';

const providerSelector = new ProviderSelector();

export const setupMLService = (app: Express): void => {
  // Initialize ML service routes
  app.post('/api/ml/predict', async (req: Request, res: Response) => {
    try {
      const { input, model } = req.body;
      const result = await providerSelector.predict('openai', input, { model });
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: 'Prediction failed' });
    }
  });
};