# Base Image for Angular
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY frontend/package*.json ./
RUN npm install
# Copy the entire Angular project into the container
COPY frontend/ .


RUN cp src/environments/environment.prod.ts src/environments/environment.ts
# Expose the app port
EXPOSE 4200

# Start the Angular app
CMD ["npm", "run", "start"]

