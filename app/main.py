from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, crud, database
from fastapi_keycloak import FastAPIKeycloak

app = FastAPI()

keycloak_openid = FastAPIKeycloak(
    server_url="https://keycloak-url",
    client_id="your-client-id",
    client_secret="your-client-secret",
    realm_name="your-realm",
)

@app.post("/tasks/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    return crud.create_task(db=db, task=task)

@app.get("/tasks/", response_model=list[schemas.TaskOut])
def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    tasks = crud.get_tasks(db=db, skip=skip, limit=limit)
    return tasks

@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: str, task: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    db_task = crud.update_task(db=db, task_id=task_id, task=task)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", response_model=schemas.TaskOut)
def delete_task(task_id: str, db: Session = Depends(database.get_db)):
    db_task = crud.delete_task(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.get("/health-check")
def health_check(db: Session = Depends(database.get_db)):
    try:
        # Test the database connection
        db.query(models.Task).first()
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
@app.get("/admin")
async def admin_area(user: dict = Depends(keycloak_openid.get_current_user)):
    if 'admin' not in user['roles']:
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"message": "Welcome, admin!"}