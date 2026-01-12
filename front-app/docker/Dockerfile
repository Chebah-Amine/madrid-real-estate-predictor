# syntax=docker/dockerfile:1

# Latest Node LTS line is 24.x (Jan 2026) :contentReference[oaicite:4]{index=4}
ARG NODE_VERSION=24
FROM node:${NODE_VERSION}-alpine AS dev

WORKDIR /usr/src/app


# Install deps first (better layer cache)
COPY ./app/package*.json ./
# If you use npm-lock: prefer npm ci
RUN npm ci

EXPOSE 4200

# Use the project's local Angular CLI (no global install needed)
CMD ["npx", "ng", "serve", "--host", "0.0.0.0", "--port", "4200"]
