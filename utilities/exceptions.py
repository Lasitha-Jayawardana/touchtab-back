from fastapi.responses import JSONResponse


class HTTPException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.code = message[0]
        self.message = message[1]
        self.description = message[2]


async def unauthorized_error(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": 'CRM_401',
                 "message": 'Not authenticated',
                 "description": 'Authentication header not found'
                 }
    )


async def not_found_error(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": 'CRM_404',
                 "message": 'Not found',
                 "description": 'Path not found'
                 }
    )


# _status_handlers
exception_handlers = {
    401: unauthorized_error,
    404: not_found_error,
}
