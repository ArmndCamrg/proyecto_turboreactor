# proyecto_turboreactor

MVP local para el cálculo de propiedades termodinámicas en la tobera de un turbofán.

## Descripción

Aplicación Streamlit que implementa análisis 1-D de flujo isentrópico en toberas convergentes y convergentes-divergentes, orientado al diseño y estudio de propulsión aeronáutica.

## Estructura

```
proyecto_turboreactor/
├── app.py                  # Entrada Streamlit
├── requirements.txt
├── src/
│   ├── calculations.py     # Relaciones isentrópicas, flujo másico, empuje
│   ├── gas_properties.py   # Propiedades termodinámicas del gas
│   └── plotting.py         # Perfiles de Mach, presión y temperatura
└── tests/
    └── test_calculations.py
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

## Uso

1. Ingresar condiciones de remanso (T₀, P₀) y presión ambiente en el panel lateral.
2. Definir la geometría de la tobera (área de garganta y área de salida).
3. Seleccionar propiedades del gas (γ, R).
4. Presionar **Calculate** para obtener:
   - Número de Mach a la salida
   - Velocidad, temperatura y presión de salida
   - Empuje bruto y flujo másico
   - Estado de ahogamiento (choked / no choked)
   - Perfiles axiales de Mach, presión y temperatura

## Física implementada

| Módulo | Contenido |
|--------|-----------|
| `gas_properties` | Propiedades del aire estándar y gases de combustión |
| `calculations` | Razones isentrópicas T₀/T y P₀/P, razón de presión crítica, solución A/A\*, flujo másico ahogado, análisis completo de tobera |
| `plotting` | Perfiles axiales y resumen de resultados |

## Pruebas

```bash
pytest tests/
```

## Estado

MVP — estructura base creada. La lógica de cálculo y visualización se implementa en la siguiente iteración.
