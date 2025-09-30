# To run the client: 
Open your terminal and navigate to the root foder of ai-kb and run:
```
1. cd client
2. python3 -m venv venv
3. source venv/bin/activate 
4. pip install -r requirements.txt
5. flask --app ./ run --debug
```

To check if it is working, open a new terminal while client app is running:
run `curl http://127.0.0.1:5000/healthz`
the system should return:
```
{
  "ok": "true"
}
```