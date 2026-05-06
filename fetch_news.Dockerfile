# Use an official Node.js image as the base
FROM node:25-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json first
COPY news/package*.json ./

# Install npm dependencies (cached in subsequent builds if files don't change)
RUN npm install

# Copy the rest of the application code
COPY /news/ .

# Expose the port the app runs on
EXPOSE 3000

# Define the command to run the application
CMD ["node", "action.js"]