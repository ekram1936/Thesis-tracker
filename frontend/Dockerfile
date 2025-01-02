# Base Image for Angular
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY frontend/package*.json ./
RUN npm install
# Copy the entire Angular project into the container
COPY frontend/ .
# Build the Angular app with the production configuration
# RUN npm run build -- --project frontend --configuration production

RUN cp src/environments/environment.prod.ts src/environments/environment.ts
# Expose the app port
EXPOSE 4200

# Start the Angular app
CMD ["npm", "run", "start"]

# CMD ["npx", "http-server", "dist", "-p", "4200"]