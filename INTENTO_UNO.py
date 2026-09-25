import argparse
import os
import sys
import pandas as pd


def detectar_columna_stock(df, columna_solicitada=None):
    """Busca la columna de stock especificada o intenta deducirla."""
    if columna_solicitada:
        if columna_solicitada in df.columns:
            return columna_solicitada
        else:
            raise ValueError(
                f"La columna '{columna_solicitada}' no existe en el archivo. "
                f"Columnas encontradas: {list(df.columns)}"
            )

    posibles_nombres = [
        "stock", "cantidad", "stock_disponible", "disponible",
        "existencias", "inventario", "qty", "quantity", "inventory",
    ]

    for col in df.columns:
        if str(col).strip().lower() in posibles_nombres:
            return col

    for col in df.columns:
        col_lower = str(col).strip().lower()
        if any(term in col_lower for term in ["stock", "cant", "existenc"]):
            return col

    return None


def leer_archivo(ruta_entrada):
    """Lee el archivo CSV o Excel manejando delimitadores y codificaciones comunes."""
    extension = os.path.splitext(ruta_entrada)[1].lower()

    if extension in [".xlsx", ".xls"]:
        return pd.read_excel(ruta_entrada)

    encodings = ["utf-8-sig", "utf-8", "latin1", "cp1252"]
    separadores = [None, ";", ","]

    for enc in encodings:
        for sep in separadores:
            try:
                if sep is None:
                    df = pd.read_csv(ruta_entrada, encoding=enc, sep=sep, engine="python")
                else:
                    df = pd.read_csv(ruta_entrada, encoding=enc, sep=sep)
                if len(df.columns) > 1 or (len(df.columns) == 1 and sep == ","):
                    return df
            except Exception:
                continue

    return pd.read_csv(ruta_entrada)


def procesar_archivo(ruta_entrada, ruta_salida=None, col_stock=None, ascendente=True, min_stock=None):
    if not os.path.exists(ruta_entrada):
        print(f"[ERROR] El archivo no existe: {ruta_entrada}")
        return None

    print(f"\n[CARGANDO] Archivo: {ruta_entrada}...")
    df = leer_archivo(ruta_entrada)
    print(f"[OK] Archivo cargado. ({len(df)} filas, {len(df.columns)} columnas)")
    print(f"     Columnas encontradas: {list(df.columns)}")

    # Identificar columna de stock
    col_seleccionada = detectar_columna_stock(df, col_stock)
    if not col_seleccionada:
        print("\n[ADVERTENCIA] No se pudo detectar la columna de stock automaticamente.")
        print(f"Columnas disponibles: {list(df.columns)}")
        col_seleccionada = input("Ingresa el nombre exacto de la columna a ordenar: ").strip()
        if col_seleccionada not in df.columns:
            print("[ERROR] Columna no encontrada. Operacion cancelada.")
            return None

    print(f"[USANDO] Columna: '{col_seleccionada}'")

    # Limpieza: convertir a numerico, reemplazar vacios con 0 para el calculo
    df[col_seleccionada] = pd.to_numeric(
        df[col_seleccionada].astype(str).str.replace(r"[^\d.-]", "", regex=True),
        errors="coerce"
    ).fillna(0)

    # Filtrar por stock minimo si se especifico
    if min_stock is not None:
        df = df[df[col_seleccionada] >= min_stock]
        print(f"[FILTRADO] Solo registros con '{col_seleccionada}' >= {min_stock}")

    # Ordenar de menor a mayor por defecto (ascendente=True)
    df_ordenado = df.sort_values(by=col_seleccionada, ascending=ascendente)
    direccion = "menor a mayor" if ascendente else "mayor a menor"
    print(f"[ORDENADO] De {direccion} por '{col_seleccionada}'")

    # Determinar ruta de salida
    if not ruta_salida:
        dir_name, file_name = os.path.split(ruta_entrada)
        base_name, ext = os.path.splitext(file_name)
        sufijo = "_menor_mayor" if ascendente else "_mayor_menor"
        ruta_salida = os.path.join(dir_name, f"{base_name}_ordenado_stock{sufijo}.xlsx")

    # Asegurar que sea .xlsx
    if not ruta_salida.lower().endswith(('.xlsx', '.xls')):
        ruta_salida = os.path.splitext(ruta_salida)[0] + ".xlsx"

    # Guardar como Excel
    df_ordenado.to_excel(ruta_salida, index=False, engine='openpyxl')
    print(f"\n[COMPLETADO] Proceso terminado exitosamente!")
    print(f"[GUARDADO] Archivo resultante en: {ruta_salida}")
    print(f"           ({len(df_ordenado)} registros)")

    # Mostrar resumen en consola
    print(f"\n--- RESUMEN ---")
    print(df_ordenado.to_string(index=False))
    print("-------------")

    return ruta_salida


def main():
    parser = argparse.ArgumentParser(description="Ordena archivos Excel/CSV por stock disponible.")
    parser.add_argument("-i", "--input", help="Ruta al archivo original (CSV o XLSX)")
    parser.add_argument("-o", "--output", help="Ruta donde se guardara el nuevo archivo (opcional)")
    parser.add_argument("-c", "--columna", help="Nombre de la columna de stock (opcional)")
    parser.add_argument(
        "--asc",
        action="store_true",
        help="Ordenar de menor a mayor (por defecto es asi)",
    )
    parser.add_argument(
        "--desc",
        action="store_true",
        help="Ordenar de mayor a menor",
    )
    parser.add_argument(
        "--min",
        type=float,
        default=None,
        help="Filtrar stock minimo (ej: --min 1 para excluir ceros)",
    )

    args = parser.parse_args()

    if not args.input:
        print("=" * 60)
        print("  ORDENADOR DE ARCHIVOS POR STOCK (PANDAS)")
        print("=" * 60)
        ruta_entrada = input("\nIngresa o arrastra la ruta del archivo original: ").strip().strip('"').strip("'")
        col = input("Columna de stock (deja vacio para auto-detectar): ").strip() or None

        sentido = input("Ordenar de menor a mayor? (S/n): ").strip().lower()
        ascendente = True if sentido != "n" else False

        min_str = input("Filtrar stock minimo? (ej. 1 para omitir ceros, o Enter para omitir): ").strip()
        min_stock = float(min_str) if min_str else None

        procesar_archivo(
            ruta_entrada=ruta_entrada,
            col_stock=col,
            ascendente=ascendente,
            min_stock=min_stock,
        )
    else:
        # Si se paso --desc sin --asc, invertir
        ascendente = not args.desc if args.desc else args.asc
        procesar_archivo(
            ruta_entrada=args.input,
            ruta_salida=args.output,
            col_stock=args.columna,
            ascendente=ascendente,
            min_stock=args.min,
        )


if __name__ == "__main__":
    main()
