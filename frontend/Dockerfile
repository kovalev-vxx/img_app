FROM node:14-slim

WORKDIR /frontend

COPY package.json ./

COPY yarn.lock ./

RUN yarn

COPY . .

EXPOSE 3000

RUN yarn build

RUN yarn global add serve

CMD [ "serve", "-s", "build" ]

