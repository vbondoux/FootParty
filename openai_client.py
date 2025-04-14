import os
import time
import openai

# Récupération des variables d’environnement injectées par Railway
openai.api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")

def create_thread():
    """Crée un nouveau thread de conversation avec l’assistant"""
    thread = openai.beta.threads.create()
    return thread.id

def send_message(thread_id: str, user_message: str):
    """Envoie un message utilisateur dans un thread et lance le run"""
    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )
    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )
    return run.id

def wait_for_run_completion(thread_id: str, run_id: str):
    """Boucle d’attente jusqu’à ce que le run soit terminé"""
    while True:
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            raise Exception("Run failed.")
        time.sleep(1)

def get_response(thread_id: str):
    """Récupère la dernière réponse du thread"""
    messages = openai.beta.threads.messages.list(thread_id=thread_id)
    if messages.data:
        return messages.data[0].content[0].text.value
    return "Aucune réponse générée par l’assistant."
