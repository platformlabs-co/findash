# Use the official Node.js image from the Docker Hub
FROM node:18-alpine

# Add build argument with production as default
ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV

# Add hot-reload support for development
ENV CHOKIDAR_USEPOLLING=true

# Create and set the working directory
WORKDIR /app

# Copy only the package.json and package-lock.json to leverage Docker cache
COPY package.json package-lock.json ./

# Install dependencies based on NODE_ENV
RUN if [ "$NODE_ENV" = "production" ]; \
    then npm ci --only=production; \
    else npm install; \
    fi

# Copy the application code
COPY . .

# Build for production, start dev server for development
EXPOSE 3000
CMD if [ "$NODE_ENV" = "production" ]; \
    then npm run build && npm run serve; \
    else npm start; \
    fi