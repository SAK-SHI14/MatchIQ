FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json .
RUN npm install

# Copy source
COPY . .

# Expose port
EXPOSE 5173

# Start Vite server in host mode
CMD ["npm", "run", "dev", "--", "--host"]
