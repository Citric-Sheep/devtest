# CRUD solution to storage Elevator Demand


## Usage
These instructions were followed to install and run the API within a Linux system.

#### Installing
```
python3 -m venv venv
pip install --upgrade pip
pip install -r ./requirements.txt
```

#### Testing
```
pytest ./tests
```

#### Deployment
```
uvicorn app:app
```


#### Sample
```commandline
$ httpx  http://127.0.0.1:8000
HTTP/1.1 200 OK
date: Mon, 08 Apr 2024 15:23:00 GMT
server: uvicorn
content-length: 56
content-type: application/json

{
    "message": "Welcome to Elevator simulator. Go to /docs"
}
```