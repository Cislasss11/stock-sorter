# ORDENADOR DE ARCHIVOS POR STOCK

Herramienta en Python (Pandas) para ordenar archivos CSV/Excel por cantidad de stock disponible.

## Características

- Lee archivos `.xlsx`, `.xls` y `.csv` automáticamente
- Detecta automáticamente la columna de stock (`Stock`, `cantidad`, `existencias`, etc.)
- Ordena de menor a mayor o mayor a menor
- Filtra por stock mínimo
- Guarda resultado como `.xlsx`
- Maneja valores nulos (`NaN`) automáticamente

## Uso

### Interactivo (doble clic en INTETO_UNO.exe)
```
INTETO_UNO.exe
```

### Línea de comandos
```
INTETO_UNO.exe -i "archivo.xlsx" -c Stock --asc
```

### Opciones
| Bandera | Descripción |
|---------|-------------|
| `-i` | Ruta al archivo de entrada |
| `-o` | Ruta de salida (opcional) |
| `-c` | Columna de stock (auto-detecta si se omite) |
| `--asc` | Ordenar de menor a mayor (default) |
| `--desc` | Ordenar de mayor a menor |
| `--min N` | Filtrar solo registros con stock >= N |

## Ejemplo

```
INTETO_UNO.exe -i Libro1.xlsx -c Stock --asc --min 1
```

## Dependencias
- Python 3.12+
- pandas
- openpyxl
- PyInstaller (para generar el .exe)

## Instalación rápida (sin Python instalado)
Solo usa `INTETO_UNO.exe` que está incluido. No necesitas instalar nada.
