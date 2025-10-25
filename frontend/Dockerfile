# Dockerfile for F1 Q&A Frontend
# Production-ready Nginx server

FROM nginx:alpine

# Maintainer info
LABEL maintainer="F1 Q&A System"
LABEL description="Frontend for F1 Q&A System - Formula 1 Semantic Network Q&A"

# Set working directory
WORKDIR /usr/share/nginx/html

# Remove default nginx static assets
RUN rm -rf ./*

# Copy frontend files
COPY public/ .
COPY src/ ./src/

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Set proper permissions
RUN chmod -R 755 /usr/share/nginx/html

# Create nginx user if not exists
RUN addgroup -g 101 -S nginx || true && \
    adduser -S -D -H -u 101 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx || true

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]

