# Stage 1: Build the React application
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./

# Install frontend dependencies (this will install a clean node_modules inside the container)
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Build the React application for production
RUN npm run build

# Stage 2: Serve the application with a lightweight Nginx server
FROM nginx:1.21-alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]