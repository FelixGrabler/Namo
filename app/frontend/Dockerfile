# Build stage
FROM node:20-alpine as build-stage

WORKDIR /app/frontend

# Copy package files
COPY app/frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY app/frontend/ .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine as production-stage

# Copy built files from build stage
COPY --from=build-stage /app/frontend/dist /usr/share/nginx/html

# Copy nginx configuration (optional, using default for now)
# COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]