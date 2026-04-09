from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from scalar_fastapi import AgentScalarConfig, get_scalar_api_reference
from starlette.middleware.cors import CORSMiddleware

from src.api import api_router
from src.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return route.name


# if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
#     sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    generate_unique_id_function=custom_generate_unique_id,
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


# fmt: off
hidden_clients = [
    "c", "clojure", "csharp", "dart", "fsharp", "go", "http", "java", "axios", "ofetch",
    "jquery", "xhr", "kotlin", "node", "objc", "ocaml", "php", "powershell", "python",
    "r", "ruby", "rust", "swift", "httpie", "wget",
]
# fmt: on


@app.get("/docs", include_in_schema=False)
async def scalar_html() -> HTMLResponse:
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title=f"{settings.PROJECT_NAME} - Documentation",
        scalar_proxy_url="https://proxy.scalar.com",
        agent=AgentScalarConfig(disabled=True),
        show_developer_tools="never",
        hidden_clients=hidden_clients,
        hide_client_button=True,
    )


@app.get("/openapi.json", include_in_schema=False)
async def openapi() -> dict[str, Any]:
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title, version=app.version, routes=app.routes
        )

    return app.openapi_schema
