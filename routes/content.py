from typing import List
from fastapi import APIRouter
from fastapi.params import Depends, Query, Body, Path
from sqlalchemy.orm import Session

from constants.custom_types import RoleEnum, AgentTypeEnum
from routes import get_db_session, Authorize
from schemas.content import CountrySchema, StateSchema, CitySchema, BusinessCategorySchema, MarketSchema
from schemas.shared import ResponsibleAgentSchema, CompanyGenericSchema
from services.content.content import ContentService

router = APIRouter(prefix='/content')


@router.post('/countries', response_model=List[CountrySchema])
async def add_countries(countries: List[CountrySchema], session: Session = Depends(get_db_session),
                        authorized_user=Depends(Authorize(RoleEnum.admin))):
    countries_list = ContentService(session=session).geo_service.add_countries(countries=countries)
    return countries_list


@router.get('/countries', response_model=List[CountrySchema])
async def list_countries(session: Session = Depends(get_db_session)):
    countries_list = ContentService(session=session).geo_service.get_all_countries()
    return countries_list


@router.post('/countries/{countryId}/states', response_model=List[StateSchema])
async def add_states(country_id: int = Path(..., alias="countryId"), countries: List[StateSchema] = Body(...),
                     session: Session = Depends(get_db_session),
                     authorized_user=Depends(Authorize(RoleEnum.admin))):
    states_list = ContentService(session=session).geo_service.add_states(country_id=country_id, states=countries)
    return states_list


@router.get('/countries/{countryId}/states', response_model=List[StateSchema])
async def get_states_by_country(country_id: int = Path(..., alias="countryId"),
                                session: Session = Depends(get_db_session)):
    states_list = ContentService(session=session).geo_service.get_states_by_country(country_id)
    return states_list


@router.get('/states', response_model=List[StateSchema])
async def get_all_states(session: Session = Depends(get_db_session)):
    states_list = ContentService(session=session).geo_service.get_all_states()
    return states_list


@router.post('/states/{stateId}/cities', response_model=List[CitySchema])
async def add_cities(state_id: int = Path(..., alias="stateId"), cities: List[CitySchema] = Body(...),
                     session: Session = Depends(get_db_session),
                     authorized_user=Depends(Authorize(RoleEnum.admin))):
    cities_list = ContentService(session=session).geo_service.add_cities(state_id=state_id, cities=cities)
    return cities_list


@router.get('/states/{stateId}/cities', response_model=List[CitySchema])
async def get_cities_by_states(state_id: int = Path(..., alias="stateId"), session: Session = Depends(get_db_session)):
    cities_list = ContentService(session=session).geo_service.get_cities_by_state(state_id)
    return cities_list


@router.get('/cities', response_model=List[CitySchema])
async def get_all_cities(session: Session = Depends(get_db_session)):
    cities_list = ContentService(session=session).geo_service.get_all_cities()
    return cities_list


@router.post('/businessCategories', response_model=List[BusinessCategorySchema])
async def add_business_categories(business_categories: List[BusinessCategorySchema],
                                  session: Session = Depends(get_db_session),
                                  authorized_user=Depends(Authorize(RoleEnum.admin))):
    categories_list = ContentService(session=session).add_business_categories(business_categories=business_categories)
    return categories_list


@router.get('/businessCategories', response_model=List[BusinessCategorySchema])
async def get_all_business_categories(session: Session = Depends(get_db_session)):
    categories_list = ContentService(session=session).get_all_business_categories()
    return categories_list


@router.post('/markets', response_model=List[MarketSchema])
async def add_markets(markets: List[BusinessCategorySchema],
                      session: Session = Depends(get_db_session),
                      authorized_user=Depends(Authorize(RoleEnum.admin))):
    markets_list = ContentService(session=session).add_markets(markets=markets)
    return markets_list


@router.get('/markets', response_model=List[MarketSchema])
async def get_all_markets(session: Session = Depends(get_db_session)):
    markets_list = ContentService(session=session).get_all_markets()
    return markets_list


@router.get('/agents', response_model=List[ResponsibleAgentSchema])
async def get_agents(agent_type: AgentTypeEnum = Query(None, alias="agentType"),
                     session: Session = Depends(get_db_session),
                     authorized_user=Depends(Authorize())):
    agents_list = ContentService(session=session).get_agents(agent_type, authorized_user)
    return agents_list


@router.get('/companies', response_model=List[CompanyGenericSchema])
async def get_companies(session: Session = Depends(get_db_session),
                        authorized_user=Depends(Authorize())):
    agents_list = ContentService(session=session).get_companies(authorized_user)
    return agents_list
