import mysql.connector
from config_bot_ColetaBFF import MYSQL_CONFIG

def test_db_connection():
    """
    Testa a conexão com o banco de dados MySQL
    """
    try:
        print("Tentando conectar ao banco de dados...")
        print(f"Host: {MYSQL_CONFIG['host']}")
        print(f"Port: {MYSQL_CONFIG.get('port', 3306)}")
        print(f"User: {MYSQL_CONFIG['user']}")
        print(f"Database: {MYSQL_CONFIG['database']}")
        
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        
        if connection.is_connected():
            print("\n[SUCCESS] Conexao bem sucedida ao banco de dados!")
            db_info = connection.get_server_info()
            print(f"Versao do MySQL: {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            database_name = cursor.fetchone()
            print(f"Banco de dados selecionado: {database_name[0]}")
            
            # Testar se a tabela 'coletados' existe
            cursor.execute("SHOW TABLES LIKE 'coletados';")
            table_exists = cursor.fetchone()
            if table_exists:
                print(f"Tabela 'coletados' encontrada: {table_exists[0]}")
                
                # Contar registros existentes
                cursor.execute("SELECT COUNT(*) FROM coletados;")
                count = cursor.fetchone()[0]
                print(f"Registros existentes na tabela 'coletados': {count}")
            else:
                print("[WARNING] Aviso: Tabela 'coletados' nao encontrada")
                
            cursor.close()
        
        connection.close()
        print("\nConexao com o banco de dados fechada.")
        
    except mysql.connector.Error as err:
        print(f"\n[ERROR] Erro ao conectar ao banco de dados MySQL: {err}")
        return False
    except Exception as e:
        print(f"\n[ERROR] Erro inesperado: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_db_connection()