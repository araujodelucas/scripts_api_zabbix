#definindo a versão do interpretador Python, nesse caso, 3.7
#!/usr/bin/python3.7

#habilitando a utilização de caracteres especiais
# -*- coding: utf-8 -*-

#importando módulo para consumir o arquivo csv
import csv

#importando módulos da biblioteca da api do zabbix
from zabbix_api import ZabbixAPI, Already_Exists

#tratando os dados de acesso ao Zabbix e arquivo CSV
try:
    url = input('Informe a URL de acesso ao Zabbix: ')
    username = input('Informe o usuário de acesso ao Zabbix: ')
    password = input('Informe a senha de acesso ao Zabbix: ')
    arq = input('Informe o arquivo CSV em seu caminho absoluto: ')

    #criando a conexão com a api do zabbix
    zapi = ZabbixAPI(url, timeout=180)
    zapi.login(username,password)
    print('Conectado na API do Zabbix, versao {}'.format(zapi.api_version()))
except Exception as err:
    print('Falha ao conectar na API do Zabbix')
    print('Erro: {}'.format(err))

#definindo função para criar o(s) host(s) group(s)
def hostgroup_create(name):
    try:
        create_hostgroup = zapi.hostgroup.create({
        "name": name
        })
        print('Grupo {} cadastrado com sucesso'.format(name))
    except Already_Exists: #se o(s) host(s) group(s) já estiver cadastrado
        print('Grupo {} já cadastrado'.format(name))
    except Exception as err: #se houver algum erro ao cadastrar o(s) host(s) group(s)
        print('Falha ao cadastrar o grupo {} - Erro'.format(name, err))

#abrindo e lendo o arquivo csv
arquivo = csv.reader(open(arq))

#laço para percorrer os hosts groups listados no arquivo csv
for [name] in arquivo:
    hostgroup_create(name)

#fechando a conexão com o Zabbix
zapi.logout()