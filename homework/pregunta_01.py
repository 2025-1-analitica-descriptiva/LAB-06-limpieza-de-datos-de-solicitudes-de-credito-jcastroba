"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import os
    import pandas as pd

    input_file = 'files/input/solicitudes_de_credito.csv'
    output_dir = 'files/output'
    output_file = os.path.join(output_dir, 'solicitudes_de_credito.csv')
    
    df = pd.read_csv(input_file, sep=';')
    df.drop(['Unnamed: 0'], axis = 1, inplace = True)
    df.dropna(inplace = True)
    df.drop_duplicates(inplace = True)

    df[['día', 'mes', 'año']] = df['fecha_de_beneficio'].str.split('/', expand = True)
    df.loc[df['año'].str.len() < 4, ['día', 'año']] = df.loc[df['año'].str.len() < 4, ['año', 'día']].values
    df['fecha_de_beneficio'] = df['año'] + '-' + df['mes'] + '-' + df['día']
    df.drop(['día', 'mes', 'año'], axis = 1, inplace = True)

    categorical_columns = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito']
    df[categorical_columns] = df[categorical_columns].apply(lambda x: x.str.lower().replace(['-', '_'], ' ', regex = True).str.strip())
    df['barrio'] = df['barrio'].str.lower().replace(['-', '_'], ' ', regex = True)

    df['monto_del_credito'] = df['monto_del_credito'].str.replace("[$, ]", "", regex = True).str.strip()
    df['monto_del_credito'] = pd.to_numeric(df['monto_del_credito'], errors='coerce')
    df['monto_del_credito'] = df['monto_del_credito'].fillna(0).astype(int)
    df['monto_del_credito'] = df['monto_del_credito'].astype(str).str.replace('.00', '')

    df.drop_duplicates(inplace = True)
   
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_file, sep=';', index=False)

if __name__ == "__main__":
    pregunta_01()