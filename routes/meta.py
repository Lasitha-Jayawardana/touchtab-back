from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from routes import get_db_session, Authorize
from schemas.common import MetaSchema
from services.meta_service import MetaService

router = APIRouter(prefix="/meta", tags=["meta"],
                   # dependencies=[Depends(Authorize())]
                   )


@router.get("/foodCategories",response_model=List[MetaSchema])
async def get_all_food_categories(
        session: Session = Depends(get_db_session)
):
    response = MetaService(session).get_all_food_categories()
    return response

#
# @router.get("/specialization")
# async def get_all_specializations(
#         session: Session = Depends(get_db_session)
# ):
#     response = MetaService(session).get_all_specializations()
#     return response
#
#
# @router.get("/report-options")
# async def get_all_report_options(
#         session: Session = Depends(get_db_session)
# ):
#     response =   MetaService(session).get_report_options()
#     return response
