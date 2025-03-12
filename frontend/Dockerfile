FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy all files
COPY . .

# Run the application
EXPOSE 3000
CMD ["npm", "run", "dev"]