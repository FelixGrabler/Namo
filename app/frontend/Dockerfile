# Development stage
FROM node:20-alpine

WORKDIR /app/frontend

# Copy package files
COPY app/frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY app/frontend/ .

# Expose port for Vite dev server
EXPOSE 5173

# Start the development server with hot reloading
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]