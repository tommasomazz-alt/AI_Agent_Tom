import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

# nel file .env abbiamo la chiave API per sfruttare Gemini AI, qui la carichiamo
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

parser = argparse.ArgumentParser(description="Chatbot")
# diciamo al parser della CLI di accettare un argument "user prompt" che è una stringa di testo
parser.add_argument("user_prompt", type=str, help="User prompt")

# diciamo al parser della CLI di accettare un flag "--verbose" da usare per visualizzare più dettagli tecnici nella console
# tornerà utile per i test, per verificare tutto il contesto, ma non si vuole usare sempre
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()

# diciamo di ricordare la lista di messaggi in modo che ogni risposta AI consideri tutta la conversazione
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

if api_key == None:
    raise RuntimeError("API Key not found")

client = genai.Client(api_key=api_key)

# la risposta di Gemini
response = client.models.generate_content(
    model = "gemini-2.5-flash", 
    contents = messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

# restituisci l'errore se la connessione con Gemini API non sta funzionando
if response.usage_metadata is  None:
    raise RuntimeError("failed API request before printing the tokens consumed")

# stampa i dettagli contestuali dell'interazione solo quando si usa il flag --verbose
if args.verbose == True:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

# stampa la risposta di Gemini se non ho function calls, altrimenti il contrario stampo solo le func calls
if response.function_calls is None:
    print("Response:")
    print(response.text)

elif isinstance(response.function_calls, list):
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")