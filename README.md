# Microservicio: Factorial (un solo archivo)

Este repositorio contiene un microservicio minimalista escrito en Python (Flask) que expone un endpoint HTTP para calcular el factorial de un número recibido por la URL.

## Contenido

- `app.py` - Microservicio (un solo archivo). Endpoint: `GET /factorial/<n>`
- `requirements.txt` - Dependencias mínimas (solo Flask)


## API

GET /factorial/<n>
- Parámetros: `n` (entero en la URL)
- Respuesta JSON 200:
  - `numero`: entero recibido
  - `factorial`: factorial de `n` como cadena
  - `paridad`: "par" o "impar" según corresponda al factorial
- Errores:
  - 400 si `n` es negativo o inválido
  - 500 en errores internos

Ejemplo de respuesta para `/factorial/5`:

```json
{ "numero": 5, "factorial": "120", "paridad": "par" }
```

## Contrato (mini)
- Entrada: entero n >= 0 por la ruta
- Salida: JSON con número, factorial, paridad
- Error mode: respuestas HTTP con JSON (`error` campo)

## Casos borde
- n negativo -> 400
- n muy grande -> el factorial crece rápido; la implementación usa enteros grandes, pero tenga cuidado con tiempos y uso de memoria.
- No numérico -> ruta con `<int:n>` no matchea; puede retornar 404 por Flask; para producción agregar validación adicional.

## Cómo ejecutar (local) - mínimas dependencias

1. Crear entorno virtual e instalar dependencias:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Ejecutar el servicio:

```powershell
python app.py
```

3. Probar:

```powershell
Invoke-RestMethod -Uri http://localhost:5000/factorial/5
```

## Contenido

- `app.py` - Microservicio (un solo archivo). Endpoint: `GET /factorial/<n>`
- `create_word.py` - Script para generar un archivo Word (`REPORTE.docx`) que contiene el enlace al repositorio de GitHub.
- `requirements.txt` - Dependencias.

## Diseño: cómo cambiaría si hay que comunicarse con un servicio de historial (análisis)
Si además debe notificar a otro servicio que persiste un historial en una DB externa.

1) Comunicación sincrónica HTTP directa
- Flujo: microservicio calcula -> realiza POST al servicio de historial con payload {numero, factorial, paridad, timestamp}

2) Comunicación asíncrona mediante mensajería (recomendada para escalabilidad)
- Flujo: microservicio publica un evento `calculo_factorial` a una cola/broker (RabbitMQ, Kafka). Servicio de historial consume y persiste en la DB..

probablemente elegiriamos la segunda pues se asemeja más al uso de un servicio y disminuye el acoplamiento