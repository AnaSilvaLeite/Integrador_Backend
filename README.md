Integrador Backend — API de Monitoramento Ambiental
Ana Paula da Silva Leite 2DS-MB

API REST desenvolvida como parte do Projeto Integrador (PWBE) do SENAI Roberto Mange. O sistema permite cadastrar locais de monitoramento, modelos de equipamentos, microcontroladores, sensores, usuários e leituras 
ambientais, além de consultar os dados por filtros e endpoints específicos.

O projeto simula pontos de monitoramento instalados nos corredores próximos aos laboratórios de informática da TecnoVille. Cada microcontrolador pode possuir sensores de temperatura, umidade, luminosidade e contagem 
de passagens. Não é necessária conexão com dispositivos físicos: os dados podem ser importados por arquivos CSV/SQL ou gerados por comando Django.

1. Tecnologias utilizadas
- Python
- Django 5.2.17
- Django REST Framework 3.18.1
- MySQL
- Django REST Framework Simple JWT 5.5.1
- django-filter 26.1
- Pillow 12.3.0 — suporte a imagens dos usuários

2. Funcionalidades
Cadastros e monitoramento
- CRUD de locais (Environment).
- CRUD de modelos de equipamentos (EquipmentModel).
- CRUD de microcontroladores (Microcontroller), com endereço MAC, coordenadas, observação, modelo, local e status.
- CRUD de sensores (Sensor), associados a um microcontrolador.
- Registro e consulta de leituras (Reading), com sensor, valor medido e data/hora.
- Cadastro e consulta de usuários, com nome, e-mail, perfil e foto.
- Filtros de sensores e microcontroladores por status.
- Filtros de leituras por sensor, data, intervalo, local, status do sensor e função.
- Bloqueio de novas leituras quando o sensor ou seu microcontrolador estiver inativo.
- Validação da correspondência entre a função do sensor e sua unidade de medida.
- Proteção de registros relacionados com on_delete=PROTECT, evitando que a exclusão de um registro pai apague o histórico associado.

Autenticação e autorização:
- A API utiliza JWT. O token de acesso tem validade de 25 minutos e o refresh token tem validade de 12 horas.
- Perfil	Permissão implementada
- Superusuário	Pode consultar e gerenciar os recursos permitidos pelas regras de cada endpoint.
- Administrador	Pode consultar e gerenciar locais, modelos, microcontroladores, sensores e leituras.
- Usuário	Pode consultar os recursos protegidos; não pode criar, editar ou excluir esses registros.

O endpoint de usuários possui uma regra mais restrita: operações de escrita são permitidas somente ao superusuário. A foto é recebida pelo campo photo.

3. Estrutura do projeto
Integrador_Backend-main/
├── api/
│   ├── management/commands/gerar_leituras.py
│   ├── migrations/
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── data/
│   ├── csv/
│   ├── prompts/csv/
│   ├── prompts/sql/
│   └── sql/
├── media/users/
├── manage.py
├── popula.py
├── .gitignore
└── requirements.txt

Principais entidades
- User: usuário baseado em AbstractUser, com nome, e-mail, tipo de acesso e foto.
- Environment: ponto/local de monitoramento.
- EquipmentModel: modelo do equipamento utilizado pelo microcontrolador.
- Microcontroller: dispositivo instalado em um local, com MAC, latitude, longitude, observação e status.
- Sensor: sensor vinculado a um microcontrolador, com função, modelo, unidade de medida e status.
- Reading: medição vinculada a um sensor, com valor e data/hora.

4. Pré-requisitos
Antes de iniciar, instale:
- Python (recomenda-se Python 3.12 ou 3.13).
- MySQL Server e um cliente, como MySQL Workbench.
- Git (opcional, caso clone o repositório).
- Instalação e configuração local
Os comandos abaixo consideram Windows com PowerShell e devem ser executados no diretório que contém manage.py.

5.1. Obter o projeto
git clone https://github.com/AnaSilvaLeite/Integrador_Backend.git
cd Integrador_Backend

5.2. Criar e ativar o ambiente virtual
python -m venv env
.\env\Scripts\Activate.ps1
Se o PowerShell bloquear a ativação do ambiente, execute nesta janela:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\env\Scripts\Activate.ps1

5.3. Preparar o arquivo de dependências
Instale as dependências:
python -m pip install --upgrade pip
pip install -r requirements.txt

5.4. Criar o banco MySQL
No MySQL Workbench ou no cliente MySQL, execute:
CREATE DATABASE integrador
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
  
O arquivo config/settings.py está configurado para conectar ao banco com estes parâmetros:
Parâmetro	Configuração atual
ENGINE	django.db.backends.mysql
NAME	integrador
USER	root
PASSWORD	root
HOST	localhost
PORT	3306

Se suas credenciais MySQL forem diferentes, altere DATABASES em config/settings.py antes de executar as migrações.

5.5. Aplicar as migrações
python manage.py makemigrations
python manage.py migrate

6. População do banco de dados
O projeto disponibiliza dados de exemplo em data/csv/, scripts SQL em data/sql/ e os prompts usados para gerar esses arquivos em data/prompts/.

6.1. Importação por CSV com popula.py
O script importa os registros na ordem necessária para respeitar as chaves estrangeiras: usuários, ambientes, modelos de equipamentos, microcontroladores, sensores e leituras. 
Ele utiliza get_or_create para evitar duplicar os registros que já existem.

Arquivos CSV incluídos:
data/csv/users.csv	Usuários de exemplo
data/csv/environments.csv	Locais de monitoramento
data/csv/equipment_models.csv	Modelos de equipamentos
data/csv/microcontrollers.csv	Microcontroladores
data/csv/sensors.csv	Sensores
data/csv/readings.csv	Leituras simuladas


6.2. População alternativa por SQL
Existem scripts SQL numerados em data/sql/. Caso opte por executar a população por SQL, utilize a ordem abaixo, após executar as migrações do Django:
- 01_users.sql
- 02_environments.sql
- 03_equipment_models.sql
- 04_microcontrollers.sql
- 05_sensors.sql
- 06_readings.sql
   
7. Executar a API
Com o ambiente virtual ativado e o banco configurado:
python manage.py runserver
A API ficará disponível localmente em:
http://127.0.0.1:8000/api/
O painel administrativo do Django fica em:
http://127.0.0.1:8000/admin/
As imagens de usuários são armazenadas em media/users/ e servidas localmente quando DEBUG=True.

8. Endpoints da API
Todas as rotas abaixo usam o prefixo http://127.0.0.1:8000/api/.
Autenticação
Método	Endpoint	Descrição
POST	/login/	Autentica o usuário e retorna access e refresh.
POST	/refresh/	Gera um novo access token a partir do refresh token.

Para acessar endpoints protegidos, envie o access token no cabeçalho:
Authorization: Bearer SEU_ACCESS_TOKEN
Recursos CRUD
Recurso	Endpoint	Métodos registrados
Locais	/environments/	GET, POST, PUT, PATCH, DELETE
Modelos de equipamentos	/equipment-models/	GET, POST, PUT, PATCH, DELETE
Microcontroladores	/microcontrollers/	GET, POST, PUT, PATCH, DELETE
Sensores	/sensors/	GET, POST, PUT, PATCH, DELETE
Leituras	/readings/	GET, POST
Usuários	/users/	GET, POST, PUT, PATCH, DELETE (escrita restrita ao superusuário)


Para consultar um registro específico, acrescente seu ID à rota, por exemplo: GET /sensors/1/.

Observação sobre leituras: o ReadingViewSet limita os métodos HTTP a GET, POST, HEAD e OPTIONS. Portanto, não disponibiliza edição ou exclusão de leituras pela API.
Filtros de microcontroladores e sensores
Endpoint	Parâmetro	Exemplo
/microcontrollers/	status	?status=ACTIVE
/sensors/	status	?status=INACTIVE

Valores de status aceitos: ACTIVE e INACTIVE.
Filtros de leituras
Parâmetro	Descrição	Exemplo
sensor	ID do sensor	?sensor=1
data	Uma data específica	?data=2026-10-01
data_inicio	Data inicial do período	?data_inicio=2026-10-01
data_fim	Data final do período	?data_fim=2026-10-31
local	ID do local/ambiente	?local=1
status	Status do sensor	?status=ACTIVE
function	Função do sensor	?function=temperature

É possível combinar parâmetros, por exemplo:
GET /api/readings/?sensor=1&data_inicio=2026-10-01&data_fim=2026-10-31
As datas dos filtros devem ser informadas no formato YYYY-MM-DD.
Endpoints adicionais de leituras
Método	Endpoint	Descrição
GET	/readings/last-24-hours/	Retorna as leituras das últimas 24 horas.
GET	/readings/latest-by-sensor/	Retorna a leitura mais recente de cada sensor.
GET	/readings/statistics/?sensor=ID	Retorna quantidade, mínimo, máximo e média das leituras de um sensor.

O endpoint de estatísticas aceita também start_date e end_date:
GET /api/readings/statistics/?sensor=1&start_date=2026-10-01&end_date=2026-10-31

9. Funcionalidades extras implementadas
O código analisado contém as seguintes funcionalidades extras do enunciado:
- Ordenação de leituras: ordena por data/hora ou valor medido usando ?ordering=registration_date, ?ordering=-registration_date ou ?ordering=measured_value.
- Resumo estatístico por sensor: endpoint /api/readings/statistics/, com total, valor mínimo, máximo e média, podendo limitar o período.
- Prevenção de leituras duplicadas: o serializer impede duplicidade considerando sensor, data/hora e valor medido.
- Geração de leituras simuladas: comando personalizado gerar_leituras, que cria medições para sensores ativos ligados a microcontroladores ativos.
- Consulta rápida de leituras: endpoints para consultar as últimas 24 horas e a leitura mais recente de cada sensor.

10. AlwaysData:
https://analeite.alwaysdata.net/api/

Projeto: Integrador Backend — API de Monitoramento Ambiental
Instituição: SENAI Roberto Mange
Repositório: github.com/AnaSilvaLeite/Integrador_Backend
