# Development stage
FROM node:20-alpine

WORKDIR /app/frontend

# Copy package files for better Docker layer caching
COPY app/frontend/package.json ./

# Install dependencies with optimized flags
RUN npm install --no-audit --no-fund --legacy-peer-deps

# Copy source code
COPY app/frontend/ ./

# Expose port for Vite dev server
EXPOSE 5173

# Start the development server with hot reloading
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]