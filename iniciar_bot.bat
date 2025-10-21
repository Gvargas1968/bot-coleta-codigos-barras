@echo off
echo.
echo ##########################################################
echo #                                                        #
echo #    Bem-vindo ao Bot de Coleta de Códigos de Barras     #
echo #                                                        #
echo ##########################################################
echo.

echo Verificando requisitos...

REM Verifica se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado. Por favor, instale o Python antes de continuar.
    pause
    exit /b 1
)

echo [OK] Python encontrado.

REM Verifica se o arquivo de configuracao existe
if not exist "config_bot_ColetaBFF.py" (
    echo [ERRO] Arquivo de configuracao 'config_bot_ColetaBFF.py' nao encontrado.
    pause
    exit /b 1
)

echo [OK] Arquivo de configuracao encontrado.

REM Verifica se o arquivo .env.local existe
if not exist ".env.local" (
    echo [AVISO] Arquivo '.env.local' nao encontrado. Criando arquivo padrao...
    echo # Token do Telegram > .env.local
    echo TELEGRAM_TOKEN=7843033735:AAH93o7O0DGb_aSwC33W_lSpkF5IQmqsL8o >> .env.local
    echo. >> .env.local
    echo # Configuracoes do Banco de Dados MySQL para conexao local >> .env.local
    echo # ATENCAO: Substitua 'endereco_ip_do_servidor' pelo IP REAL do servidor onde o Docker esta rodando >> .env.local
    echo MYSQL_HOST=endereco_ip_do_servidor >> .env.local
    echo MYSQL_PORT=3306 >> .env.local
    echo MYSQL_USER=root >> .env.local
    echo MYSQL_PASSWORD=M^$^&dff!ch >> .env.local
    echo MYSQL_DATABASE=basealephbff >> .env.local
    echo. >> .env.local
    echo [INFO] Arquivo .env.local criado com configuracoes padrao.
    echo [INFO] Voce precisa editar este arquivo com o IP correto do servidor Docker.
    echo [INFO] Execute: notepad .env.local
    pause
    exit /b 0
)

REM Verifica se as variáveis sensíveis foram configuradas
findstr /C:"endereco_ip_do_servidor" ".env.local" >nul
if not errorlevel 1 (
    echo [ERRO] Voce precisa atualizar o arquivo .env.local com o IP correto do servidor Docker.
    echo [ERRO] Substitua 'endereco_ip_do_servidor' pelo IP real do servidor.
    echo [INFO] Execute: notepad .env.local para editar o arquivo.
    pause
    exit /b 1
)

REM Verifica se o token do Telegram foi removido do .env.local (ou se está usando .env.local para configurações locais)
findstr /C:"7843033735:AAH93o7O0DGb_aSwC33W_lSpkF5IQmqsL8o" ".env.local" >nul
if not errorlevel 1 (
    echo [ERRO] O token do bot está configurado no arquivo .env.local, o que pode ser um risco de segurança.
    echo [INFO] Recomenda-se remover o token do arquivo .env.local e usá-lo apenas como variável de ambiente.
    pause
    exit /b 1
)

echo [OK] Configuracoes verificadas.

echo.
echo Executando o teste de conexao com o banco de dados...
python test_db_connection.py

echo.
set /p run_bot=Deseja executar o bot agora? (s/n): 
if /i "%run_bot%"=="s" (
    echo.
    echo Executando o bot de coleta de codigos de barras...
    echo Pressione CTRL+C para parar o bot.
    echo.
    python ColetasCodBarraMultiplos.py
) else (
    echo.
    echo Voce optou por nao executar o bot agora.
    echo Para executa-lo depois, use o comando: python ColetasCodBarraMultiplos.py
)

echo.
echo ##########################################################
echo #                       FIM                              #
echo ##########################################################
pause

