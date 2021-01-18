FROM node:12.16.1-slim
RUN apt-get update \
 && apt-get install git -y

WORKDIR /frontend

COPY package.json package.json
RUN npm install

ENV NUXT_HOST '0.0.0.0'
ENV NUXT_PORT 3000

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev"]
