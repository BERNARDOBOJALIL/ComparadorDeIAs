import os
import time
import json
import dotenv
from datetime import datetime
from google import genai
from groq import Groq
from colorama import Fore, Back, Style, init

# Inicializar colorama
init(autoreset=True)

dotenv.load_dotenv()

# ======================
# GEMINI PRO
# ======================
def run_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "No se encontró GEMINI_API_KEY ni GOOGLE_API_KEY en el entorno/.env"
        )

    client = genai.Client(api_key=api_key)

    start_time = time.time()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    elapsed_time = time.time() - start_time

    usage_meta = response.usage_metadata if hasattr(response, "usage_metadata") else None
    
    # Calcular costo: $0.30/M tokens entrada, $2.50/M tokens salida
    tokens_input = getattr(usage_meta, "prompt_token_count", 0) if usage_meta else 0
    tokens_output = getattr(usage_meta, "candidates_token_count", 0) if usage_meta else 0
    cost = (tokens_input * 0.30 / 1_000_000) + (tokens_output * 2.50 / 1_000_000)
    
    output = {
        "model": "Gemini 2.5 Flash",
        "text": getattr(response, "text", str(response)),
        "tokens_input": tokens_input if tokens_input > 0 else None,
        "tokens_output": tokens_output if tokens_output > 0 else None,
        "tokens_total": getattr(usage_meta, "total_token_count", None) if usage_meta else None,
        "response_time_seconds": round(elapsed_time, 3),
        "cost_usd": round(cost, 6),
        "raw_response": response.model_dump() if hasattr(response, "model_dump") else str(response)
    }

    return output


# ======================
# GROQ (LLAMA 3)
# ======================
def run_groq(prompt):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    start_time = time.time()
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    elapsed_time = time.time() - start_time

    tokens_input = completion.usage.prompt_tokens
    tokens_output = completion.usage.completion_tokens
    cost = (tokens_input * 0.59 / 1_000_000) + (tokens_output * 0.79 / 1_000_000)

    output = {
        "model": "Llama 3.3 70B (Groq)",
        "text": completion.choices[0].message.content,
        "tokens_input": tokens_input,
        "tokens_output": tokens_output,
        "tokens_total": completion.usage.total_tokens,
        "response_time_seconds": round(elapsed_time, 3),
        "cost_usd": round(cost, 6),
        "raw_response": completion.model_dump()
    }

    return output


# ======================
# SELECTOR DE MODELO
# ======================
def run_model(model_name, prompt):
    if model_name == "gemini":
        return run_gemini(prompt)
    elif model_name == "groq":
        return run_groq(prompt)
    else:
        raise ValueError("Modelo no soportado")


# ======================
# MAIN
# ======================

if __name__ == "__main__":
    print()
    print(Fore.CYAN + Style.BRIGHT + "═" * 75)
    print(Fore.CYAN + Style.BRIGHT + "  COMPARADOR DE MODELOS DE IA".center(75))
    print(Fore.CYAN + Style.BRIGHT + "═" * 75)
    print()
    
    while True:
        prompt = input(Fore.YELLOW + "Ingresa tu prompt (o 'salir' para terminar): " + Style.RESET_ALL).strip()
        
        if prompt.lower() in ['salir', 'exit', 'quit', 'q']:
            print()
            print(Fore.CYAN + "👋 ¡Hasta pronto!")
            print()
            break
        
        if not prompt:
            print(Fore.RED + Style.BRIGHT + "\n[ERROR] El prompt no puede estar vacío\n")
            continue
        
        print()
        print(Fore.MAGENTA + "Procesando con ambos modelos...")
        print()
        
        try:
            results = {
                "timestamp": datetime.now().isoformat(),
                "prompt": prompt,
                "gemini": run_model("gemini", prompt),
                "groq": run_model("groq", prompt)
            }
            
            
            historial_file = "historial.json"
            historial = []
            
        
            if os.path.exists(historial_file):
                try:
                    with open(historial_file, 'r', encoding='utf-8') as f:
                        historial = json.load(f)
                except:
                    historial = []
            
            
            historial.append(results)
            
            
            with open(historial_file, 'w', encoding='utf-8') as f:
                json.dump(historial, indent=4, ensure_ascii=False, fp=f)
            
            print(Fore.GREEN + Style.BRIGHT + "─" * 75)
            print(Fore.GREEN + Style.BRIGHT + "  COMPARATIVA DE RESULTADOS".center(75))
            print(Fore.GREEN + Style.BRIGHT + "─" * 75)
            print()
            
            for model_key in ["gemini", "groq"]:
                data = results[model_key]
                
                print(Fore.WHITE + Back.BLUE + Style.BRIGHT + f" {data['model']} " + Style.RESET_ALL)
                print()
                
                print(Fore.CYAN + "  Tokens:")
                print(Fore.WHITE + f"    Entrada     : " + Fore.YELLOW + f"{data['tokens_input']:>10}")
                print(Fore.WHITE + f"    Salida      : " + Fore.YELLOW + f"{data['tokens_output']:>10}")
                print(Fore.WHITE + f"    Total       : " + Fore.GREEN + Style.BRIGHT + f"{data['tokens_total']:>10}")
                print()
                print(Fore.CYAN + "  Performance:")
                print(Fore.WHITE + f"    Tiempo      : " + Fore.YELLOW + f"{data['response_time_seconds']:>10}s")
                print(Fore.WHITE + f"    Costo       : " + Fore.GREEN + f"${data['cost_usd']:>10.6f}")
                print()
                print(Fore.CYAN + "  Respuesta:")
                
                text_lines = data['text'].split('\n')
                display_lines = min(5, len(text_lines))
                for line in text_lines[:display_lines]:
                    print(Fore.WHITE + f"    {line}")
                if len(text_lines) > display_lines:
                    print(Fore.WHITE + Style.DIM + f"    ... ({len(text_lines) - display_lines} líneas más)")
                print()
                print(Fore.WHITE + Style.DIM + "─" * 75)
                print()
            
            print(Fore.CYAN + Style.BRIGHT + "═" * 75)
            print(Fore.GREEN + f"Resultados guardados en historial.json (Total: {len(historial)} consultas)")
            print(Fore.CYAN + Style.BRIGHT + "═" * 75)
            print()
            
        except KeyboardInterrupt:
            print()
            print(Fore.CYAN + "\n👋 ¡Hasta pronto!")
            print()
            break
        except Exception as e:
            print()
            print(Fore.RED + Style.BRIGHT + f"[ERROR] {str(e)}")
            print()
            continue
