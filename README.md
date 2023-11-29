# TVE
## Key Technologies

* [Poetry](https://python-poetry.org/docs/pyproject/)
* [FastAPI](https://fastapi.tiangolo.com/) - FastAPI framework, high performance, easy to learn, fast to code, ready for production


## Development environment Setup

### Python

```commandline
python 3.7
```

#### Configuration Environment Variables

Rename .sample.env to .env
```commandline
cp .sample.env .env
```
Enter respective values for environment variables

## Docker Deployment

```bash
make build
```

```bash
make run
```
## Documentation
### API name:
    API Usage: 
    API Description: 
    URL: <url>/api/v1/<path>
    Method: POST/GET/PUT
    Sample Input:
        {
        "json_key":"json_value"
        }
 
    Sample Output:
        {
        "json_key":"json_value"
        }
