# proyecto_turboreactor

Calculadora local de propiedades termodinámicas para toberas de turbofán,
basada en análisis isentrópico 1-D con número de Mach variable.

---

## Objetivo

Proporcionar una herramienta interactiva que permita analizar el comportamiento
termodinámico del gas a lo largo de una tobera de turbofán bajo supuestos de
flujo isentrópico, ideal para estudios de diseño preliminar, validación académica
y exploración paramétrica de ciclos de propulsión.

---

## Modelo físico

El análisis se basa en las relaciones isentrópicas para flujo compresible
unidimensional estacionario de un gas caloricamente perfecto.

### Secuencia de cálculo por punto

Dado un rango de presiones estáticas P desde la presión de remanso P₀ hasta la
presión de descarga P_salida, en cada punto se calcula:

| Paso | Variable | Fórmula |
| ---- | -------- | ------- |
| 1 | Número de Mach M | `M = √{ (2/(γ−1)) · [(P₀/P)^((γ−1)/γ) − 1] }` |
| 2 | Temperatura estática T | `T = T₀ / [1 + (γ−1)/2 · M²]` |
| 3 | Velocidad del sonido a | `a = √(γ R T)` |
| 4 | Velocidad del flujo V | `V = √[2γR(T₀ − T) / (γ−1)]` |
| 5 | Densidad ρ | `ρ = P / (R T)` &nbsp; *(ley del gas ideal)* |
| 6 | Área transversal A | `A = ṁ / (ρ V)` &nbsp; *(ecuación de continuidad)* |

### Variables de entrada del usuario

| Símbolo | Descripción | Unidad |
| ------- | ----------- | ------ |
| P₀ | Presión de remanso en la entrada | kPa |
| P_salida | Presión estática de descarga | kPa |
| T₀ | Temperatura de remanso en la entrada | K |
| ṁ | Gasto másico | kg/s |
| γ | Razón de calores específicos Cp/Cv | — |
| R | Constante específica del gas | J/(kg·K) |
| N | Número de puntos de discretización | — |

---

## Variables calculadas

El modelo produce un perfil de las siguientes variables a lo largo del rango de
presiones especificado:

| Variable | Símbolo | Descripción | Unidad |
| -------- | ------- | ----------- | ------ |
| Presión estática | P | Presión termodinámica local del gas en cada sección. Disminuye conforme el gas se expande hacia la salida. | kPa |
| Temperatura estática | T | Temperatura del gas en el marco de referencia del fluido. Cae al convertirse entalpía en energía cinética. | K |
| Velocidad | V | Velocidad axial del flujo calculada a partir de la caída de entalpía entre el estado total y el estático. | m/s |
| Número de Mach | M | Relación entre la velocidad del flujo y la velocidad local del sonido. Aumenta monótonamente al disminuir la presión. | — |
| Densidad | ρ | Masa por unidad de volumen del gas, obtenida mediante la ley del gas ideal. | kg/m³ |
| Área de flujo | A | Sección transversal requerida por la ecuación de continuidad para el gasto másico dado. | m² |
| Radio equivalente | R | Radio de una sección circular cuya área coincide con el área de flujo calculada. | m |

### Radio equivalente de flujo

El radio equivalente convierte el área de flujo en una dimensión geométrica
intuitiva asumiendo que la sección transversal de la tobera es circular.

**Supuesto geométrico:** la sección transversal es un círculo, por lo que:

```math
A = π R²
```

Despejando el radio:

```math
R = √(A / π)
```

Esta relación es la inversa directa de la fórmula del área del círculo.
No requiere hipótesis adicionales sobre el flujo; sólo describe la geometría
implícita de una tobera de revolución.

> **Interpretación física:** El radio equivalente permite relacionar el
> comportamiento termodinámico del flujo con la geometría requerida de la
> tobera. Al ver cómo evoluciona R con la presión, el ingeniero puede estimar
> directamente el diámetro de cada sección sin pasar por el área.

**Nota:** en el punto de remanso (P = P₀, M = 0, V = 0) el área no está
definida y, por tanto, el radio equivalente también se registra como `NaN`
en esa fila del resultado.

---

## Supuestos del MVP

1. **Flujo isentrópico** — proceso adiabático y sin irreversibilidades (sin fricción,
   sin transferencia de calor).
2. **Flujo 1-D** — las propiedades del gas son uniformes en cada sección transversal.
3. **Gas caloricamente perfecto** — γ, Cp y R constantes a lo largo del análisis.
4. **Presión de remanso P₀ constante** — no hay pérdidas de presión total aguas arriba.
5. **Gasto másico constante** — conservación de masa en toda la tobera.
6. **Punto de entrada en reposo** — en P = P₀ el Mach es 0; el área es físicamente
   indefinida y se reporta como NaN en esa fila del resultado.
7. **Cp del aire lineal** — aproximación `Cp = 1005 + 0.1 · (T − 300)` válida en
   el rango 200–1500 K; no apta para temperaturas de disociación (> 2500 K).
8. **Sin efectos de onda de choque** — el modelo no detecta ni corrige discontinuidades
   por ondas de choque normales en la tobera divergente.

---

## Stack tecnológico

| Componente | Tecnología | Versión mínima |
| ---------- | ---------- | -------------- |
| Interfaz gráfica | [Streamlit](https://streamlit.io) | 1.35 |
| Cálculo numérico | [NumPy](https://numpy.org) | 1.26 |
| Tablas de resultados | [Pandas](https://pandas.pydata.org) | 2.2 |
| Gráficas interactivas | [Plotly](https://plotly.com/python) | 5.22 |
| Gráficas estáticas | [Matplotlib](https://matplotlib.org) | 3.8 |
| Pruebas unitarias | [pytest](https://pytest.org) | 8.0 |
| Lenguaje | Python | 3.10+ |

---

## Estructura de carpetas

```text
proyecto_turboreactor/
│
├── app.py                        # Punto de entrada — interfaz Streamlit
├── requirements.txt              # Dependencias del proyecto
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── calculations.py           # Relaciones isentrópicas, Mach, velocidad,
│   │                             # densidad, área, tabla de resultados
│   ├── gas_properties.py         # Propiedades del gas: densidad, velocidad del
│   │                             # sonido, Cp, γ (ley de gas ideal)
│   └── plotting.py               # Gráficas Plotly y Matplotlib
│
└── tests/
    ├── __init__.py
    └── test_calculations.py      # Pruebas unitarias de todas las funciones
```

---

## Instalación en macOS

### Requisitos previos — macOS

- Python 3.10 o superior (`python3 --version`)
- pip actualizado

### Pasos en macOS

```bash
# 1. Clonar o descargar el repositorio
git clone <url-del-repositorio>
cd proyecto_turboreactor

# 2. Crear entorno virtual
python3 -m venv .venv

# 3. Activar el entorno virtual
source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

Para desactivar el entorno cuando termines:

```bash
deactivate
```

---

## Instalación en Windows

### Requisitos previos — Windows

- Python 3.10 o superior desde [python.org](https://www.python.org/downloads/)
  (marcar **Add Python to PATH** durante la instalación)
- pip actualizado

### Pasos en PowerShell o CMD

```powershell
# 1. Clonar o descargar el repositorio
git clone <url-del-repositorio>
cd proyecto_turboreactor

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar el entorno virtual
.venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

> Si PowerShell bloquea la activación por política de ejecución, ejecutar
> primero: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

Para desactivar el entorno cuando termines:

```powershell
deactivate
```

---

## Cómo ejecutar la app

Con el entorno virtual activado, desde la raíz del proyecto:

```bash
streamlit run app.py
```

Streamlit abrirá automáticamente el navegador en `http://localhost:8501`.

### Flujo de uso

1. En el **panel lateral izquierdo**, introducir los parámetros de entrada:
   - Presión total de entrada P₀ y presión de salida.
   - Temperatura total T₀ y gasto másico ṁ.
   - Propiedades del gas: γ y R.
   - Número de puntos de discretización.
2. Presionar el botón **Calcular**.
3. Revisar las **métricas** en la parte superior: Mach máximo, velocidad máxima,
   densidad inicial, área de salida y radio equivalente final.
4. Explorar la **tabla de resultados** (primeras 20 filas visibles).
5. Analizar los **perfiles termodinámicos** en las gráficas interactivas:
   - Presión estática vs Velocidad
   - Presión estática vs Número de Mach
   - Presión estática vs Temperatura estática
   - Presión estática vs Densidad
   - Presión estática vs Área de flujo
   - **Radio equivalente vs presión**
6. Revisar la **comparación normalizada de tendencias**: todas las propiedades
   (incluyendo el radio equivalente) normalizadas al rango [0, 1] para comparar
   su evolución en la misma escala, independientemente de sus unidades.
7. Descargar el resultado completo en formato CSV.

---

## Cómo correr las pruebas

```bash
# Todas las pruebas
pytest tests/

# Con reporte de cobertura por módulo
pytest tests/ -v

# Solo las pruebas de una función específica
pytest tests/ -k "density"
pytest tests/ -k "mach"
pytest tests/ -k "pressure_ratio"
```

Las pruebas unitarias cubren:

**`gas_properties`**

- `calculate_density`, `calculate_speed_of_sound`, `calculate_cp_air`, `calculate_gamma`

**`calculations`**

- `generate_pressure_range`, `calculate_velocity_from_mach`, `calculate_mach_number`
- `calculate_flow_area`, `calculate_radius_from_area`, `build_results_table`
- `calculate_static_temperature`, `calculate_static_pressure`
- `calculate_velocity_from_temperature`, `calculate_mach_from_pressure_ratio`

Cada función tiene pruebas de:

- **Caso válido** con valor numérico conocido.
- **Propiedades físicas** (monotonicidad, proporcionalidad, roundtrip).
- **Casos de error** con `ValueError` esperado para entradas inválidas.

---

## Cómo exportar el CSV

1. Ejecutar la app y presionar **Calcular**.
2. Hacer clic en el botón **Descargar CSV completo** que aparece bajo la tabla.
3. El archivo `turbofan_nozzle_results.csv` se guardará en la carpeta de descargas
   del navegador.

### Columnas del CSV exportado

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
> P = P₀ el fluido está en reposo (M = 0, V = 0) y el área es indefinida.

---

## Limitaciones actuales

- **Modelo aún idealizado** — los resultados representan el límite teórico
  isentrópico; las condiciones reales de operación siempre difieren por efectos
  no modelados.
- **Sin pérdidas viscosas** — no se consideran fricción en la pared ni capa
  límite; la presión total se conserva perfectamente, lo que sobreestima la
  velocidad y el empuje en diseños reales.
- **Sin transferencia de calor** — el proceso se modela como completamente
  adiabático; en toberas refrigeradas o en presencia de flujo de calor hacia
  la pared esto introduce error significativo.
- **Solo secciones circulares** — el radio equivalente asume geometría de
  revolución. Toberas de sección rectangular, elíptica o tipo "slot" no
  pueden representarse con esta formulación.
- **Sin ondas de choque** — el modelo no detecta ni modela discontinuidades.
  Los resultados en condiciones supersónicas fuertes pueden no ser físicamente
  representativos sin verificar el régimen de operación.
- **γ y R constantes** — no se modela la variación de propiedades con la
  temperatura (gas caloricamente imperfecto). Esto introduce error a temperaturas
  muy altas (> 1500 K) o en presencia de disociación.
- **Flujo 1-D** — no se capturan efectos de capa límite, perfil de velocidades
  radial ni separación del flujo.
- **Sin geometría explícita** — la tobera no tiene forma definida; el análisis
  se realiza sobre el rango de presiones, no sobre coordenadas axiales.
- **Temperatura constante** — T₀ se trata como uniforme en toda la entrada;
  no se modela variación radial de temperatura.
- **Sin análisis de empuje** — `analyze_nozzle` aún no está implementada; el
  cálculo de empuje bruto y evaluación de ahogamiento están pendientes.
- **`flow_area_m2` y `radius_m` = NaN en el punto inicial** — consecuencia del
  punto de remanso donde V = 0; deben omitirse al graficar o analizar estas columnas.

---

## Próximos pasos técnicos

### Física y modelo

- [ ] **Flujo ahogado (choking flow)** — detectar automáticamente cuándo la
      garganta alcanza M = 1 y limitar el cálculo al régimen subsónico correcto
      cuando la contrapresión supera el valor crítico.
- [ ] **Área crítica A\*** — calcular y mostrar el área de la garganta donde
      M = 1, como referencia de diseño fundamental de la tobera.
- [ ] **Relaciones A/A\*** — implementar `mach_from_area_ratio` para obtener
      el número de Mach a partir de la razón de área local respecto a la
      garganta, habilitando el análisis geométrico completo de la tobera.
- [ ] **Régimen supersónico** — extender el modelo para cubrir la rama
      supersónica (M > 1) de la relación A/A\*, incluyendo la detección de
      la condición de sobre- y sub-expansión en la salida.
- [ ] Implementar `analyze_nozzle`: cálculo completo de empuje bruto, verificación
      de ahogamiento y clasificación del tipo de tobera.
- [ ] Agregar modelo de onda de choque normal para condiciones de sub-expansión
      en toberas convergentes-divergentes.
- [ ] Incorporar propiedades variables con la temperatura (tablas de gas real
      o polinomios de la NASA para Cp(T)).

### Ingeniería de software

- [ ] Completar implementación de `get_air_properties` y
      `get_combustion_gas_properties` con correlaciones publicadas.
- [ ] Agregar cobertura de pruebas con `pytest-cov` y reporte de porcentaje.
- [ ] Implementar `plot_mach_profile`, `plot_pressure_profile`,
      `plot_temperature_profile` y `plot_results_summary` en Matplotlib.
- [ ] Separar la lógica de la app en funciones para facilitar pruebas de
      integración de la interfaz.

### Interfaz y experiencia de usuario

- [ ] Agregar selector de tipo de gas (aire, gas de combustión) para cargar
      propiedades preconfiguradas.
- [ ] Incluir gráfica de perfil geométrico (área vs posición axial) cuando
      se implemente la relación A/A*.
- [ ] Permitir comparar dos condiciones de operación en la misma gráfica.
- [ ] Agregar exportación a PDF del reporte completo.
