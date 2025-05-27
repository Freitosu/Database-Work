# Sistema de Gerenciamento de Jogos com ZODB, MongoDB e ETL para Data Warehouse

Instruções

### 1. Execução

- Para iniciar o sistema, execute o arquivo principal.
- O sistema exibirá um menu interativo no terminal.

### 2. Menu Principal

As opções típicas do menu incluem:
- **Cadastrar Jogo:** Insira os dados solicitados para adicionar um novo jogo.
- **Listar Jogos:** Exibe todos os jogos cadastrados.
- **Buscar Jogo:** Permite buscar um jogo pelo nome ou outro critério.
- **Atualizar Jogo:** Selecione um jogo e altere suas informações.
- **Remover Jogo:** Exclua um jogo do sistema.
- **Adicionar Comentário:** Escolha um jogo e insira um comentário e avaliação.
- **Sair:** Ao sair, o ETL será executado automaticamente.
Este projeto é um sistema de gerenciamento de jogos que utiliza múltiplos bancos de dados:  
- **ZODB** para persistência dos dados principais dos jogos e usuários  
- **MongoDB** para armazenamento de comentários dos usuários  
- **PostgreSQL (Data Warehouse)** para análises de vendas simuladas via processo ETL

## Estrutura do Projeto

## Principais Funcionalidades

- **CRUD de Jogos:**  
  Criação, listagem, busca, atualização e remoção de jogos persistidos no ZODB.

- **Comentários:**  
  Usuários podem adicionar comentários e avaliações aos jogos, armazenados no MongoDB.

- **ETL para Data Warehouse:**  
  O script [`etl/etl_dw.py`](etl/etl_dw.py) simula vendas dos jogos e alimenta tabelas dimensionais e fato em um banco PostgreSQL para análises.

## Como Executar

1. **Instale as dependências:**
2. **Configure os bancos de dados:**
- ZODB: Não requer configuração adicional, armazena dados em `jogos.fs`.
- PostgreSQL: Crie o banco `Hum` e as tabelas necessárias no schema `dw` (veja o script ETL para estrutura).

3. **Execute o sistema:**

O menu interativo permite gerenciar jogos e, ao sair, executa automaticamente o ETL para atualizar o Data Warehouse.

## Observações

- O arquivo [`jogo_view.py`](jogo_view.py) contém um exemplo de API REST (comentado).
- O ETL simula vendas dos últimos 30 dias para cada jogo.
- Usuários e autenticação estão parcialmente implementados/comentados.

## Créditos

Desenvolvido para fins acadêmicos.
