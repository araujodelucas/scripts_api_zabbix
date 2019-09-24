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

#definindo função para criar o(s) usuario(s)
def create_user(alias,passw,name,surname,user_type,grupoid):
    try:
        create_user = zapi.user.create({
            "alias": alias,
            "passwd": passw,
            "name": name,
            "surname": surname,
            "type": user_type,
            "usrgrps": [
                {
                    "usrgrpid": grupoid
                }
            ]
        })
        print('Usuário {} cadastrado com sucesso'.format(alias))
    except Already_Exists: #se o(s) usuario(s) já estiver cadastrado
        print('Usuário {} já está cadastrado'.format(alias))
    except Exception as err: #se houver algum erro ao cadastrar o(s) usuario(s)
        print('Falha ao cadastrar o usuário: {} - Erro: {}'.format(alias,err))

#abrindo e lendo o arquivo csv
arquivo = csv.reader(open(arq),delimiter=';')

#laço para percorrer os usuarios listados no arquivo csv
for [alias,passw,name,surname,user_type,grupoid] in arquivo:
    create_user(alias,passw,name,surname,user_type,grupoid)

#fechando a conexão com o Zabbix
zapi.logout()