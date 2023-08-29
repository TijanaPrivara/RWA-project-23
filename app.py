import security
import database
import models
from fastapi import FastAPI, Depends, HTTPException, Form, Path, Body, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import List
from models import TaskDb, TaskIn, UserDb, ProjectIn, ProjectDb
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.on_event("startup")
async def startup_db_client():
    await database.init_db()

### API: Auth & Users ###

@app.get("/users/me")
async def get_me(current_user: dict = Depends(security.get_current_user)):
    return current_user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    return await security.login(form.username, form.password)

@app.post("/register/user", response_model=models.UserDb)
async def register_user(
    user: models.UserIn = Body(...),
    current_user: dict = Depends(security.get_current_user),
):
    if not security.is_valid_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    hashed_password = security.hash_password(user.password)
    user_db = models.UserDb(
        _id=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )

    new_user = await database.db["users"].insert_one(jsonable_encoder(user_db))
    created_user = await database.db["users"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)

### API: Task ###

@app.post("/tasks", response_model=TaskDb)
async def create_task(
    task_in: TaskIn,
    current_user: UserDb = Depends(security.get_current_user),
):
    created_task = await database.save_task(task_in)
    return created_task

@app.get("/tasks", response_model=List[models.TaskDb])
async def list_tasks(current_user: UserDb = Depends(security.get_current_user)):
    tasks = await database.list_tasks()
    return tasks

@app.put("/tasks/{task_id}/status")
async def update_task_status_endpoint(
    task_id: str,
    new_status: str,
    current_user: UserDb = Depends(security.get_current_user)
):
    updated_task = await database.perform_update_task_status(task_id, new_status)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str, current_user: UserDb = Depends(security.get_current_user)):
    deleted_task = await database.delete_task(task_id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task

### API: Project ###

@app.post("/projects/", response_model=ProjectDb)
async def create_project_endpoint(project_in: ProjectIn, current_user: UserDb = Depends(security.get_current_user)):
    created_project_result = await database.create_project(project_in)
    return created_project_result

@app.get("/projects", response_model=List[models.ProjectDb])
async def list_projects(current_user: UserDb = Depends(security.get_current_user)):
    projects = await database.list_projects()
    return projects