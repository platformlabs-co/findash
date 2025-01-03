# Use the official Node.js image from the Docker Hub
FROM node:18-alpine

# Set environment variables
ENV NODE_ENV=development

# Create and set the working directory
WORKDIR /app

# Copy only the package.json and package-lock.json to leverage Docker cache
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Run the application with live reload
CMD ["npm", "start"]