from pydantic import BaseModel
from typing import Any
from datetime import datetime

class ResponseModel(BaseModel):
    folio: str = datetime.now().strftime("%Y%m%d%H%M%S")

class ResponseSuccess(ResponseModel):
    message: str = "Success"
    result: Any = "data"

class ResponseFailure(ResponseModel):
    message: str = "Fail"
    detail: Any = "something went wrong"

class ResponseWarning(ResponseModel):
    message: str = "Warning"
    detail: Any = "something went wrong"
    
    
# from fastapi import FastAPI, Request, status
# from fastapi.responses import JSONResponse

# from datetime import datetime

# app = FastAPI()


# class ExceptionResponse:
#     def __init__(self, **kwargs):
#         self.status_code = kwargs.get("status_code")
#         self.data = kwargs.get("data")

# class ExceptionResponseFail(ExceptionResponse):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#     def __str__(self):
#         return self.data.get("detail")
    
# class ExceptionResponseSuccess(ExceptionResponse):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#     def __str__(self):
#         return self.data.get("result")
    
# class ExceptionResponseWarning(ExceptionResponse):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
        
#     def __str__(self):
#         return self.data.get("detail")

# @app.exception_handler(ExceptionResponseSuccess)
# async def exception_handler_fail(request: Request, exc: ExceptionResponseSuccess):
#     return await JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content={
#             "message": "ERROR",
#             "folio": f"{datetime.now().strftime('%Y%m%d%H%M%S')}",
#             "detail": str(exc),
#         },
#     )

# @app.exception_handler(ExceptionResponseWarning)
# async def exception_handler_warninig(request: Request, exc: ExceptionResponseWarning):
#     return await JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={
#             "message": "WARNING",
#             "folio": f"{datetime.now().strftime('%Y%m%d%H%M%S')}",
#             "detail": str(exc),
#         },
#     )

# @app.exception_handler(ExceptionResponseSuccess)
# async def exception_handler_success(request: Request, exc: ExceptionResponseSuccess):
#     return await JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content={
#             "message": "SUCCESS",
#             "folio": f"{datetime.now().strftime('%Y%m%d%H%M%S')}",
#             "result": str(exc),
#         },
#     )
