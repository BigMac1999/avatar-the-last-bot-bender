FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy the package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Expose the port the app runs on
EXPOSE 3000

# Set environment variables for Next.js
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1

# Command to run the application
CMD ["npx", "next", "dev", "-p", "3000", "-H", "0.0.0.0"]

