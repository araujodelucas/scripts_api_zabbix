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

#definindo função para criar o(s) host(s)
def host_create(name_,ip_,mib,group_id,template_id):
    try:
        create_host = zapi.host.create({
            "host": name_,
            "interfaces": [
                {
                    "type": 2,
                    "main": 1,
                    "useip": 1,
                    "ip": ip_,
                    "dns": "",
                    "port": "161",
                    "bulk": 1
                }
            ],
            "groups": [
                {
                    "groupid": group_id
                }
            ],
            "templates": [
                {
                    "templateid": template_id
                }
            ],
            "inventory_mode": 1,
            "macros": [
                {
                    "macro": "{$SNMP_COMMUNITY}",
                    "value": mib
                }
            ]
        })

        print('Host {} cadastrado com sucesso'.format(name_))
    except Already_Exists: #se o objeto já estiver cadastrado
        print('Host {} já cadastrado'.format(name_))
    except Exception as err:
        print('Falha ao cadastrar o host {} - Erro'.format(name_, err))

#abrindo e lendo o arquivo csv
arquivo = csv.reader(open(arq),delimiter=';')

#laço para percorrer os hosts listados no arquivo csv
for [name_,ip_,mib,group_id,template_id] in arquivo:
    host_create(name_,ip_,mib,group_id,template_id)

#fechando a conexão com o Zabbix
zapi.logout()
