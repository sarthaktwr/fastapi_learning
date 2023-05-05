import cv2
from enum import Enum
from typing import Union
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, FileResponse


file_path = '5.jpg'
# cap = cv2.VideoCapture('1.mp4')
app = FastAPI()
templates = Jinja2Templates(directory = 'templates')
fake_items_db = [{'name': 'jiojas', 'name': 'djfnsjifnis', 'name': 'wqapflk', 'name': 'njnfiabfsabdias'}]

#################################
#		# Reading Frames		#
#################################

def frame_read():

	while True:
		ret, frame = cap.read()
		if ret:
			success, buffer = cv2.imencode('.jpg', frame)
			frame = buffer.tobytes()
			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')			
		else:
			break

#################################
#		# Video Streaming		#
#		# Image Display			#
#################################	
@app.get('/')
def index(request: Request):
	return templates.TemplateResponse('index.html', {'request': request})

@app.get('/video_feed')
def video_feed():
	return StreamingResponse(frame_read(), media_type= 'multipart/x-mixed-replace; boundary=frame')

@app.get('/img_display')
def display_img():
	return FileResponse(file_path)

#################################
#		# Basic Commands		#
#################################

@app.get('/')
def read_root():
	return {'hello', 'world'}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
	return {"item_id": item_id, "q": q}

@app.get('/users/hi')
def read_user_hi():
	return {'user_id': 'current user id'}

@app.get('/users/{user_id}')
def read_user(user_id: str):
	return {'user_id': user_id}

class models(str, Enum):
	alexnet = 'alexnet'
	lenet = 'lenet'
	cnn = 'cnn'
	resnet = 'resnet'

@app.get('/models')
def models_desc():
	return 'The deep learning models are given in another api'

@app.get('/models/{model_name}')
def models_name(model_name: str):
	l = [models.alexnet.value, models.cnn.value, models.resnet.value, models.lenet.value]
	if model_name in l:
		return {'model_name': model_name}
	else:
		return f'Please enter a choose from the model list {l[0], l[1], l[2], l[3]}'

@app.get('/files/{file_path: path}')
def read_file(file_path: str):
	return {'file_path': file_path}

@app.get('/items/')
def read_items(skip: int = 0, limit = 23):
	return fake_items_db[skip: limit]

@app.get('/items/{item_id}')
def get_items(item_id: str, q: Union[str, None] = None):
	if q:
		return {'item_id': item_id, 'q': q}

	return {'item_id': item_id}