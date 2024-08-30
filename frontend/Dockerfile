# Use Node.js for the Tailwind CSS build process
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package.json package-lock.json ./

# Install the Node.js dependencies (only for the build phase)
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the Tailwind CSS using the production configuration
RUN npm run build:css

# Verify the contents of the dist directory
RUN ls -l /app/dist/

# Use NGINX to serve the frontend application
FROM nginx:alpine

# Copy the built CSS and other assets from the build stage
COPY --from=build /app/dist /usr/share/nginx/html/dist
COPY --from=build /app/assets /usr/share/nginx/html/assets/

# Copy HTML and script files
COPY --from=build /app/index.html /usr/share/nginx/html/
COPY --from=build /app/roadmap.html /usr/share/nginx/html/
COPY --from=build /app/scripts /usr/share/nginx/html/scripts/

# Copy the NGINX configuration file
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Expose the port that NGINX will serve on
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
