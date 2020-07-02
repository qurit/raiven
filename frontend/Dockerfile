FROM node:12.16.1-slim
WORKDIR /frontend

COPY package.json package.json
RUN npm install

ENV NUXT_HOST '0.0.0.0'

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "start"]
