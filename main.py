# import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI

# from fastapi_limiter import FastAPILimiter
# from src.conf.config import settings
# from sqladmin import Admin

# from src.database.db import engine
from src.routes import auth, users, countries, cities, currency


# Створюємо екземпляр FastApi, встановлюємо назву додатка у swagger та відсортуємо роути по методах:
# from src.services.admin_panel.admin_panel import UserAdmin, CityAdmin, CountryAdmin, SubscribePlanAdmin

app = FastAPI(swagger_ui_parameters={"operationsSorter": "method"}, title='Platforma17 app')

# підключаємо адмінку
# http://localhost:8001/admin/
# admin = Admin(app, engine)
# admin.add_view(UserAdmin)
# admin.add_view(CountryAdmin)
# admin.add_view(CityAdmin)
# admin.add_view(SubscribePlanAdmin)


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
app.include_router(countries.router, prefix='/api')
app.include_router(cities.router, prefix='/api')
app.include_router(currency.router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
