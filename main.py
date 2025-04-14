from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware  # ✅ Import ajouté
from openai_client import create_thread, send_message, wait_for_run_completion, get_response

app = FastAPI()

# Servir les fichiers statiques (JS, CSS)
app.mount("/static", StaticFiles(directory="public"), name="static")

# Autorise les requêtes cross-origin (ex : frontend HTML sur un autre domaine ou Railway static)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tu pourras restreindre à ton domaine plus tard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_index():
    return FileResponse("public/index.html")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    if not user_input:
        return {"error": "Message manquant"}

    # Création d’un nouveau thread
    thread_id = create_thread()

    # Envoi du message utilisateur
    run_id = send_message(thread_id, user_input)

    # Attente que le run soit terminé
    wait_for_run_completion(thread_id, run_id)

    # Récupération de la réponse générée
    response = get_response(thread_id)

    return {"response": response}
