from fastapi import FastAPI

def valvelogic(a: str, b: str, op: str) -> dict[str, int]:
    result = eval(f"{a} {op} {b}")
    if result == 3:
        return {"we dont do that here": 69}
    else:
        return {"result": result}

app = FastAPI(
    title="My First FastAPI Application",
    description="A simple FastAPI application",
    version="0.1.0",
)

@app.get("/")
def read_home() -> dict[str, str]:
    return {"message": "Welcome to my FastAPI application!"}

@app.get("/hello/{name}")
def say_name(name: str) -> dict[str, str]:
    return {"message": f"Hello, {name}"}

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}

'''@app.get("/mathvalve/add/{a}/{b}")
def add_numbers(a: int, b: int) -> dict[str, int]:
    return valvelogic(str(a), str(b), "+")'''

@app.get("/mathvalve/{op}/{a}/{b}")
def evaluate_operation(a: int, b: int, op: str) -> dict[str, int]:
    op_dict = {
        "add": "+",
        "subtract": "-",
        "multiply": "*",
        "divide": "/"
    }
    if op in op_dict:
        return valvelogic(str(a), str(b), op_dict[op])
    else:
        return {"error": "Invalid operation"}