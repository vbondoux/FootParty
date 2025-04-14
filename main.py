from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai_client import create_thread, send_message, wait_for_run_completion, get_response

app = FastAPI()

# Autorise les requêtes cross-origin (ex : frontend React sur un autre domaine)
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
