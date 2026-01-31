import json
import matplotlib.pyplot as plt
from datetime import datetime
from colorama import Fore, Back, Style, init
import mplcursors
import os

init(autoreset=True)

def cargar_historial():
    """Carga el historial de comparaciones"""
    if not os.path.exists("historial.json"):
        print(Fore.RED + "No se encontró historial.json")
        print("Ejecuta ask.py primero para generar datos.")
        return None
    
    with open("historial.json", 'r', encoding='utf-8') as f:
        return json.load(f)


def generar_graficas():
    """Genera gráficas comparativas de los modelos"""
    historial = cargar_historial()
    
    if not historial or len(historial) == 0:
        print(Fore.RED + "No hay datos suficientes para graficar")
        return
    
    print()
    print(Fore.CYAN + Style.BRIGHT + "═" * 75)
    print(Fore.CYAN + Style.BRIGHT + f"  GENERANDO GRÁFICAS ({len(historial)} consultas)".center(75))
    print(Fore.CYAN + Style.BRIGHT + "═" * 75)
    print()
    
    # Extraer datos para gráficas
    indices = list(range(1, len(historial) + 1))
    prompts = [h['prompt'][:50] + '...' if len(h['prompt']) > 50 else h['prompt'] for h in historial]
    
    # Datos Gemini
    gemini_tokens_total = [h['gemini']['tokens_total'] for h in historial]
    gemini_tokens_input = [h['gemini']['tokens_input'] for h in historial]
    gemini_tokens_output = [h['gemini']['tokens_output'] for h in historial]
    gemini_tiempo = [h['gemini']['response_time_seconds'] for h in historial]
    gemini_costo = [h['gemini']['cost_usd'] for h in historial]
    
    # Datos Groq
    groq_tokens_total = [h['groq']['tokens_total'] for h in historial]
    groq_tokens_input = [h['groq']['tokens_input'] for h in historial]
    groq_tokens_output = [h['groq']['tokens_output'] for h in historial]
    groq_tiempo = [h['groq']['response_time_seconds'] for h in historial]
    groq_costo = [h['groq']['cost_usd'] for h in historial]
    
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Comparativa  Cool', fontsize=16, fontweight='bold')
    fig.patch.set_facecolor('#F5F5F5')
    
    color_gemini = '#6366F1'  
    color_groq = '#10B981'    
    
    # 1. Tokens Totales
    ax1 = axes[0, 0]
    ax1.set_facecolor('#FAFAFA')
    ax1.plot(indices, gemini_tokens_total, label='Gemini 2.5 Flash', 
             color=color_gemini, linewidth=2.5, alpha=0.8)
    ax1.plot(indices, groq_tokens_total, label='Llama 3.3 70B', 
             color=color_groq, linewidth=2.5, alpha=0.8)
    sc1_gemini = ax1.scatter(indices, gemini_tokens_total, color=color_gemini, s=80, zorder=5, edgecolors='white', linewidth=1.5)
    sc1_groq = ax1.scatter(indices, groq_tokens_total, color=color_groq, s=80, marker='s', zorder=5, edgecolors='white', linewidth=1.5)
    ax1.set_xlabel('Número de Consulta', fontweight='bold')
    ax1.set_ylabel('Tokens Totales', fontweight='bold')
    ax1.set_title('Tokens Totales por Consulta', fontsize=12, fontweight='bold', pad=10)
    ax1.legend(framealpha=0.9)
    ax1.grid(True, alpha=0.2, linestyle='--')
    
    # 2. Tokens de Entrada
    ax2 = axes[0, 1]
    ax2.set_facecolor('#FAFAFA')
    ax2.plot(indices, gemini_tokens_input, label='Gemini 2.5 Flash', 
             color=color_gemini, linewidth=2.5, alpha=0.8)
    ax2.plot(indices, groq_tokens_input, label='Llama 3.3 70B', 
             color=color_groq, linewidth=2.5, alpha=0.8)
    sc2_gemini = ax2.scatter(indices, gemini_tokens_input, color=color_gemini, s=80, zorder=5, edgecolors='white', linewidth=1.5)
    sc2_groq = ax2.scatter(indices, groq_tokens_input, color=color_groq, s=80, marker='s', zorder=5, edgecolors='white', linewidth=1.5)
    ax2.set_xlabel('Número de Consulta', fontweight='bold')
    ax2.set_ylabel('Tokens de Entrada', fontweight='bold')
    ax2.set_title('Tokens de Entrada por Consulta', fontsize=12, fontweight='bold', pad=10)
    ax2.legend(framealpha=0.9)
    ax2.grid(True, alpha=0.2, linestyle='--')
    
    # 3. Tokens de Salida
    ax3 = axes[0, 2]
    ax3.set_facecolor('#FAFAFA')
    ax3.plot(indices, gemini_tokens_output, label='Gemini 2.5 Flash', 
             color=color_gemini, linewidth=2.5, alpha=0.8)
    ax3.plot(indices, groq_tokens_output, label='Llama 3.3 70B', 
             color=color_groq, linewidth=2.5, alpha=0.8)
    sc3_gemini = ax3.scatter(indices, gemini_tokens_output, color=color_gemini, s=80, zorder=5, edgecolors='white', linewidth=1.5)
    sc3_groq = ax3.scatter(indices, groq_tokens_output, color=color_groq, s=80, marker='s', zorder=5, edgecolors='white', linewidth=1.5)
    ax3.set_xlabel('Número de Consulta', fontweight='bold')
    ax3.set_ylabel('Tokens de Salida', fontweight='bold')
    ax3.set_title('Tokens de Salida por Consulta', fontsize=12, fontweight='bold', pad=10)
    ax3.legend(framealpha=0.9)
    ax3.grid(True, alpha=0.2, linestyle='--')
    
    # 4. Tiempo de Respuesta
    ax4 = axes[1, 0]
    ax4.set_facecolor('#FAFAFA')
    ax4.plot(indices, gemini_tiempo, label='Gemini 2.5 Flash', 
             color=color_gemini, linewidth=2.5, alpha=0.8)
    ax4.plot(indices, groq_tiempo, label='Llama 3.3 70B', 
             color=color_groq, linewidth=2.5, alpha=0.8)
    sc4_gemini = ax4.scatter(indices, gemini_tiempo, color=color_gemini, s=80, zorder=5, edgecolors='white', linewidth=1.5)
    sc4_groq = ax4.scatter(indices, groq_tiempo, color=color_groq, s=80, marker='s', zorder=5, edgecolors='white', linewidth=1.5)
    ax4.set_xlabel('Número de Consulta', fontweight='bold')
    ax4.set_ylabel('Tiempo (segundos)', fontweight='bold')
    ax4.set_title('Tiempo de Respuesta por Consulta', fontsize=12, fontweight='bold', pad=10)
    ax4.legend(framealpha=0.9)
    ax4.grid(True, alpha=0.2, linestyle='--')
    
    # 5. Costo por Consulta
    ax5 = axes[1, 1]
    ax5.set_facecolor('#FAFAFA')
    ax5.plot(indices, gemini_costo, label='Gemini 2.5 Flash', 
             color=color_gemini, linewidth=2.5, alpha=0.8)
    ax5.plot(indices, groq_costo, label='Llama 3.3 70B', 
             color=color_groq, linewidth=2.5, alpha=0.8)
    sc5_gemini = ax5.scatter(indices, gemini_costo, color=color_gemini, s=80, zorder=5, edgecolors='white', linewidth=1.5)
    sc5_groq = ax5.scatter(indices, groq_costo, color=color_groq, s=80, marker='s', zorder=5, edgecolors='white', linewidth=1.5)
    ax5.set_xlabel('Número de Consulta', fontweight='bold')
    ax5.set_ylabel('Costo (USD)', fontweight='bold')
    ax5.set_title('Costo por Consulta', fontsize=12, fontweight='bold', pad=10)
    ax5.legend(framealpha=0.9)
    ax5.grid(True, alpha=0.2, linestyle='--')
    ax5.ticklabel_format(style='plain', axis='y')
    
    # 6. Costo Acumulado
    ax6 = axes[1, 2]
    ax6.set_facecolor('#FAFAFA')
    gemini_costo_acum = [sum(gemini_costo[:i+1]) for i in range(len(gemini_costo))]
    groq_costo_acum = [sum(groq_costo[:i+1]) for i in range(len(groq_costo))]
    ax6.plot(indices, gemini_costo_acum, label='Gemini 2.5 Flash', 
             color=color_gemini, linewidth=2.5, alpha=0.8)
    ax6.plot(indices, groq_costo_acum, label='Llama 3.3 70B', 
             color=color_groq, linewidth=2.5, alpha=0.8)
    sc6_gemini = ax6.scatter(indices, gemini_costo_acum, color=color_gemini, s=80, zorder=5, edgecolors='white', linewidth=1.5)
    sc6_groq = ax6.scatter(indices, groq_costo_acum, color=color_groq, s=80, marker='s', zorder=5, edgecolors='white', linewidth=1.5)
    ax6.set_xlabel('Número de Consulta', fontweight='bold')
    ax6.set_ylabel('Costo Acumulado (USD)', fontweight='bold')
    ax6.set_title('Costo Acumulado', fontsize=12, fontweight='bold', pad=10)
    ax6.legend(framealpha=0.9)
    ax6.grid(True, alpha=0.2, linestyle='--')
    ax6.ticklabel_format(style='plain', axis='y')
    
    # Tooltips asquerosos
    all_scatters = [
        sc1_gemini, sc1_groq, sc2_gemini, sc2_groq,
        sc3_gemini, sc3_groq, sc4_gemini, sc4_groq,
        sc5_gemini, sc5_groq, sc6_gemini, sc6_groq
    ]
    
    scatter_data = {
        sc1_gemini: ('Gemini', gemini_tokens_total, 'tokens totales'),
        sc1_groq: ('Groq', groq_tokens_total, 'tokens totales'),
        sc2_gemini: ('Gemini', gemini_tokens_input, 'tokens entrada'),
        sc2_groq: ('Groq', groq_tokens_input, 'tokens entrada'),
        sc3_gemini: ('Gemini', gemini_tokens_output, 'tokens salida'),
        sc3_groq: ('Groq', groq_tokens_output, 'tokens salida'),
        sc4_gemini: ('Gemini', gemini_tiempo, 'seg'),
        sc4_groq: ('Groq', groq_tiempo, 'seg'),
        sc5_gemini: ('Gemini', gemini_costo, 'USD'),
        sc5_groq: ('Groq', groq_costo, 'USD'),
        sc6_gemini: ('Gemini', [sum(gemini_costo[:i+1]) for i in range(len(gemini_costo))], 'USD acum.'),
        sc6_groq: ('Groq', [sum(groq_costo[:i+1]) for i in range(len(groq_costo))], 'USD acum.'),
    }
    
    for scatter in all_scatters:
        cursor = mplcursors.cursor(scatter, hover=2)
        
        @cursor.connect("add")
        def on_add(sel):
            idx = int(sel.target[0]) - 1
            model, values, unit = scatter_data[sel.artist]
            value = values[idx]
            
            if 'USD' in unit:
                value_str = f"${value:.6f}"
            elif 'seg' in unit:
                value_str = f"{value:.3f}s"
            else:
                value_str = f"{value}"
            
            text = f"{model} - Consulta #{idx + 1}\n"
            text += f"{prompts[idx]}\n"
            text += f"Valor: {value_str}"
            
            sel.annotation.set_text(text)
            sel.annotation.get_bbox_patch().set(
                boxstyle='round,pad=0.5',
                facecolor='white',
                edgecolor='gray',
                alpha=0.95
            )
    
    plt.tight_layout()
    
    # Mostrar gráfica
    print(Fore.YELLOW + "Mostrando gráficas...")
    plt.show()
    
    print()
    print(Fore.CYAN + Style.BRIGHT + "═" * 75)
    print(Fore.CYAN + Style.BRIGHT + "  A ver si jala".center(75))
    print(Fore.CYAN + Style.BRIGHT + "═" * 75)
    print()
    
    print(Fore.WHITE + Back.BLUE + Style.BRIGHT + " Gemini 2.5 Flash " + Style.RESET_ALL)
    print(Fore.CYAN + f"  Promedio tokens totales: " + Fore.YELLOW + f"{sum(gemini_tokens_total)/len(gemini_tokens_total):.1f}")
    print(Fore.CYAN + f"  Promedio tiempo:         " + Fore.YELLOW + f"{sum(gemini_tiempo)/len(gemini_tiempo):.3f}s")
    print(Fore.CYAN + f"  Costo total:             " + Fore.GREEN + f"${sum(gemini_costo):.6f}")
    print(Fore.CYAN + f"  Costo promedio:          " + Fore.GREEN + f"${sum(gemini_costo)/len(gemini_costo):.6f}")
    print()
    
    print(Fore.WHITE + Back.BLUE + Style.BRIGHT + " Llama 3.3 70B (Groq) " + Style.RESET_ALL)
    print(Fore.CYAN + f"  Promedio tokens totales: " + Fore.YELLOW + f"{sum(groq_tokens_total)/len(groq_tokens_total):.1f}")
    print(Fore.CYAN + f"  Promedio tiempo:         " + Fore.YELLOW + f"{sum(groq_tiempo)/len(groq_tiempo):.3f}s")
    print(Fore.CYAN + f"  Costo total:             " + Fore.GREEN + f"${sum(groq_costo):.6f}")
    print(Fore.CYAN + f"  Costo promedio:          " + Fore.GREEN + f"${sum(groq_costo)/len(groq_costo):.6f}")
    print()
    
    print(Fore.CYAN + Style.BRIGHT + "═" * 75)
    print()


if __name__ == "__main__":
    generar_graficas()
