# Model serving tutorial

Deployment instructions:

1. Install virtualenv: `pip install virtualenv`

2. Create the new environment: `python3 -m venv env`

3. Activate the environment: `source env/bin/activate`

4. Install the dependencies: `pip install -r requirements.txt`

5. Start the server: `uvicorn main:app --reload`

6. Testing the service using a tool like Postman:

```
POST /predict HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

[
	{
		"credit_score": 713,
	    "country": "Spain",
	    "gender": "Female",
	    "age": 48,
	    "tenure": 1,
	    "balance": 163760.82,
	    "products_number": 1,
	    "credit_card": 0,
	    "active_member": 0,
	    "estimated_salary": 42117.90
	}
]
```