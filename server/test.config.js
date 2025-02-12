const path = require('path');

module.exports = {
    rootDir: path.resolve(__dirname),
    testEnvironment: 'node',
    testMatch: [
        '**/__tests__/**/*.js',
        '**/?(*.)+(spec|test).js'
    ],
    moduleFileExtensions: ['js', 'json', 'ts'],
    transform: {
        '^.+\\.js$': 'babel-jest',
        '^.+\\.ts$': 'ts-jest'
    },
    globals: {
        'ts-jest': {
            tsconfig: 'tsconfig.json'
        }
    },
    coverageDirectory: './coverage',
    collectCoverageFrom: [
        'src/**/*.js',
        'src/**/*.ts',
        '!**/node_modules/**',
        '!**/*.test.js',
        '!**/*.test.ts'
    ],
    coverageThreshold: {
        global: {
            branches: 80,
            functions: 80,
            lines: 80,
            statements: 80
        }
    }
};