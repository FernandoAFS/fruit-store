# Fruit store exercise monorepo

- fruit-store: Main python project.
- data: Placeholder. data-lab uses this to read and write.
- data-lab: Jupyter notebooks for offline data analysis.
- devops: docker-compose files

## Quickstart demo:

1. Copy all the contents of "data" to devops/input-data. It sould look like `devops/input-data/2023...`
2. Build the docker images:

```bash
cd fruit-store
make docker
```

3. Run the server

```bash
cd devops
docker compose up -d
```

4. Upload the data:

```bash
cd devops
docker compose run load
```

5. Print the report

```bash
cd devops
docker compose run report
```
