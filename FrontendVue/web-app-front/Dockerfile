FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Não precisa mais do build, pois estamos em modo de desenvolvimento
# RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "dev"]