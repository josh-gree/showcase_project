# Coding Showcase - Joshua Greenhalgh

## Aims

- To show off a range of technologies that I have used and some I have not.
- Multi-language - Python, JS, Golang, SQL
- Multi-tech - Frontend (JS, Vue/React, HTML), Backend (PG, Kafka, Golang, Docker, maybe k8s)
- Engineering + Analysis

## Outline

- Monitor response times to an endpoint, cluster them, vizualize them
- Use go to create the endpoint, simulate requests using python (async), push response times to kafka, collect kafka stream in PG, cluster on a moving window using a view on PG (python), pass cluster params to kafka, pull kafka stream to websocket, realtime updating frontend viz in Vue/React...

# Useage

Pull containers;

```bash
> make pull
```

Bring containers up;

```bash
> make up
```

Viz available at `http://localhost:8080`
