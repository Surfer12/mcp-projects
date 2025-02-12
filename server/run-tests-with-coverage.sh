#!/bin/bash

# Set Mock Environment Variables Explicitly
export ANTHROPIC_API_KEY='mock-anthropic-key'
export OPENAI_API_KEY='mock-openai-key'
export GOOGLE_API_KEY='mock-google-key'

# Execute Coverage Tests
./node_modules/.bin/nyc --reporter=html --reporter=text ./node_modules/.bin/mocha "tests/**/*.test.js"