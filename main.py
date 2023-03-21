import os
 
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
 
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

content = ''
 
 
@app.post("/file/upload")
async def upload(file: UploadFile = File(...)):
    global content
    content = ''
    fn = file.filename
    save_path = f'./file/'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
 

    save_file = os.path.join(save_path, fn)
 
    f = open(save_file, 'wb')
    data = await file.read()
    f.write(data)
    f.close()
 
    import subprocess

    # 要执行的命令
    cmd = "extractpdf " + str(os.path.abspath(os.path.join(save_path, fn)))
    print(cmd)

    # 使用subprocess库调用命令
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 解码并打印标准输出
    out, err = proc.communicate()
    content = out.decode()
    print(content)
    
    return {"msg": f'{fn}上传成功', 'length': len(data)}

@app.get("/ask")
async def search(q: str):
    global content
    import subprocess
    if len(content.strip())==0:
        return "pdf 解析失败重试"
    cmd = 'chatgptqa "' + content +'" "' + q + '"' 
    print(cmd)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 解码并打印标准输出
    out, err = proc.communicate()
    
    ret = out.decode()
    ret = ret.replace('\n', '')
    return ret

 
if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0")

