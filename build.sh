#!/bin/bash

echo "Building PromptPerfect for Vercel deployment..."

# Install dependencies and build frontend
cd frontend/frontend
npm install
npm run build

echo "Build completed successfully!"
echo "Deploy to Vercel by running: vercel"
