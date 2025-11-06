from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles as BaseStaticFiles

import schemas
import services

class StaticFiles(BaseStaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        if path.endswith(('.woff2', '.woff', '.ttf', '.eot', '.svg')):
            if path.endswith('.woff2'):
                response.headers['content-type'] = 'font/woff2'
            elif path.endswith('.woff'):
                response.headers['content-type'] = 'font/woff'
            elif path.endswith('.ttf'):
                response.headers['content-type'] = 'font/ttf'
            elif path.endswith('.eot'):
                response.headers['content-type'] = 'application/vnd.ms-fontobject'
            elif path.endswith('.svg'):
                response.headers['content-type'] = 'image/svg+xml'
            response.headers['cache-control'] = 'no-cache'
        return response

app = FastAPI(
    title="RoastMaster AI",
    description="An API and web app to roast names using AI.",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the homepage with a GUI to interact with the API."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Simple health check endpoint to confirm the API is running.
    """
    return {"status": "ok"}

@app.post("/api/roast", response_model=schemas.RoastResponse, status_code=status.HTTP_200_OK)
async def api_create_roast(roast_request: schemas.RoastRequest):
    """
    API endpoint to get a roast for a name via POST request with a JSON body.
    """
    return await get_roast_logic(roast_request.name)

@app.get("/api/{name}", response_model=schemas.RoastResponse, status_code=status.HTTP_200_OK)
async def api_get_roast(name: str):
    """
    API endpoint to get a roast for a name via GET request with a path parameter.
    """
    return await get_roast_logic(name)

async def get_roast_logic(name: str):
    """
    API endpoint to get a roast for a name.
    It handles caching and queues requests to an external AI service.
    """
    try:
        roast_result = services.get_roast_for_name(name)

        if "Error:" in roast_result or "An unexpected error occurred:" in roast_result:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=roast_result
            )

        return schemas.RoastResponse(roast=roast_result)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error occurred: {str(e)}"
        )