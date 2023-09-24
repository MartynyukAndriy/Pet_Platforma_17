# from sqlalchemy.ext.asyncio import engine

from src.database.db import engine
from sqladmin import Admin, ModelView

from src.database.models import User, City, Country, MasterInfo, Admin as Administrator, SubscribePlan


# визначаємо зміст адмінки: якими моделями бази даних і якими полями хочемо керувати через адмінку:
class UserAdmin(ModelView, model=User):
    column_list = "__all__"
    column_searchable_list = [User.name]
    column_sortable_list = [User.user_id, User.user_role, User.country_id, User.city_id]
    column_default_sort = [(User.email, True), (User.name, False)]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

#
# class MasterInfoAdmin(ModelView, model=MasterInfo):
#     column_list = [MasterInfo.user_id, MasterInfo.name, MasterInfo.email]
#     column_searchable_list = [MasterInfo.name]
#     column_sortable_list = [MasterInfo.user_id]
#     column_default_sort = [(MasterInfo.email, True), (MasterInfo.name, False)]
#     can_create = True
#     can_edit = True
#     can_delete = False
#     can_view_details = True
#     can_export = True
#     name = "Master"
#     name_plural = "Masters"
#     icon = "fa-solid fa-user-gear"


class CityAdmin(ModelView, model=City):
    column_list = "__all__"
    column_searchable_list = [City.city_ukr]
    column_sortable_list = [City.city_id]
    column_default_sort = [(City.city_id, True), (City.city_ukr, False)]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
    name = "City"
    name_plural = "Cities"
    icon = "fa-solid fa-city"


class SubscribePlanAdmin(ModelView, model=SubscribePlan):
    column_list = "__all__"
    column_searchable_list = [SubscribePlan.subscribe_plan]
    column_sortable_list = [SubscribePlan.plan_id]
    column_default_sort = [(SubscribePlan.subscribe_plan, True), (SubscribePlan.plan_id, False)]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
    name = "Subscribe Plan"
    name_plural = "Subscribe Plans"
    icon = "fa-solid fa-file-invoice-dollar"


class CountryAdmin(ModelView, model=Country):
    column_list = "__all__"
    column_searchable_list = [Country.country_ukr]
    column_sortable_list = [Country.country_id]
    column_default_sort = [(Country.country_id, True), (Country.country_ukr, False)]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
    name = "Country"
    name_plural = "Countries"
    icon = "fa-solid fa-earth-americas"

#
# class AdministratorAdmin(ModelView, model=Administrator):
#     column_list = [Administrator.user_id, Administrator.name, Administrator.email]
#     column_searchable_list = [Administrator.name]
#     column_sortable_list = [Administrator.name]
#     column_default_sort = [(Administrator.email, True), (Administrator.name, False)]
#     can_create = True
#     can_edit = True
#     can_delete = False
#     can_view_details = True
#     can_export = True
#     name = "Administrator"
#     name_plural = "Administrators"
#     icon = "fa-solid fa-person-military-pointing"
