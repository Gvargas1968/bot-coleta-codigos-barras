# Instruções para executar o Bot de Coleta de Códigos de Barras localmente

## Passo 1: Configurar o IP do servidor Docker

Antes de executar o bot, é necessário configurar o IP correto do servidor onde o Docker está rodando.

1. No arquivo `.env.local`, substitua `endereco_ip_do_servidor` pelo IP real do servidor Docker.
   Exemplo: Se o IP do servidor for 192.168.1.100, altere:
   ```
   MYSQL_HOST=endereco_ip_do_servidor
   ```
   para:
   ```
   MYSQL_HOST=192.168.1.100
   ```

## Passo 2: Testar a conexão com o banco de dados

Execute o script de teste para verificar se a conexão com o banco de dados está funcionando:

```
python test_db_connection.py
```

Se aparecer a mensagem "[SUCCESS] Conexao bem sucedida ao banco de dados!", a conexão está funcionando corretamente.

## Passo 3: Executar o bot

Após confirmar que a conexão com o banco de dados está funcionando, execute o bot com o comando:

```
python ColetasCodBarraMultiplos.py
```

## Observações:

- O token do Telegram já está configurado no projeto, mas pode ser necessário atualizá-lo se o bot não funcionar corretamente
- Certifique-se de que a porta 3306 no servidor Docker está acessível a partir da sua máquina local
- Se ocorrerem erros de conexão, verifique se o firewall do servidor permite conexões na porta 3306