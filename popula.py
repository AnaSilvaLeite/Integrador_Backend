
import os
import csv
import django

from pathlib import Path
from datetime import datetime
from decimal import Decimal

# Configuração do Django
BASE_DIR = Path(__file__).resolve().parent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import transaction
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

from api.models import (
    Environment,
    EquipmentModel,
    Microcontroller,
    Sensor,
    Reading
)

User = get_user_model()

DATA_DIR = BASE_DIR / "data"


# ==========================================================
# LEITURA DOS ARQUIVOS CSV
# ==========================================================

def ler_csv(nome_arquivo):
    caminho = DATA_DIR / nome_arquivo

    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho}"
        )

    print(f"\nLendo arquivo: {nome_arquivo}")

    with open(
        caminho,
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        # Lê somente a primeira linha para identificar
        # corretamente o separador do arquivo.
        cabecalho = arquivo.readline()
        arquivo.seek(0)

        if not cabecalho.strip():
            raise ValueError(
                f"O arquivo {nome_arquivo} está vazio."
            )

        try:
            delimitador = csv.Sniffer().sniff(
                cabecalho,
                delimiters=",;\t"
            ).delimiter
        except csv.Error:
            delimitador = ","

        print(
            f"Separador identificado: {repr(delimitador)}"
        )

        leitor = csv.DictReader(
            arquivo,
            delimiter=delimitador
        )

        if not leitor.fieldnames:
            raise ValueError(
                f"O arquivo {nome_arquivo} não possui cabeçalho."
            )

        # Padroniza os nomes das colunas.
        leitor.fieldnames = [
            campo.strip().replace("\ufeff", "").lower()
            for campo in leitor.fieldnames
        ]

        print(
            f"Cabeçalhos encontrados: {leitor.fieldnames}"
        )

        dados_csv = []

        for linha in leitor:
            dados = {}

            for chave, valor in linha.items():
                if chave is not None:
                    chave = chave.strip().lower()
                    dados[chave] = (
                        valor.strip() if valor else ""
                    )

            dados_csv.append(dados)

        return dados_csv


# ==========================================================
# VERIFICAÇÃO DAS COLUNAS OBRIGATÓRIAS
# ==========================================================

def verificar_colunas(nome_arquivo, dados, colunas):
    if not dados:
        raise ValueError(
            f"O arquivo {nome_arquivo} não possui registros."
        )

    colunas_encontradas = set(dados[0].keys())

    colunas_faltantes = [
        coluna for coluna in colunas
        if coluna not in colunas_encontradas
    ]

    if colunas_faltantes:
        raise ValueError(
            f"\nErro no arquivo {nome_arquivo}.\n"
            f"Colunas encontradas: {sorted(colunas_encontradas)}\n"
            f"Colunas necessárias: {colunas}\n"
            f"Colunas faltantes: {colunas_faltantes}"
        )


# ==========================================================
# IMPORTAÇÃO DOS USUÁRIOS
# ==========================================================

def importar_usuarios():
    print("\n--- Importando usuários ---")

    usuarios = ler_csv("users.csv")

    verificar_colunas(
        "users.csv",
        usuarios,
        ["username", "name", "email", "type", "password"]
    )

    for dados in usuarios:
        username = dados["username"]

        if User.objects.filter(username=username).exists():
            print(f"Usuário já existente: {username}")
            continue

        usuario = User(
            username=username,
            name=dados["name"],
            email=dados["email"],
            type=dados["type"]
        )

        usuario.set_password(dados["password"])

        if dados["type"] == "SUPERUSER":
            usuario.is_superuser = True
            usuario.is_staff = True

        usuario.save()

        print(f"Usuário criado: {username}")


# ==========================================================
# IMPORTAÇÃO DOS AMBIENTES
# ==========================================================

def importar_ambientes():
    print("\n--- Importando ambientes ---")

    ambientes = ler_csv("environments.csv")

    verificar_colunas(
        "environments.csv",
        ambientes,
        ["point", "name", "description"]
    )

    for dados in ambientes:
        ponto = dados["point"]

        ambiente, criado = Environment.objects.get_or_create(
            point=ponto,
            defaults={
                "name": dados["name"],
                "description": dados["description"]
            }
        )

        if criado:
            print(f"Ambiente criado: {ponto}")
        else:
            print(f"Ambiente já existente: {ponto}")


# ==========================================================
# IMPORTAÇÃO DOS MODELOS DE EQUIPAMENTOS
# ==========================================================

def importar_modelos():
    print("\n--- Importando modelos de equipamentos ---")

    modelos = ler_csv("equipment_models.csv")

    verificar_colunas(
        "equipment_models.csv",
        modelos,
        ["name", "description"]
    )

    for dados in modelos:
        nome = dados["name"]

        modelo, criado = EquipmentModel.objects.get_or_create(
            name=nome,
            defaults={
                "description": dados["description"]
            }
        )

        if criado:
            print(f"Modelo criado: {nome}")
        else:
            print(f"Modelo já existente: {nome}")


# ==========================================================
# IMPORTAÇÃO DOS MICROCONTROLADORES
# ==========================================================

def importar_microcontroladores():
    print("\n--- Importando microcontroladores ---")

    microcontroladores = ler_csv("microcontrollers.csv")

    verificar_colunas(
        "microcontrollers.csv",
        microcontroladores,
        [
            "mac_address",
            "latitude",
            "longitude",
            "observation",
            "status",
            "environment_point",
            "equipment_model_name"
        ]
    )

    for dados in microcontroladores:
        mac = dados["mac_address"]

        ambiente = Environment.objects.get(
            point=dados["environment_point"]
        )

        modelo = EquipmentModel.objects.get(
            name=dados["equipment_model_name"]
        )

        microcontrolador, criado = (
            Microcontroller.objects.get_or_create(
                mac_address=mac,
                defaults={
                    "latitude": Decimal(dados["latitude"]),
                    "longitude": Decimal(dados["longitude"]),
                    "observation": dados["observation"],
                    "status": dados["status"],
                    "environment": ambiente,
                    "equipment_model": modelo
                }
            )
        )

        if criado:
            print(f"Microcontrolador criado: {mac}")
        else:
            print(f"Microcontrolador já existente: {mac}")


# ==========================================================
# IMPORTAÇÃO DOS SENSORES
# ==========================================================

def importar_sensores():
    print("\n--- Importando sensores ---")

    sensores = ler_csv("sensors.csv")

    verificar_colunas(
        "sensors.csv",
        sensores,
        [
            "function",
            "model",
            "unit_measureament",
            "status",
            "microcontroller_mac_address"
        ]
    )

    for dados in sensores:
        microcontrolador = Microcontroller.objects.get(
            mac_address=dados["microcontroller_mac_address"]
        )

        function = dados["function"]
        model = dados["model"]

        sensor, criado = Sensor.objects.get_or_create(
            function=function,
            model=model,
            microcontroller=microcontrolador,
            defaults={
                "unit_measureament": dados["unit_measureament"],
                "status": dados["status"]
            }
        )

        if criado:
            print(
                f"Sensor criado: {function} - "
                f"{microcontrolador.mac_address}"
            )
        else:
            print(
                f"Sensor já existente: {function} - "
                f"{microcontrolador.mac_address}"
            )


# ==========================================================
# IMPORTAÇÃO DAS LEITURAS
# ==========================================================

def importar_leituras():
    print("\n--- Importando leituras ---")

    leituras = ler_csv("readings.csv")

    verificar_colunas(
        "readings.csv",
        leituras,
        [
            "registration_date",
            "sensor_function",
            "microcontroller_mac_address",
            "measured_value"
        ]
    )

    for dados in leituras:
        sensor = Sensor.objects.get(
            function=dados["sensor_function"],
            microcontroller__mac_address=dados[
                "microcontroller_mac_address"
            ]
        )

        data = datetime.strptime(
            dados["registration_date"],
            "%Y-%m-%d %H:%M:%S"
        )

        # Torna a data compatível com USE_TZ=True,
        # caso essa configuração esteja ativada no Django.
        if settings.USE_TZ and timezone.is_naive(data):
            data = timezone.make_aware(data)

        valor = Decimal(dados["measured_value"])

        leitura, criado = Reading.objects.get_or_create(
            sensor=sensor,
            registration_date=data,
            measured_value=valor
        )

        if criado:
            print(
                f"Leitura criada: {sensor.function} - {valor}"
            )
        else:
            print(
                f"Leitura já existente: {sensor.function} - {valor}"
            )


# ==========================================================
# EXECUÇÃO DA IMPORTAÇÃO
# ==========================================================

@transaction.atomic
def popular_banco():

    print("\n====================================")
    print(" INICIANDO IMPORTAÇÃO DOS DADOS")
    print("====================================")

    # A ordem respeita os relacionamentos entre as tabelas.
    importar_usuarios()
    importar_ambientes()
    importar_modelos()
    importar_microcontroladores()
    importar_sensores()
    importar_leituras()

    print("\n====================================")
    print(" IMPORTAÇÃO FINALIZADA COM SUCESSO")
    print("====================================")

    print("\nResumo dos registros:")

    print(f"Usuários: {User.objects.count()}")
    print(f"Ambientes: {Environment.objects.count()}")
    print(f"Modelos: {EquipmentModel.objects.count()}")
    print(f"Microcontroladores: {Microcontroller.objects.count()}")
    print(f"Sensores: {Sensor.objects.count()}")
    print(f"Leituras: {Reading.objects.count()}")


# ==========================================================
# INÍCIO DO PROGRAMA
# ==========================================================

if __name__ == "__main__":

    try:
        popular_banco()

    except Exception as erro:
        print("\nERRO DURANTE A IMPORTAÇÃO:")
        print(erro)
        raise
