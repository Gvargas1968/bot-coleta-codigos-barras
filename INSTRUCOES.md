# Instruções para executar o Bot de Coleta de Códigos de Barras localmente

## Passo 1: Configurar variáveis de ambiente de forma segura

Antes de executar o bot, é necessário configurar as variáveis de ambiente de forma segura, substituindo os valores padrão sensíveis:

1. Crie um arquivo `.env.local` no diretório raiz (já está incluído no .gitignore)
2. Configure as variáveis obrigatórias:

```
TELEGRAM_TOKEN=seu_token_real_aqui
MYSQL_HOST=endereco_ip_do_servidor
MYSQL_PORT=3306
MYSQL_USER=seu_usuario
MYSQL_PASSWORD=sua_senha_segura
MYSQL_DATABASE=nome_do_banco
```

**IMPORTANTE**: Substitua `endereco_ip_do_servidor` pelo IP real do servidor Docker.
Exemplo: Se o IP do servidor for 192.168.1.100, altere:
```
MYSQL_HOST=192.168.1.100
```

**ATENÇÃO**: Este projeto agora inclui validações de segurança que impedem a execução se variáveis críticas não estiverem configuradas.

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

Ou utilize o script de inicialização para Windows:

```
iniciar_bot.bat
```

## Observações de Segurança:

- **O token do Telegram NÃO deve estar hardcoded no código fonte**
- **A senha do banco de dados NÃO deve estar hardcoded no código fonte**
- **Certifique-se de que seu arquivo .env.local está no .gitignore e NÃO será commitado**
- **Nunca compartilhe valores de variáveis de ambiente em repositórios públicos**
- **Certifique-se de que a porta 3306 no servidor Docker está acessível a partir da sua máquina local**
- **Se ocorrerem erros de conexão, verifique se o firewall do servidor permite conexões na porta 3306**