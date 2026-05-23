# Manual de instalación y uso — Windows

**proyecto_turboreactor** · Calculadora de propiedades termodinámicas para toberas de turbofán

---

## Índice

1. [Requisitos previos](#1-requisitos-previos)
2. [Instalar Python](#2-instalar-python)
3. [Instalar Git](#3-instalar-git)
4. [Instalar Visual Studio Code](#4-instalar-visual-studio-code)
5. [Clonar el repositorio](#5-clonar-el-repositorio)
6. [Abrir la carpeta en VS Code](#6-abrir-la-carpeta-en-vs-code)
7. [Crear el entorno virtual](#7-crear-el-entorno-virtual)
8. [Activar el entorno virtual en PowerShell](#8-activar-el-entorno-virtual-en-powershell)
9. [Instalar dependencias](#9-instalar-dependencias)
10. [Ejecutar la aplicación Streamlit](#10-ejecutar-la-aplicación-streamlit)
11. [Abrir la app en el navegador](#11-abrir-la-app-en-el-navegador)
12. [Correr las pruebas con pytest](#12-correr-las-pruebas-con-pytest)
13. [Exportar resultados en CSV](#13-exportar-resultados-en-csv)
14. [Variables visualizadas](#14-variables-visualizadas)
15. [Interpretación de gráficas](#15-interpretación-de-gráficas)
16. [Actualizar el proyecto con git pull](#16-actualizar-el-proyecto-con-git-pull)
17. [Problemas comunes y solución](#17-problemas-comunes-y-solución)

---

## 1. Requisitos previos

Antes de comenzar, verifica que tu equipo cumple con lo siguiente:

| Requisito | Versión mínima | Notas |
| --------- | -------------- | ----- |
| Windows | 10 (64-bit) | Windows 11 también compatible |
| Python | 3.10 | Se instala en el paso 2 |
| Git | 2.40 | Se instala en el paso 3 |
| VS Code | 1.85 | Opcional pero recomendado |
| RAM | 4 GB | 8 GB recomendado para datasets grandes |
| Espacio en disco | 1 GB libres | Para Python, dependencias y datos |

No se requiere conexión a internet durante el uso de la app, solo para la instalación inicial.

---

## 2. Instalar Python

### Descargar

1. Abre el navegador y ve a <https://www.python.org/downloads/windows/>
2. Haz clic en el botón **Download Python 3.x.x** (la versión más reciente de la rama 3.x).
3. Descarga el instalador **Windows installer (64-bit)**.

### Instalar

1. Ejecuta el archivo `.exe` descargado.
2. **Importante:** en la primera pantalla del instalador, marca la casilla
   **"Add Python 3.x to PATH"** antes de continuar.
3. Haz clic en **Install Now**.
4. Espera a que termine y haz clic en **Close**.

### Verificar la instalación

Abre PowerShell (`Win + X` → **Terminal** o **Windows PowerShell**) y ejecuta:

```powershell
python --version
```

Deberías ver algo como:

```
Python 3.12.3
```

Si el comando no se reconoce, cierra y vuelve a abrir PowerShell para que tome el PATH actualizado.

---

## 3. Instalar Git

### Descargar

1. Ve a <https://git-scm.com/download/win>
2. La descarga del instalador de 64-bit comenzará automáticamente.

### Instalar

1. Ejecuta el instalador `.exe`.
2. Acepta las opciones por defecto en cada pantalla.
3. En la pantalla **"Choosing the default editor used by Git"**, puedes seleccionar
   **Visual Studio Code** si ya lo tienes instalado, o dejar **Vim** (valor por defecto).
4. En **"Adjusting your PATH environment"**, deja seleccionada la opción
   **"Git from the command line and also from 3rd-party software"**.
5. Continúa con los valores por defecto y haz clic en **Install**.

### Verificar la instalación

```powershell
git --version
```

Resultado esperado:

```
git version 2.45.1.windows.1
```

---

## 4. Instalar Visual Studio Code

VS Code es el editor recomendado. Si prefieres otro editor, puedes omitir este paso.

### Descargar e instalar

1. Ve a <https://code.visualstudio.com/>
2. Haz clic en **Download for Windows**.
3. Ejecuta el instalador y acepta las opciones por defecto.
4. **Recomendado:** en la pantalla de tareas adicionales, marca:
   - **"Add 'Open with Code' action to Windows Explorer file context menu"**
   - **"Add 'Open with Code' action to Windows Explorer directory context menu"**
   - **"Register Code as an editor for supported file types"**

### Extensiones recomendadas

Una vez instalado VS Code, abre el panel de extensiones (`Ctrl + Shift + X`) e instala:

- **Python** (Microsoft) — soporte completo para Python
- **Pylance** (Microsoft) — autocompletado e inferencia de tipos
- **GitLens** — visualización avanzada del historial de Git

---

## 5. Clonar el repositorio

Elige una carpeta donde quieras guardar el proyecto. Por ejemplo, `C:\Proyectos`.

### Desde PowerShell

```powershell
# Crear la carpeta si no existe
New-Item -ItemType Directory -Path "C:\Proyectos" -Force

# Moverse a esa carpeta
cd C:\Proyectos

# Clonar el repositorio
git clone <url-del-repositorio>

# Entrar a la carpeta del proyecto
cd proyecto_turboreactor
```

Reemplaza `<url-del-repositorio>` con la URL real del repositorio (por ejemplo,
`https://github.com/usuario/proyecto_turboreactor.git`).

### Verificar que la descarga fue exitosa

```powershell
dir
```

Deberías ver archivos como `app.py`, `requirements.txt`, `README.md`, y las
carpetas `src/` y `tests/`.

---

## 6. Abrir la carpeta en VS Code

### Opción A — desde PowerShell

Con la terminal ya ubicada dentro de `proyecto_turboreactor`:

```powershell
code .
```

### Opción B — desde VS Code

1. Abre VS Code.
2. Menú **File** → **Open Folder…**
3. Navega a `C:\Proyectos\proyecto_turboreactor` y haz clic en **Seleccionar carpeta**.

VS Code detectará automáticamente que es un proyecto Python y puede sugerirte
instalar la extensión Python si aún no la tienes.

---

## 7. Crear el entorno virtual

Un entorno virtual aísla las dependencias del proyecto del resto del sistema,
evitando conflictos de versiones.

Desde PowerShell, **dentro de la carpeta del proyecto**:

```powershell
python -m venv .venv
```

Esto crea una carpeta oculta `.venv` dentro del proyecto con una instalación
privada de Python.

### Verificar que se creó correctamente

```powershell
dir .venv
```

Deberías ver subcarpetas como `Scripts`, `Lib` e `Include`.

---

## 8. Activar el entorno virtual en PowerShell

### Primer uso: habilitar la ejecución de scripts

Windows bloquea la ejecución de scripts por defecto. Ejecuta esto **una sola vez**
con PowerShell como administrador:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Escribe `S` (Sí) cuando se solicite confirmación.

> Si no tienes permisos de administrador, usa en su lugar:
>
> ```powershell
> Set-ExecutionPolicy -Scope Process Bypass
> ```
>
> Este ajuste solo aplica a la sesión actual de PowerShell.

### Activar el entorno

```powershell
.venv\Scripts\Activate.ps1
```

Sabrás que el entorno está activo porque el prompt cambiará y mostrará el prefijo
`(.venv)` al inicio:

```
(.venv) PS C:\Proyectos\proyecto_turboreactor>
```

> **Nota:** debes activar el entorno virtual **cada vez** que abras una nueva
> terminal antes de trabajar con el proyecto.

### Desactivar el entorno cuando termines

```powershell
deactivate
```

---

## 9. Instalar dependencias

Con el entorno virtual activo, instala todas las bibliotecas necesarias:

```powershell
pip install -r requirements.txt
```

Verás la descarga e instalación de los paquetes. El proceso puede tardar
entre 1 y 3 minutos según la velocidad de tu conexión.

### Verificar la instalación

```powershell
pip list
```

Deberías ver entre los paquetes: `streamlit`, `numpy`, `pandas`, `plotly`,
`matplotlib` y `pytest`.

---

## 10. Ejecutar la aplicación Streamlit

Con el entorno virtual activo y dentro de la carpeta del proyecto:

```powershell
streamlit run app.py
```

Verás en la terminal una salida similar a:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

La app se abrirá automáticamente en tu navegador por defecto.
Si no se abre sola, consulta el paso siguiente.

Para **detener** la aplicación, presiona `Ctrl + C` en la terminal.

---

## 11. Abrir la app en el navegador

Si el navegador no se abrió automáticamente:

1. Abre cualquier navegador (Chrome, Edge, Firefox).
2. Escribe en la barra de dirección:

```
http://localhost:8501
```

3. Presiona `Enter`.

### Uso básico de la interfaz

Una vez en el navegador:

1. En el **panel lateral izquierdo**, configura los parámetros de cálculo:
   - Presión total de entrada P₀ [kPa]
   - Presión estática de salida [kPa]
   - Temperatura total T₀ [K]
   - Gasto másico ṁ [kg/s]
   - Razón de calores específicos γ
   - Constante del gas R [J/(kg·K)]
   - Número de puntos de discretización

2. Haz clic en el botón **Calcular**.

3. Revisa las métricas superiores: Mach máximo, velocidad máxima, densidad
   inicial, área final y radio equivalente final.

4. Explora las gráficas interactivas de los perfiles termodinámicos y la
   comparación normalizada de tendencias.

---

## 12. Correr las pruebas con pytest

Las pruebas unitarias verifican que todas las funciones de cálculo producen
resultados correctos.

Con el entorno virtual activo:

```powershell
# Ejecutar todas las pruebas
pytest tests/

# Ejecutar con detalle (nombre de cada prueba)
pytest tests/ -v

# Ejecutar solo las pruebas de una función específica
pytest tests/ -k "density"
pytest tests/ -k "mach"
pytest tests/ -k "pressure_ratio"
pytest tests/ -k "results_table"
```

### Resultado esperado

```
========================= test session starts ==========================
platform win32 -- Python 3.12.3, pytest-8.x.x
collected XX items

tests/test_calculations.py ................................  [100%]

========================== XX passed in X.XXs ==========================
```

Si alguna prueba falla, pytest mostrará el nombre de la prueba, el valor
esperado y el valor obtenido para facilitar el diagnóstico.

---

## 13. Exportar resultados en CSV

1. Ejecuta la app y presiona **Calcular** con los parámetros deseados.
2. Desplázate hacia abajo hasta el botón **Descargar CSV completo**.
3. Haz clic en el botón.
4. El archivo `turbofan_nozzle_results.csv` se guardará en la carpeta
   de descargas de tu navegador (por defecto `C:\Users\<tu_usuario>\Downloads`).

### Columnas del archivo exportado

| Columna | Descripción | Unidad |
| ------- | ----------- | ------ |
| `pressure_kpa` | Presión estática local P | kPa |
| `static_temperature_k` | Temperatura estática local T | K |
| `speed_of_sound_m_s` | Velocidad del sonido local a | m/s |
| `velocity_m_s` | Velocidad del flujo V | m/s |
| `mach_number` | Número de Mach local M | — |
| `density_kg_m3` | Densidad del gas ρ | kg/m³ |
| `flow_area_m2` | Área transversal de flujo A | m² |
| `radius_m` | Radio equivalente de sección circular R | m |

> La primera fila tiene `flow_area_m2 = NaN` y `radius_m = NaN` porque en
> P = P₀ el fluido está en reposo (M = 0, V = 0) y el área es físicamente
> indefinida. Estas filas deben omitirse al analizar la geometría.

### Abrir el CSV en Excel

1. Abre Excel.
2. **Datos** → **Obtener datos** → **Desde archivo** → **Desde texto o CSV**.
3. Selecciona el archivo descargado.
4. Verifica que el delimitador sea **coma** y haz clic en **Cargar**.

---

## 14. Variables visualizadas

> **Nota:** Las variables se calculan mediante relaciones isentrópicas
> simplificadas para flujo compresible. Los resultados representan el límite
> teórico de un gas caloricamente perfecto sin pérdidas.

La aplicación calcula y grafica las siguientes variables en cada punto del
rango de presiones especificado:

| Variable | Símbolo | Descripción | Unidad |
| -------- | ------- | ----------- | ------ |
| Presión estática | P | Presión termodinámica local del gas. Es el eje x de todas las gráficas de perfil; disminuye conforme el gas se expande hacia la salida. | kPa |
| Número de Mach | M | Relación entre la velocidad del flujo y la velocidad local del sonido. Cuantifica el régimen de compresibilidad: subsónico (M < 1) o supersónico (M > 1). | — |
| Velocidad | V | Velocidad axial del flujo obtenida de la caída de entalpía entre el estado total y el estático. Aumenta al disminuir la presión. | m/s |
| Densidad | ρ | Masa por unidad de volumen del gas, calculada mediante la ley del gas ideal. Disminuye al expandirse el gas. | kg/m³ |
| Área de flujo | A | Sección transversal necesaria para que el gasto másico especificado sea consistente con la ecuación de continuidad `A = ṁ / (ρ V)`. | m² |
| Radio equivalente | R | Radio de una sección circular de área igual al área de flujo calculada. **El radio equivalente se calcula suponiendo una sección transversal circular:** `R = √(A / π)`. | m |

### Nota sobre el punto inicial

En la primera fila (P = P₀) el fluido está en reposo: M = 0 y V = 0.
En ese punto el área de flujo y el radio equivalente son físicamente
indefinidos y aparecen como `NaN` tanto en la tabla como en las gráficas.

---

## 15. Interpretación de gráficas

La aplicación genera dos tipos de visualizaciones: gráficas individuales de
perfil y una gráfica comparativa normalizada.

### Gráficas de perfil individual

Cada gráfica muestra cómo evoluciona una variable termodinámica en función
de la presión estática local. El eje x siempre es la presión [kPa],
que decrece de izquierda a derecha conforme el gas se expande.

| Gráfica | Qué representa |
| ------- | -------------- |
| **Presión vs Velocidad** | La velocidad aumenta al caer la presión: la entalpía de remanso se convierte en energía cinética. |
| **Presión vs Número de Mach** | El Mach crece monótonamente; cruza M = 1 si la tobera está ahogada. |
| **Presión vs Temperatura estática** | La temperatura cae junto con la presión por la expansión isentrópica. |
| **Presión vs Densidad** | La densidad decrece siguiendo la ley del gas ideal a temperatura decreciente. |
| **Presión vs Área de flujo** | El área puede disminuir (tobera convergente subsónica) o aumentar (divergente supersónica) según el régimen. |
| **Radio equivalente vs presión** | Evolución del radio de la sección circular equivalente. Sigue la misma tendencia que el área porque `R = √(A / π)`: al aumentar A, R aumenta proporcionalmente. |

### Por qué el radio sigue una tendencia similar al área

El radio equivalente es una transformación monotóna del área:

```math
R = √(A / π)
```

Dado que la raíz cuadrada es una función estrictamente creciente, R crece
siempre que A crece y decrece siempre que A decrece. La forma de la curva
es la misma; solo cambia la escala del eje y (de m² a m). Esto permite al
ingeniero leer directamente el diámetro requerido en cada sección sin
necesidad de calcular manualmente la raíz.

### Gráfica de comparación normalizada de tendencias

Esta gráfica superpone todas las variables en un único eje aplicando
normalización **min-max** a cada columna:

```math
valor_norm = (valor − mín) / (máx − mín)
```

El resultado de cada variable queda en el rango [0, 1], lo que permite
comparar tendencias y correlaciones independientemente de las unidades
originales (kPa, K, m/s, kg/m³, m², m).

**Cuándo es útil:**

- Identificar qué variables crecen o decrecen juntas al expandirse el gas.
- Detectar anomalías en el perfil (por ejemplo, un área que no decrece
  cuando se esperaría que lo hiciera).
- Comparar visualmente la pendiente de cada propiedad a lo largo del rango
  de presiones sin que las diferencias de escala distorsionen la lectura.

> La gráfica normalizada **no** conserva las unidades originales ni permite
> leer valores absolutos. Úsala solo para análisis de tendencias; para
> valores numéricos, consulta la tabla de resultados o el CSV exportado.

---

## 16. Actualizar el proyecto con git pull

Cuando el repositorio tenga cambios nuevos, actualiza tu copia local con:

```powershell
# Asegúrate de estar en la carpeta del proyecto
cd C:\Proyectos\proyecto_turboreactor

# Descargar e integrar los cambios del repositorio remoto
git pull
```

### Después de actualizar

Si se agregaron nuevas dependencias, vuelve a instalarlas:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si se modificaron pruebas o código, verifica que todo sigue funcionando:

```powershell
pytest tests/ -v
```

---

## 17. Problemas comunes y solución

### `python` no se reconoce como comando

**Síntoma**

```
python : El término 'python' no se reconoce...
```

**Causa**

Python no fue agregado al PATH durante la instalación.

**Solución**

1. Abre el instalador de Python de nuevo y elige **Modify**.
2. Avanza hasta **Advanced Options** y marca **"Add Python to environment variables"**.
3. Haz clic en **Install** y reinicia PowerShell.

Alternativamente, usa `py` en lugar de `python`:

```powershell
py --version
py -m venv .venv
```

---

### PowerShell bloquea la activación del entorno virtual

**Síntoma**

```
.venv\Scripts\Activate.ps1 : No se puede cargar el archivo porque la ejecución
de scripts está deshabilitada en este sistema.
```

**Solución**

Ejecuta en PowerShell (puede requerir abrir como administrador):

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Si no tienes permisos de administrador, usa solo para la sesión actual:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

---

### `streamlit` no se reconoce después de instalar

**Síntoma**

```
streamlit : El término 'streamlit' no se reconoce...
```

**Causa**

El entorno virtual no está activado.

**Solución**

```powershell
.venv\Scripts\Activate.ps1
streamlit run app.py
```

Verifica que el prompt muestre el prefijo `(.venv)` antes de ejecutar cualquier
comando del proyecto.

---

### La app no abre el navegador automáticamente

**Solución**

Abre manualmente el navegador y navega a:

```
http://localhost:8501
```

---

### Error `ModuleNotFoundError` al ejecutar la app o las pruebas

**Síntoma**

```
ModuleNotFoundError: No module named 'streamlit'
```

**Causa**

Las dependencias no están instaladas en el entorno activo.

**Solución**

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### El puerto 8501 ya está en uso

**Síntoma**

```
OSError: [Errno 98] Address already in use
```

**Solución**

Usa un puerto diferente:

```powershell
streamlit run app.py --server.port 8502
```

Luego abre `http://localhost:8502` en el navegador.

---

### `pytest` no encuentra los módulos de `src/`

**Síntoma**

```
ModuleNotFoundError: No module named 'src'
```

**Causa**

pytest no está ejecutándose desde la raíz del proyecto.

**Solución**

Asegúrate de estar en la carpeta raíz antes de ejecutar pytest:

```powershell
cd C:\Proyectos\proyecto_turboreactor
pytest tests/ -v
```

---

### `git pull` devuelve conflictos

**Síntoma**

```
CONFLICT (content): Merge conflict in archivo.py
```

**Solución**

Si no tienes cambios locales propios que quieras conservar:

```powershell
git fetch origin
git reset --hard origin/main
```

> **Advertencia:** este comando descarta todos tus cambios locales no
> confirmados. Úsalo solo si estás seguro de que no perderás trabajo importante.

Si tienes cambios que quieres conservar, consulta con el responsable del
proyecto antes de resolver el conflicto.
