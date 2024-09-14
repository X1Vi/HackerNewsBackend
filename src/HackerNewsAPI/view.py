from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware
import threading

app = FastAPI()

origins = [
    "http://localhost:5173" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def getStoryDataThread(story: str, toAppendStoriesArray: list):
    story_obj_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story}.json?print=pretty")    
    if story_obj_response.status_code == 200:
        toAppendStoriesArray.append(story_obj_response.json())
    print("Thread Destroyed")

def threadingStoriesRequest(stories: list, toAppendStoriesArray: list):
    for story in stories:
        storyThread = threading.Thread(target=getStoryDataThread, args=(story, toAppendStoriesArray))
        storyThread.run()


@app.get("/")
async def getTopHackerNew():
    try:
        response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
        
        if response.status_code != 200:
            return {"error": "Hacker New API isnt working"}

        stories = response.json()
        stories = list(stories)
        stories = stories[:10]
        
        
    
        stories_arr = []
        
        threadingStoriesRequest(stories=stories, toAppendStoriesArray=stories_arr)
                
        return {"stories": stories_arr}
        
    except Exception as e:
        return {"e": str(e)}