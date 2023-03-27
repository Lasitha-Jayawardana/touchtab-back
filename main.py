from urllib.request import Request

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from starlette import status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response, RedirectResponse

from routes import get_db_session,  authentication
from utilities.exceptions import exception_handlers, HTTPException
from utilities.logger import logger

tags_metadata = [

    # {
    #     "name": "Authentication Endpoint",
    #     "description": "Authenticates users",
    # },
    # {
    #     "name": "User Endpoint",
    #     "description": "Operations with admins/sales agents.",
    # },
    # {
    #     "name": "Company Endpoint",
    #     "description": "Operations with company",
    # },
    # {
    #     "name": "Content Endpoint",
    #     "description": "All meta contents",
    # },
    # {
    #     "name": "GoogleAds Endpoint",
    #     "description": "Operations with googleads ads services",
    # },
]

app = FastAPI(title="Touchtab", version="1.0.0", openapi_tags=tags_metadata,
              exception_handlers=exception_handlers, dependencies=[Depends(get_db_session)])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    logger.exception(exc)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"code": 'CRM_422',
                 "message": "Request validation error",  # exc.errors()
                 "description": "Invalid field or value in the request."  # exc.body
                 }
    )


# _lookup_exception_handler
@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    logger.exception(exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code,
                 "message": exc.message,
                 "description": exc.description
                 }
    )


# capture all unhandled exceptions (internal server error)
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.debug(exc)
        return Response("Internal server error", status_code=500)


app.middleware('http')(catch_exceptions_middleware)

app.include_router(authentication.router, prefix="/api", tags=["Auth Endpoint"])
# app.include_router(fund_admin.router, prefix="/api", tags=["Fund Admin Endpoint"])
# app.include_router(investor.router, prefix="/api", tags=["Investor Endpoint"])
# app.include_router(investor_admin.router, prefix="/api", tags=["Investor Admin Endpoint"])
# app.include_router(super_admin.router, prefix="/api", tags=["Super Admin Endpoint"])
# app.include_router(fund_user.router, prefix="/api", tags=["Fund USer Endpoint"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("")
async def root():
    return


@app.get("/")
async def eb_health():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Investwell API. 2023"},
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000, reload=False)
