#Importing FastAPI class from fastapi library to build an API and HTTPException for Error Handling
from fastapi import FastAPI,HTTPException

#This is a variable of type list to store our tasks temporarly
tasks = []

#creating an instance for FastAPI,this instance only handles the requests and sending the responses

app = FastAPI()

'''
creating an end point for POST request,This contains path,operation,decorator and function,
when someone hits the end point the associated function will be executed,here we used the function for creating new task
'''

@app.post("/tasks")  #This is the end point of POST request,which is created using decorator(@app)
def create_task(title: str,description: str = ""): #This is a function which asks two arguments(title,desc) from the client
    task_id = len(tasks) + 1 #assigning an id for each task to uniquely identifying each task
    task = {
                "id"            : task_id,
                "title"         : title,
                "description"   : description,
                "status"        : "pending"
                
            }   #we are creating a dictionary with key-values
    tasks.append(task) #adding the task to created list called task
    return task #we are returning the created task to the client

'''
creating an end point for GET request,which will gives all the tasks what are available as a response to the client
'''

@app.get("/tasks") #This is the end point for GET request
def get_tasks(): #This is a function,which gives a list of tasks available to client,when someone hit the end point of above
    return tasks #returning all the tasks


'''
creating an end point for GET request with specific id,which will gives a response as a specific task,
if that specific id not available then it results in erro
'''

@app.get("/tasks/{task_id}") #This is a dynamic routing with path-parameters for getting task by id
def get_task_by_id(task_id: int): #Function which asks for id which is of type integer
    for task in tasks: #for loop which loops through the tasks list
        if task["id"] == task_id: #checking for task_id Availability
            return task

    raise HTTPException(status_code=404,detail="Task not found")

'''
    creating an end point for PUT request,which will update the task as per client request,if not found raise an error
'''

@app.put("/tasks/{task_id}")  #This is a dynamic routing with path-parameters for updating the task
def update_task_by_id(task_id: int, title: str, description: str = "", status: str = "pending"):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = title
            task["description"] = description
            task["status"] = status
            return task

    raise HTTPException(status_code=404, detail="Task not found")
'''
    creating an end point for DELETE request,which will delete the task by id,if not found raise an error
'''

@app.delete("/tasks/{task_id}") #This is a dynamic routing with path-parameters for deleting the task by id
def delete_task_by_id(task_id: int): #This function accepts an id of a tsak to delete the task in tasks list
    for index,task in enumerate(tasks): #enumerate() gives the index of each iterable object(tasks list)
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)
            return deleted_task

    raise HTTPException(status_code=404,detail="Task not found")

