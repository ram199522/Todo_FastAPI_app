#Importing FastAPI class from fastapi library to build an API and HTTPException for Error Handling
from fastapi import FastAPI,HTTPException,Body
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient


#creating an instance for FastAPI,this instance only handles the requests and sending the responses

app = FastAPI()

client =AsyncIOMotorClient("mongodb://127.0.0.1:27017")
db = client.todo_db
tasks_collection = db.todo


'''
creating an end point for POST request,This contains path,operation,decorator and function,
when someone hits the end point the associated function will be executed,here we used the function for creating new task
'''

@app.post("/tasks")  #This is the end point of POST request,which is created using decorator(@app)
async def create_task(task: dict): #This is a function which asks tasK:dict from the client
    if "title" not in task or "description" not in task:
        raise HTTPException(status_code=404,detail="Missing 'title' or 'description' ")


    new_task = {
                "title"         : task["title"],
                "description"   : task["description"],
                "status"        : "pending"
                
            }   #we are creating a dictionary with key-values

    result = await tasks_collection.insert_one(new_task)
    new_task["_id"] = str(result.inserted_id)
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
    object_id = ObjectId(task_id)  # Convert string to ObjectId
    task = await tasks_collection.find_one({"_id": object_id})
     
    if task: #checking for task_id Availability
        task["_id"] = str(task["_id"])
        return task

    raise HTTPException(status_code=404,detail="Task not found")
'''
    creating an end point for PUT request,which will update the task as per client request,if not found raise an error
'''

@app.put("/tasks/{task_id}")  #This is a dynamic routing with path-parameters for updating the task
async def update_task_by_id(task_id: str, updated_task:dict):
    object_id = ObjectId(task_id)  # Convert string to ObjectId
    result = await tasks_collection.update_one({"_id":object_id},{"$set":updated_task})

    if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Task not found or not modifief")
 
    return {"message" : "Task Updated Successfully"}

'''
    creating an end point for DELETE request,which will delete the task by id,if not found raise an error
'''

@app.delete("/tasks/{task_id}") #This is a dynamic routing with path-parameters for deleting the task by id
async def delete_task_by_id(task_id: str): #This function accepts an id of a tsak to delete the task in tasks list
    object_id = ObjectId(task_id)  # Convert string to ObjectId
    result = await tasks_collection.delete_one({"_id":object_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404,detail="Task not found")

    return {"message" : "Deleted the task Successfully"}

