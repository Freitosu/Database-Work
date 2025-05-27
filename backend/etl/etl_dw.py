import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import psycopg2
from psycopg2 import sql, OperationalError, DatabaseError
from datetime import datetime, timedelta
import random
import logging
from contextlib import contextmanager

from zodb.db import JogoDB

# Configuração básica do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@contextmanager
def get_pg_connection():
    """Gerenciador de contexto para conexão PostgreSQL"""
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Hum",
            user="postgres",
            password="1234"
        )
        yield conn
    except OperationalError as e:
        logging.error(f"Erro na conexão com PostgreSQL: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logging.info("Conexão com PostgreSQL encerrada.")

def insert_dim_jogo(conn, jogo):
    """Insere ou retorna o jogo na dimensão"""
    with conn.cursor() as cur:
        try:
            cur.execute("""
                SELECT jogo_id FROM dw.dim_jogo WHERE titulo = %s AND ano = %s
            """, (jogo.titulo, jogo.ano))
            result = cur.fetchone()
            if result:
                logging.debug(f"Jogo '{jogo.titulo}' já existe na dimensão com ID {result[0]}")
                return result[0]

            cur.execute("""
                INSERT INTO dw.dim_jogo (titulo, descricao, ano, categoria, duracao)
                VALUES (%s, %s, %s, %s, %s) RETURNING jogo_id
            """, (jogo.titulo, jogo.descricao, jogo.ano, jogo.categoria, jogo.duracao))
            jogo_id = cur.fetchone()[0]
            conn.commit()
            logging.info(f"Jogo '{jogo.titulo}' inserido com ID {jogo_id}")
            return jogo_id
        except DatabaseError as e:
            conn.rollback()
            logging.error(f"Erro ao inserir jogo '{jogo.titulo}': {e}")
            raise

def insert_dim_tempo(conn, data_venda):
    """Insere ou retorna a data na dimensão tempo"""
    with conn.cursor() as cur:
        try:
            cur.execute("""
                SELECT tempo_id FROM dw.dim_tempo WHERE data_venda = %s
            """, (data_venda,))
            result = cur.fetchone()
            if result:
                logging.debug(f"Data {data_venda} já existe na dimensão tempo com ID {result[0]}")
                return result[0]

            cur.execute("""
                INSERT INTO dw.dim_tempo (data_venda, ano, mes, dia)
                VALUES (%s, %s, %s, %s) RETURNING tempo_id
            """, (data_venda, data_venda.year, data_venda.month, data_venda.day))
            tempo_id = cur.fetchone()[0]
            conn.commit()
            logging.info(f"Data {data_venda} inserida com ID {tempo_id}")
            return tempo_id
        except DatabaseError as e:
            conn.rollback()
            logging.error(f"Erro ao inserir data {data_venda}: {e}")
            raise

def insert_fato_venda(conn, jogo_id, tempo_id, preco, quantidade):
    """Insere registro de fato venda"""
    with conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO dw.fato_venda (jogo_id, tempo_id, preco, quantidade)
                VALUES (%s, %s, %s, %s)
            """, (jogo_id, tempo_id, preco, quantidade))
            conn.commit()
            logging.debug(f"Fato venda inserido - jogo_id: {jogo_id}, tempo_id: {tempo_id}, quantidade: {quantidade}")
        except DatabaseError as e:
            conn.rollback()
            logging.error(f"Erro ao inserir fato venda: {e}")
            raise

def simular_vendas_ultimos_30_dias(conn, jogo):
    """Simula vendas para os últimos 30 dias para um jogo específico"""
    for dias_atras in range(30):
        data_venda = datetime.now().date() - timedelta(days=dias_atras)
        tempo_id = insert_dim_tempo(conn, data_venda)
        quantidade = random.randint(0, 5)
        if quantidade > 0:
            insert_fato_venda(conn, jogo_id=jogo['id'], tempo_id=tempo_id, preco=jogo['preco'], quantidade=quantidade)
            logging.info(f"Venda simulada em {data_venda} - {quantidade} unidades do jogo '{jogo['titulo']}'")

def remover_jogos_antigos(conn, jogos_zodb):
    """Remove do DW jogos que não existem mais no ZODB"""
    ids_zodb = set(j.id for j in jogos_zodb)
    with conn.cursor() as cur:
        cur.execute("SELECT jogo_id FROM dw.dim_jogo")
        ids_dw = set(row[0] for row in cur.fetchall())
        ids_para_remover = ids_dw - ids_zodb
        for jogo_id in ids_para_remover:
            cur.execute("DELETE FROM dw.fato_venda WHERE jogo_id = %s", (jogo_id,))
            cur.execute("DELETE FROM dw.dim_jogo WHERE jogo_id = %s", (jogo_id,))
        if ids_para_remover:
            conn.commit()
            logging.info(f"Removidos jogos do DW: {ids_para_remover}")

def main():
    logging.info("Início do ETL de vendas")

    zodb = JogoDB()
    jogos = zodb.listar_jogos()
    logging.info(f"Total de jogos encontrados no ZODB: {len(jogos)}")

    with get_pg_connection() as conn:
        remover_jogos_antigos(conn, jogos)
        for jogo in jogos:
            try:
                jogo_id = insert_dim_jogo(conn, jogo)
                jogo_info = {
                    'id': jogo_id,
                    'titulo': jogo.titulo,
                    'preco': jogo.preco
                }
                simular_vendas_ultimos_30_dias(conn, jogo_info)
            except Exception as e:
                logging.error(f"Erro ao processar jogo {jogo.titulo}: {e}")

    zodb.fechar()
    logging.info("ETL finalizado com sucesso.")

if __name__ == "__main__":
    main()
