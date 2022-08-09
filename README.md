
# Dealership AI

This project provides a website serving and AI model trained to estimate the value of used cars.

It consists of a dockerized service architecture, that is served using kubernetes via an ingress controller.

The model is logged using MLflow,
allowing us to organize our diferent models and serving only the correct one to the backend for inference.

During experimentation we concluded that a (linear) regression is the best fit for our problem, since it provides very fast inference and possibility for explainability through coefficients.

Backend properties:
- Technologies: FastAPI, Tortoise ORM, Aerich
- Using Aerich for easy db setup, updatas and migration
- Providing API calls for and executing inference, car and user management
- Providing small features like dynmaic select filter and model coefficient endpoints
- Running via ingress on port 80, subpath /FastAPI

Frontend properties:
- Vue.js 3 using mostly Composition API
- Vuex as store for car and user entities, also handling axios API requests
- Quasar as UI component library

Our training dataset consists of three sources:
- a static .csv from Autoscout24 serves as base (saved in S3 MinIO)
- feedback endpoint for "car sales" from the backend 
- a scraper as Kubernetes cronjob saving around 400 new car listings from Autoscout24 (also to S3 MinIO)

Heres a little overview as C4 model on level 2:

![C4 Container Diagramm Level 2](C4ContainerLevel2.svg)


## Development

The whole project can be run locally via the docker-compose.yaml
Simply clone the whole repo, cd into the base folder and execute:

```
docker-compose up -d --build    
```

That starts the frontend, backend and db containers and linking them correctly with a persistend db and volume mount to the repo.
Therefore changes can be seen by execeuting the above again.

The Vue.js frontend should be visible under `localhost:8080` and the FastAPI backend under `localhost/fastapi`.

### Frontend
Since the frontend needs to be built for production, and therefore is also built for the docker compose, a better workflow for frontend developing would be, to stop the frontend container and run the frontend via npm.
Just cd into `services/frontend` and execute:

```
npm install
npm run serve
```
Now you can immediately see the changes in the frontend.


## Kubernetes & Ingress
The following services/deployments are served using their own Kubernetes pods/containers:
- frontend: ingress service on port 80
- backend: ingress service on port 80, subpath /fastapi
- scraper: cronjob executed everyday at 13:35 (GMT+2)
- database: stateful set
- mlflow model training: job exceuted on change

Only the frontend and backend are handled by ingress.
See the .yaml files for further info on the structure.

## Gitlab CI/CD 
Once a new commit has been pushed to gitlab, a pipeline consisting of a build and deploy phase is executed by gitlab runners.
Note that the database is NOT part of this pipeline.

#### Build stage:
Build all the docker containers (frontend, backend, scraper, training/experimentation),
then we commit them to docker hub.

#### Deploy stage:
Log into the Kubernetes cluster and applying the .yaml-files for the above mentioned containers.
This results every pod (were the image pull policy is set accordingly) to check for a new image.
Backend and frontend pods are also explicitly restarted.

