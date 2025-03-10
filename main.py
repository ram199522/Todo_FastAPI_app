#Importing FastAPI class from fastapi library to build an API and HTTPException for Error Handling
from fastapi import FastAPI,HTTPException
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient


#creating an instance for FastAPI,this instance only handles the requests and sending the responses

app = FastAPI()

client = "mongodb://127.0.0.1:27017"
db = client.todo_db
tasks_collection = db.todo_db


'''
creating an end point for POST request,This contains path,operation,decorator and function,
when someone hits the end point the associated function will be executed,here we used the function for creating new task
'''

@app.post("/tasks")  #This is the end point of POST request,which is created using decorator(@app)
async def create_task(task:dict): #This is a function which asks tasK:dict from the client
    if "title" not in task or "description" not in task:
        raise HTTPException(status_code=404,detail="Missing 'title' or 'description' ")


    new_task = {
                "title"         : task["title"],
                "description"   : task["description"],
                "status"        : "pending"
                
            }   #we are creating a dictionary with key-values

    result = await tasks_collection.insert_one(new_task)
    new_task["_id'] = str(result.inserted_id)
    return new_task #we are returning the created task to the client

'''
creating an end point for GET request,which will gives all the tasks what are available as a response to the client
'''

@app.get("/tasks") #This is the end point for GET request
async def get_tasks(): #This is a function,which gives a list of tasks available to client,when someone hit the end point of above
    tasks = await tasks_collection.find().to_list(50)
    for task in tasks:
        task["_id"] = str(task["_id"])

    return tasks #returning all the tasks


'''
creating an end point for GET request with specific id,which will gives a response as a specific task,
if that specific id not available then it results in erro
'''

@app.get("/tasks/{task_id}") #This is a dynamic routing with path-parameters for getting task by id
async def get_task_by_id(task_id: str): #Function which asks for id which is of type str
    task = await tasks_collection.find_one({"_id":ObjectId(task_id)})
        if not task: #checking for task_id Availability
            raise HTTPException(status_code=404,detail="Task not found")
    task["_id"] = str(task["_id"])
    return task

'''
    creating an end point for PUT request,which will update the task as per client request,if not found raise an error
'''

@app.put("/tasks/{task_id}")  #This is a dynamic routing with path-parameters for updating the task
async def update_task_by_id(task_id: str, updated_task:dict):
    result = await tasks_collection.update_one({"_id":ObjectId(task_id),{"$set":updated_task}})

    if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
 
    return {"message" : "Task Updated Successfully"}

'''
    creating an end point for DELETE request,which will delete the task by id,if not found raise an error
'''

@app.delete("/tasks/{task_id}") #This is a dynamic routing with path-parameters for deleting the task by id
def delete_task_by_id(task_id: int): #This function accepts an id of a tsak to delete the task in tasks list
    result = await tasks_collection.delete_one({"_id":ObjectId(task_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404,detail="Task not found")

    return {"message" : "Deleted the task Successfully"}

