FROM node:10.12.0-alpine

COPY ./frontend/package*.json ./

RUN npm install && rm ./package*.json

COPY ./frontend /app/

WORKDIR /app

CMD [ "npm", "run", "serve" ]
