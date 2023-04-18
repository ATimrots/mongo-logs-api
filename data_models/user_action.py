import sys
sys.path.append('/var/www/mongo-log-api/enums/')

from typing import Union
from typing import Any
from typing import Dict
from datetime import datetime
from action import Action
from project import Project
from pydantic import BaseModel

class Payload(BaseModel):
    old: Union[Dict[str, Any], None] = None
    new: Union[Dict[str, Any], None] = None
    context: Union[Dict[str, Any], None] = None

class UserAction(BaseModel):
    admin_uuid: str
    model_uuid: Union[str, None] = None
    model_type: Union[str, None] = None
    action: Action
    payload: Union[Payload, None] = None
    ip_address: str
    time: datetime

    class Config:
        schema_extra = {
            "example": {
                "project": "b2b_platform",
                "admin_uuid": "435089ef-297a-45ee-8327-81ef319116d1",
                "model_uuid": "50568fc6-9757-4edb-9f93-65d71a95b27b",
                "model_type": "App\\Models\\Product",
                "action": "update",
                "payload": {"old": {"title": "Lāpstas kāts"}, "new": {"title": "Lāpstas kāts no koka"}},
                "ip_address": "127.0.0.1",
                "time": "2023-04-10T15:53:00+05:00"
            }
        }
