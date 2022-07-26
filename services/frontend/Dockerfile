# build stage
FROM node:lts-alpine as build-stage

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

RUN npm install @vue/cli@5.0.4 -g

COPY package.json .
COPY package-lock.json .
RUN npm install
COPY . .
RUN npm run build

#production-stage
FROM nginx:stable-alpine  as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80