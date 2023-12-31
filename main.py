# import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI

# from fastapi_limiter import FastAPILimiter
from src.conf.config import settings
from sqladmin import Admin

from src.database.db import create_async_engine

from src.routes import auth, users, countries, cities, currencies, services, service_categories, masters


engine = create_async_engine(settings.sqlalchemy_database_url)


# Створюємо екземпляр FastApi, встановлюємо назву додатка у swagger та відсортуємо роути по методах:
from src.services.admin_panel.admin_panel import UserAdmin, MasterInfoAdmin, CityAdmin, CountryAdmin, \
    SubscribePlanAdmin, UserResponseAdmin, ServiceAdmin, ServiceCategoryAdmin

app = FastAPI(swagger_ui_parameters={"operationsSorter": "method"}, title='Platforma17 app')

# підключаємо адмін-панель
# http://localhost:8001/admin/
admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(MasterInfoAdmin)
admin.add_view(CountryAdmin)
admin.add_view(CityAdmin)
admin.add_view(SubscribePlanAdmin)
admin.add_view(UserResponseAdmin)
admin.add_view(ServiceCategoryAdmin)
admin.add_view(ServiceAdmin)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}


# @app.on_event("startup")
# async def startup():
#     r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, password=settings.redis_password,
#     encoding="utf-8", db=0)
#     await FastAPILimiter.init(r)

app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(masters.router, prefix='/api')
app.include_router(countries.router, prefix='/api')
app.include_router(cities.router, prefix='/api')
app.include_router(currencies.router, prefix='/api')
app.include_router(services.router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)