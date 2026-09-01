import re

with open("web_prototype/server.py", "r") as f:
    content = f.read()

imports_to_add = """
import requests
import urllib.parse
from gtts import gTTS
"""

content = content.replace("from fastapi.templating import Jinja2Templates", "from fastapi.templating import Jinja2Templates\n" + imports_to_add)

models_to_add = """
class GenerateImageRequest(BaseModel):
    prompt: str
    seed: Optional[int] = None

class GenerateAudioRequest(BaseModel):
    script: str
"""
content = content.replace("class SingleTxSimRequest(BaseModel):", models_to_add + "\nclass SingleTxSimRequest(BaseModel):")

endpoints_to_add = """
@app.post("/api/generate/image")
async def generate_image(req: GenerateImageRequest):
    try:
        encoded_prompt = urllib.parse.quote(req.prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"
        if req.seed:
            url += f"&seed={req.seed}"
            
        res = requests.get(url, timeout=20)
        if res.status_code == 200:
            filename = f"gen_img_{uuid.uuid4().hex[:8]}.jpg"
            assets_dir = os.path.join(STATIC_DIR, "assets")
            os.makedirs(assets_dir, exist_ok=True)
            filepath = os.path.join(assets_dir, filename)
            with open(filepath, "wb") as f:
                f.write(res.content)
            return JSONResponse(content={"url": f"/static/assets/{filename}", "status": "success"})
        return JSONResponse(content={"error": "Image generation failed"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/api/generate/audio")
async def generate_audio(req: GenerateAudioRequest):
    try:
        tts = gTTS(text=req.script, lang="en", slow=False)
        filename = f"gen_audio_{uuid.uuid4().hex[:8]}.mp3"
        assets_dir = os.path.join(STATIC_DIR, "assets")
        os.makedirs(assets_dir, exist_ok=True)
        filepath = os.path.join(assets_dir, filename)
        tts.save(filepath)
        return JSONResponse(content={"url": f"/static/assets/{filename}", "status": "success"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
"""
content = content.replace("if __name__ == \"__main__\":", endpoints_to_add + "\nif __name__ == \"__main__\":")

with open("web_prototype/server.py", "w") as f:
    f.write(content)
