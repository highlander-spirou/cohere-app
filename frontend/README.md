1. install dependencies `npm install` or `yarn`
2. run in development
`npm run start` or `yarn start`
3. run in production (must deploy the backend first, via Heroku for example) -> get the backend url -> App.tsx -> line 21 -> change from "localhost" to backend server links
`yarn build` -> deploy the static dist folder to static deployment (like netlify)