Build the docker image (using the name 'a24-scraper'):
```bash
docker build --tag a24-scraper .
```

Run the docker image in this folder for correct mounting:
```bash
docker run -d \
  -it \
  --name a24-scraper \
  -v "$(pwd)":/app \
  a24-scraper:latest
```
