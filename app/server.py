import aiohttp
import asyncio
import uvicorn
import random
from PIL import Image as pimage
from fastai	import *
from fastai.vision import *
from io	import BytesIO
from starlette.applications	import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import	HTMLResponse, JSONResponse, FileResponse, UJSONResponse
from starlette.staticfiles import StaticFiles
import base64

#export_file_url = 'https://www.dropbox.com/s/6bgq8t6yextloqp/export.pkl?raw=1'
export_file_url	= 'https://www.dropbox.com/s/u9lrwbiqajokr30/export.pkl?dl=1'
export_file_name = 'export.pkl'

classes	= ['black',	'grizzly', 'teddys']
path = Path(__file__).parent

app	= Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'],	allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

img_bytes = []

async def download_file(url, dest):
	if dest.exists(): return
	async with aiohttp.ClientSession() as session:
		async with session.get(url)	as response:
			data = await response.read()
			with open(dest,	'wb') as f:
				f.write(data)


async def setup_learner():
	await download_file(export_file_url, path /	export_file_name)
	try:
		learn =	load_learner(path, export_file_name)
		return learn
	except RuntimeError	as e:
		if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
			print(e)
			message	= "\n\nThis	model was trained with an old version of fastai	and	will not work in a CPU environment.\n\nPlease update the fastai	library	in your	training environment and export	your model again.\n\nSee instructions for 'Returning to	work' at https://course.fast.ai."
			raise RuntimeError(message)
		else:
			raise


loop = asyncio.get_event_loop()
tasks =	[asyncio.ensure_future(setup_learner())]
learn =	loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route('/')
async def homepage(request):
	html_file =	path / 'view' /	'index.html'
	return HTMLResponse(html_file.open().read())

@app.route('/analyze', methods=['POST'])	
async def analyze(request):
	img_data = await request.form()
	img_bytes =	await (img_data['file'].read())
	#img_array = bytearray(img_bytes)
	#img = open_image(BytesIO(img_bytes))
	img_bytes = BytesIO(img_bytes)

	#form = await request.form()
	#img_bytes = await form['file'].read()
	#img = pimage.open(BytesIO(img_bytes))

	#print("inpaiting...")

	#for	i in range(50, 150,	1):
	#	r =	random.randint(0,1)*255
	#	img_array[i] = r
		
	
	#img_bytes = bytes(img_array)
	#print('image array random!\n')

	#encoded_img = base64.encodebytes(img_array).decode('ascii')
	#print(encoded_img)
	#return JSONResponse(encoded_img)

	#pixels = img.load()
	#for	i in range(img.size[0]):
	#	for j in range(img.size[1]):
	#		r =	random.randint(0,1)*255
	#		pixels[i,j] = (r, r, r)

	#result_image = pimage.fromarray((img * 255).astype('uint8'))
	#img.save('tt.png')
	#return FileResponse('tt.png')

	#img_bytes = bytes(img_array)
	#print('image array random!\n')
	#return UJSONResponse(img_bytes)
	


	#prediction	= learn.predict(img)[0]
	#return	JSONResponse({'result':	str(prediction)})
	return	JSONResponse({'result':	'ok!'})

@app.route("/img2img", methods=['POST'])
async def img2img(request):
    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".png", delete=False) as FOUT:
        FOUT.write(img_bytes)
        return FileResponse(FOUT.name, media_type="image/png")


if __name__	== '__main__':
	if 'serve' in sys.argv:
		uvicorn.run(app=app, host='0.0.0.0', port=5000,	log_level="info")
