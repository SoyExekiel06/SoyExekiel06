# MaximalCalc

Calculadora de escritorio maximalista, multiplataforma y profesional. Inspirada funcionalmente en GNOME Calculator, pero con una identidad visual rica, expresiva y detallada que evoca paneles de instrumentos técnicos y software de ingeniería de los 80/90.

## Características

- **4 Modos**: Básico, Avanzado (científico), Financiero y Programador.
- **Parser matemático propio**: Sin `eval()`. Implementado con tokenizador y parser recursivo descendente.
- **Diseño maximalista**: Paneles con profundidad, gradientes, indicadores LED, tipografía técnica y jerarquía visual clara.
- **Temas**: Oscuro, Claro y Automático (detección de sistema).
- **Historial persistente**: Guardado entre sesiones mediante QSettings.
- **Memoria**: MC, MR, M+, M-, MS con indicador visual.
- **Atajos de teclado**: Navegación completa por teclado.
- **Portapapeles**: Copiar, pegar y saneado de entrada.
- **Configurable**: Precisión decimal, modo de ángulos, tema visual.
- **Tests automatizados**: Cobertura del núcleo matemático con pytest.

## Tecnologías

- **Python 3.9+**
- **PySide6** (Qt para Python)
- **pytest** (para tests)

Sin dependencias de red. Funciona 100% offline.

## Requisitos

- Python 3.9 o superior
- pip

## Instalación

### Linux

```bash
cd Llcalculator
python3 -m venv venv
source venv/bin/activate
pip install PySide6 pytest
```

### Windows

```powershell
cd Llcalculator
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install PySide6 pytest
```

## Ejecución

```bash
python main.py
```

## Tests

```bash
pytest tests/
```

## Estructura

```
calculator/
├── main.py
├── requirements.txt
├── README.md
├── core/        # Núcleo matemático
├── modes/       # Lógica de modos
├── ui/          # Interfaz gráfica
├── utils/       # Utilidades
└── tests/       # Tests automatizados
```

## Empaquetar

### Windows (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name MaximalCalc main.py
```

### Linux (AppImage)

Usa `linuxdeploy` o `appimage-builder` tras PyInstaller.

## Licencia

Proyecto educativo. Código abierto para uso personal.