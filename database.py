import models
import security
import uuid
import os
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from models import  TaskIn
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List

load_dotenv()

mongo_uri = os.getenv("MONGODB_URI")
mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
db = mongodb_client["fastapi_task_db"]
tasks_collection = db["tasks"]


async def init_db():
    print("Connected to the MongoDB database!")

### User ###

async def get_user(username: str, password: str = None):
    document = await db["users"].find_one({"_id": username})
    print(f'database.get_user({username}, {password}): {document}')
    if document:
        user = models.UserDb(**document)
        if password:
            if security.verify_password(password, user.hashed_password):
                return user
        else:
            return user
        
 ### Task ###

async def create_task(task_in: models.TaskIn):
    user_id = str(uuid.uuid4())
    task_db = models.TaskDb(
        _id=user_id,
        title=task_in.title,
        description=task_in.description,
        priority=task_in.priority,
        status=task_in.status,
        due_date=task_in.due_date,
        project_name=task_in.project_name
    )
    new_task = await db["tasks"].insert_one(jsonable_encoder(task_db))
    created_task = await db["tasks"].find_one({"_id": new_task.inserted_id})

    created_task["_id"] = str(created_task["_id"])
    return created_task

async def save_task(task_in: TaskIn):
    user_id = str(uuid.uuid4())
    task_db = models.TaskDb(
        _id=user_id,
        title=task_in.title,
        description=task_in.description,
        priority=task_in.priority,
        status=task_in.status,
        due_date=task_in.due_date,
        project_name=task_in.project_name
    )
    new_task = await db["tasks"].insert_one(jsonable_encoder(task_db))
    created_task = await db["tasks"].find_one({"_id": new_task.inserted_id})

    created_task["_id"] = str(created_task["_id"])
    return created_task

async def update_task_status(task_id: str, new_status: str):
    updated_task = await db["tasks"].find_one_and_update(
        {"_id": task_id},
        {"$set": {"status": new_status}},
        return_document=True
    )
    return updated_task

async def perform_update_task_status(task_id: str, new_status: str):
    updated_task = await update_task_status(task_id, new_status)
    return updated_task

async def delete_task(task_id: str):
    deleted_task = await db["tasks"].find_one_and_delete({"_id": task_id})
    return deleted_task

async def list_tasks():
    tasks = []
    async for task in db["tasks"].find():
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return tasks

### Project ###

async def create_project(project_in: models.ProjectIn):
    project_id = str(uuid.uuid4())
    project_db = models.ProjectDb(
        _id=project_id,
        name=project_in.name,
        description=project_in.description
    )

    new_project = await db["projects"].insert_one(jsonable_encoder(project_db))
    created_project = await db["projects"].find_one({"_id": new_project.inserted_id})

    created_project["_id"] = str(created_project["_id"])
    return created_project

async def list_projects():
    projects = []
    async for project in db["projects"].find():
        project["_id"] = str(project["_id"])
        projects.append(project)
    return projects