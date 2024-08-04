import os
import sqlite3
# Aluno: Nome do Aluno
# Descrição o resultado: Retorna o limite inferior e superior das 6 classes de renda 
# e o total de famílias de cada classe para a região brasileira desejada.
# A região desejada é informada através de parâmtro.   

# the relative file path
# Caminho relativo da pasta que está o banco de dados
path = '/bd/bases/POF_morador.DB' 

# get the path to the directory this script is in
#perga o caminho da pasta que este script está contido
scriptdir = os.path.dirname(__file__)
print (scriptdir)
# add the relative path to the database file from there
#Acrescenta o caminho onde está o banco de dados
db_path = os.path.join(scriptdir, path)
print (db_path)
# make sure the path exists and if not create it
#os.makedirs(os.path.dirname(db_path), exist_ok=True)

# create the connection
# cria a conexão com o banco de dados, se não exir BD ele cria
con = sqlite3.connect(db_path)
# have queries return a dictionary rather than a tuple (optional)

#con.row_factory = sqlite3.Row  

# create a reference to the database cursur for later use
# cria um cursor para usar com o banco de dados
cur = con.cursor()
#cur.execute(""" SELECT * FROM V_RegiaoRacaBebida """)


#cur.execute(""" SELECT * FROM sqlite_master WHERE type='table' """)

#LISTAS AS TABELAS
#cur.execute(""" SELECT name FROM sqlite_master WHERE type='table' """)

# LISTAS A ESTRUTURA DA TABELA INFORMADA
#nome_tabela= input('Nome da tabela: ')
#cur.execute(""" SELECT * FROM sqlite_master WHERE type='table' AND name =? """,[nome_tabela])

#LISTA AS UF QUE TEM ESCOLAS
#cur.execute(""" SELECT * FROM ESCOLAS""")
#LISTA TOTAL DE ESCOLAS POR UF
#cur.execute(""" SELECT UF,COUNT(1) AS TOTAL FROM T_ESCOLAS GROUP BY UF """)

#LISTA TOTAL DE ESCOLAS DA SILGA DA UF INFORMADA (RJN, SP, MA)
#uf= input('UF: ')
#cur.execute(""" SELECT UF,COUNT(1) AS TOTAL FROM T_ESCOLAS WHERE UF = ?  GROUP BY UF """,[uf])


# LISTA O TOTAL DE MUNICÍPIO QUE NÃO TEM ESCOLAS 
# cur.execute("""
# SELECT  COUNT(*) FROM (
# SELECT NOME_MUNICIPIO FROM T_MUNICIPIO
# EXCEPT
# SELECT DISTINCT MUNICIPIO FROM T_ESCOLAS
# ) """)

# for linha in cur.fetchall():
#       print(linha);

regiao='Norte'
# executa uma  consulta
cur.execute("""
SELECT  
RG.Regiao,F.LIMITE_INFERIOR,F.LIMITE_SUPERIOR,F.CLASSE 
,SUM(PESO_FINAL/TAMANHO_FAMILIA) as  TOTAL_FAMILIAS
FROM Quest_morador A
INNER JOIN Faixa_renda_familiar F 
    ON (RENDA_TOTAL BETWEEN F.LIMITE_INFERIOR 
        AND F.LIMITE_SUPERIOR) 
        OR (RENDA_TOTAL>=F.LIMITE_INFERIOR AND CLASSE='CLASSE 6')
INNER JOIN T_UF ON T_UF.COD_UF=A.UF
INNER JOIN T_REGIAO RG ON RG.cod_regiao=T_UF.cod_regiao
WHERE A.UF IN 
    (SELECT COD_UF FROM T_UF WHERE RENDA_MEDIA_FAMILIAR <
                (SELECT AVG(RENDA_MEDIA_FAMILIAR) FROM T_UF ) )
    and RG.Regiao = ?
GROUP BY RG.Regiao,F.LIMITE_INFERIOR,F.LIMITE_SUPERIOR,F.CLASSE
ORDER BY RG.Regiao,F.LIMITE_INFERIOR,F.LIMITE_SUPERIOR,F.CLASSE
 """,[regiao])


dados = cur.fetchall() 

title = [i[0] for i in cur.description]
print(title) # exibe os rótulos/nome dos atributos
 
for linha in dados:
    print(linha) # exibe cada linha da query 

arquivo=scriptdir+"/arquivo.csv" # especifica o caminho do arquivo de saída
with open(arquivo, "w",encoding="locale") as f: # abre um arquivo de saída para escrita
    f.write(";".join([str(cell) for cell in title]) + "\n") # escreva a saída no arquivo
    for row in dados:
        f.write(";".join([str(cell) for cell in row]) + "\n") # escreva a saída no arquivo
