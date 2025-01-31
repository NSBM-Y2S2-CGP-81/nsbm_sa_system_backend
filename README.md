# NSBM Super App - System Backend

---
Currently available services thorugh API:

| Service                     | Status  |
|-----------------------------|---------|
| Basic User Auth and Login   | ✔       |
| API Key Generation          | ✔       |
| Oauthv2 Authentication      | ❌      |
| Access Point Count data     | ❌      |
| Database Access             | ➖       |

More Services yet to develop...

---

## How to run this?
1. Export Mongo DB server address and secret key.
```
For windows[CMD]-
set MONGO_URI=mongodb://localhost:27017/your_db
set JWT_SECRET_KEY=your_secret_key

For windows[PowerShell]-
$env:MONGO_URI="mongodb://localhost:27017/your_db"
$env:JWT_SECRET_KEY="your_secret_key"

For mac/linux
export MONGO_URI="mongodb://localhost:27017/your_db"
export JWT_SECRET_KEY="your_secret_key"
```
2. Install the requirements and run the server
```
pip install -r requirements.txt
python run.py
```


## How to use the API ?

### Testing the API

1. User Registration
```
curl -X POST http://127.0.0.1:5000/auth/register -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass"}'
```

2. User Login and receive token
```
curl -X POST http://127.0.0.1:5000/auth/login -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass"}'
```

3. Store Data
```
curl -X POST http://127.0.0.1:5000/data/store -H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" -d '{"key": "value"}'
```

4. Fetch Data
```
curl -X GET http://127.0.0.1:5000/data/fetch -H "Authorization: Bearer YOUR_TOKEN"
```
