import sqlite3

# Conectar a la base de datos y crear la base de datos y tablas si no existen
conn = sqlite3.connect('/workspaces/experiment_python/results/test_results.db')

# Crear tabla para resultados de las pruebas con un campo de marca de tiempo
conn.execute('''
CREATE TABLE IF NOT EXISTS test_results (
    test_name TEXT NOT NULL,
    outcome TEXT NOT NULL,
    duration REAL,
    error_message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Crear tabla para resultados del análisis estático con un campo de marca de tiempo
conn.execute('''
CREATE TABLE IF NOT EXISTS static_analysis_results (
    tool TEXT NOT NULL,
    issues INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
