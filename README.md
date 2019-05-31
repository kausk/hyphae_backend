# hyphae_backend

Important: in routes/image.js change the variable pathToRoot to hyphae_frontend from 
```
const pathToRoot = '/Users/ksk/hyphae_frontend'; // CHANGE TO YOUR LOCAL hyphae_frontend
```
to the absolute path of the hyphae_backend folder on your computer. For example if your username is Keshav and the hyphae_backend folder is in your home directory, this could be:
```
const pathToRoot = '/Users/keshav/hyphae_frontend'; // CHANGE TO YOUR LOCAL hyphae_frontend
```
This simulates a common datastore between the backend and frontend, which will be an Amazon S3 bucket eventually.


In order to install all dependencies and run the local development server: 

```
npm install
npm start
```
Make sure the development server is running before starting the hyphae_frontend!
