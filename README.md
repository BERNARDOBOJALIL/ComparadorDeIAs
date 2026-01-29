# Comparador de Modelos de IA

Herramienta de línea de comandos para comparar respuestas, rendimiento y costos entre diferentes modelos de lenguaje (LLM). Actualmente soporta **Gemini 2.5 Flash** y **Llama 3.3 70B** (via Groq).

## 📋 Características

- ✅ Comparación lado a lado de respuestas de múltiples modelos
- ✅ Métricas detalladas de uso de tokens (entrada, salida y total)
- ✅ Cálculo preciso de costos en USD
- ✅ Medición de tiempos de respuesta
- ✅ Interfaz de terminal colorida y profesional
- ✅ Exportación automática de resultados a JSON

## 🤖 Modelos Soportados

### Gemini 2.5 Flash (Google)
- **Modelo**: `gemini-2.5-flash`
- **Precio entrada**: $0.30 / millón de tokens
- **Precio salida**: $2.50 / millón de tokens
- **API**: Google Gemini API

### Llama 3.3 70B Versatile (Groq)
- **Modelo**: `llama-3.3-70b-versatile`
- **Precio entrada**: $0.59 / millón de tokens
- **Precio salida**: $0.79 / millón de tokens
- **API**: Groq Cloud

## 📦 Requisitos

- Python 3.12+
- API Key de Google Gemini
- API Key de Groq

### Dependencias principales

```
google-genai        (Cliente oficial de Google Gemini)
groq                (Cliente oficial de Groq)
colorama==0.4.6     (Colores en terminal)
python-dotenv==1.2.1 (Gestión de variables de entorno)
```

Ver `requirements.txt` para la lista completa de dependencias.

## 🚀 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd Topicos
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar variables de entorno**
   
   Crear un archivo `.env` en la raíz del proyecto con tus API keys:
   ```env
   GEMINI_API_KEY=tu_api_key_de_gemini
   GROQ_API_KEY=tu_api_key_de_groq
   ```
   
   También puedes usar `GOOGLE_API_KEY` en lugar de `GEMINI_API_KEY`.

## 💻 Uso

Ejecutar el comparador:

```bash
python ask.py
```

El programa te pedirá que ingreses un prompt. Ejemplo:

```
══════════════════════════════════════════════════════════════════════════════
                        COMPARADOR DE MODELOS DE IA                          
══════════════════════════════════════════════════════════════════════════════

Ingresa tu prompt: Explica qué es el machine learning

Procesando con ambos modelos...
```

## 📊 Salida

El programa mostrará una comparativa visual en la terminal con:

- **Nombre del modelo**
- **Tokens de entrada**: Cantidad de tokens en el prompt
- **Tokens de salida**: Cantidad de tokens generados
- **Tokens totales**: Suma de entrada + salida
- **Tiempo de respuesta**: En segundos
- **Costo**: Calculado en USD según las tarifas actuales
- **Respuesta**: Primeras 5 líneas de la respuesta generada

### Ejemplo de salida:

```
───────────────────────────────────────────────────────────────────────────
                        COMPARATIVA DE RESULTADOS
───────────────────────────────────────────────────────────────────────────

 Gemini 2.5 Flash 

  Tokens:
    Entrada     :         15
    Salida      :        120
    Total       :        135

  Performance:
    Tiempo      :     2.350s
    Costo       : $0.000305

  Respuesta:
    El machine learning es una rama de la inteligencia artificial...
```

### Archivo JSON

Los resultados completos se guardan automáticamente en un archivo JSON con el formato:

```
comparacion_YYYYMMDD_HHMMSS.json
```

Contenido del JSON:
```json
{
    "timestamp": "2026-01-28T22:30:45.123456",
    "prompt": "Tu prompt aquí",
    "gemini": {
        "model": "Gemini 2.5 Flash",
        "text": "Respuesta completa...",
        "tokens_input": 15,
        "tokens_output": 120,
        "tokens_total": 135,
        "response_time_seconds": 2.35,
        "cost_usd": 0.000305,
        "raw_response": {...}
    },
    "groq": {
        "model": "Llama 3.3 70B (Groq)",
        "text": "Respuesta completa...",
        "tokens_input": 12,
        "tokens_output": 95,
        "tokens_total": 107,
        "response_time_seconds": 1.87,
        "cost_usd": 0.000082,
        "raw_response": {...}
    }
}
```

## 🔧 Estructura del Proyecto

```
Topicos/
│
├── ask.py              # Script principal
├── requirements.txt    # Dependencias de Python
├── .env               # Variables de entorno (no incluido en git)
├── .gitignore         # Archivos ignorados por git
├── README.md          # Este archivo
└── comparacion_*.json # Archivos de salida generados
```

## 💰 Cálculo de Costos

Los costos se calculan usando las tarifas oficiales de cada proveedor:

**Fórmula**:
```
Costo Total = (tokens_entrada × precio_entrada_por_millón / 1,000,000) + 
              (tokens_salida × precio_salida_por_millón / 1,000,000)
```

## 📝 Notas

- Los precios son válidos a la fecha de enero 2026 y pueden cambiar
- Se requiere conectividad a internet para usar las APIs
- Respeta los límites de cuota de cada proveedor (rate limits)
- El tier gratuito de Gemini tiene límites diarios y por minuto
- Groq generalmente tiene límites más generosos en el tier gratuito

## 🔐 Seguridad

- **NUNCA** subas tu archivo `.env` a repositorios públicos
- Mantén tus API keys privadas
- Usa variables de entorno o archivos `.env` para las credenciales
- Revisa periódicamente tu uso y costos en los paneles de cada proveedor

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📞 Soporte

Para obtener tus API keys:
- **Gemini**: https://ai.google.dev/
- **Groq**: https://console.groq.com/

Para reportar problemas o sugerencias, abre un issue en el repositorio.
