const path = require('path');
const dotenv = require('dotenv');
const dotenvExpand = require('dotenv-expand');

// Load environment configuration
const loadEnvironmentConfig = () => {
    const environment = process.env.NODE_ENV || 'development';
    const configDir = path.resolve(__dirname, '../../config/env');

    const envFiles = [
        `.env.${environment}.local`,
        `.env.${environment}`,
        '.env.local',
        '.env'
    ];

    envFiles.forEach(file => {
        const result = dotenv.config({ path: path.join(configDir, file) });
        if (result.error) {
            console.warn(`Could not load environment file: ${file}`);
        } else {
            dotenvExpand.expand(result);
        }
    });
};

loadEnvironmentConfig();

// Import unified server
const server = require('./unified-server');

// Start server
async function startServer() {
    try {
        await server.initialize();
        const port = process.env.PORT || 3000;
        server.listen(port);
    } catch (error) {
        console.error('Failed to start server:', error);
        process.exit(1);
    }
}

startServer();