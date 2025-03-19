from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from app.api import create_question_session_endpoint
from app.api import evaluate_question_session_endpoint
from app.api import user_details_endpoint

app = FastAPI()

app.include_router(create_question_session_endpoint.router)
app.include_router(evaluate_question_session_endpoint.router)
app.include_router(user_details_endpoint.router)

# Mount the static directory
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html>
        <head>
            <title>Welcome to DG</title>
        </head>
        <body style="text-align:center; font-family: Arial, sans-serif; margin-top: 50px;">
            <img src="/static/logo.png" alt="Logo"  height="100" />
            <h1>Welcome to the Cognitive Health Improving Exercises Component!</h1>
            <p></p>
        </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)