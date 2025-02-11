import { setupCodeAnalysisService } from '@services/code-analysis';
import { setupCoreService } from '@services/core';
import { setupIDEService } from '@services/ide';
import { setupMLService } from '@services/ml';
import dotenv from 'dotenv';
import express from 'express';

// Load environment variables
dotenv.config({ path: './config/env/.env' });

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Initialize services
setupCodeAnalysisService(app);
setupCoreService(app);
setupIDEService(app);
setupMLService(app);

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// Start server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});