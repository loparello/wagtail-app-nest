FROM node:24-slim

WORKDIR /frontend

# Copy package.json and package-lock.json first to leverage Docker cache
COPY ./package*.json /frontend/

RUN npm install

COPY ./vite.config.ts /frontend/
COPY ./tsconfig*.json /frontend/
COPY ./eslint.config.js /frontend/
COPY ./src /frontend/src

EXPOSE 5173

# Default command to run the development server
CMD ["npm", "run", "serve"]
