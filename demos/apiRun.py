import sys

import uvicorn
from fastapi import FastAPI, applications
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="标题", description="描述", version='1.0.0')

# def swagger_monkey_patch(*args, **kwargs):
#     return get_swagger_ui_html(
#         *args, **kwargs,
#         swagger_js_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js',
#         swagger_css_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css',
        
#     )

# applications.get_swagger_ui_html = swagger_monkey_patch
    

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许访问的源
        allow_credentials=True,  # 支持 cookie
        allow_methods=["*"],  # 允许使用的请求方法
        allow_headers=["*"]  # 允许携带的 Headers
    )

app.mount("/templates",
            StaticFiles(directory="/templates"),
            name="templates")

@app.get("/", response_class=HTMLResponse)
async def index():
    return RedirectResponse(url="/templates/index.html")



@app.get("/stop")
def stopApi():
    import os
    os._exit(0)

@app.on_event('startup')
def startup():
    pass

@app.on_event('shutdown')
def shutdown():
    pass

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
