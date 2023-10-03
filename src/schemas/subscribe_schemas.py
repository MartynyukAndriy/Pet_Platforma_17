from pydantic import BaseModel, Field


class SubscribeModel(BaseModel):
    subscribe_plan: str = Field(min_length=2)
    plan_period: int


class SubscribeResponse(BaseModel):
    plan_id: int = 1
    subscribe_plan: str = 'MasterGold'
    plan_period: int = 30

    class Config:
        from_attributes = True

