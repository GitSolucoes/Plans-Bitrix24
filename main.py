from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import time

app = Flask(__name__)

load_dotenv()

BITRIX_WEBHOOK_URL = os.getenv('BITRIX_WEBHOOK_URL')
URL_VPS = os.getenv('URL_VPS')
 
BITRIX_WEBHOOK_URL = f"{BITRIX_WEBHOOK_URL}"




def log_erro(mensagem, e=None):
    """ Função de log de erro para registrar exceções """
    import traceback
    erro_detalhado = traceback.format_exc()
    print(f"\n[ERRO] {mensagem}")
    if e:
        print(f"[DETALHES] {str(e)}")
    print(f"[TRACEBACK] {erro_detalhado}\n")

# CIDADES DA OPERADORA VERO - INTERNET 
CITIES_API_OURO = [
    "TRÊS LAGOAS - MS",
    "RIO VERDE - GO",
    "GOIANIRA - GO",
    "BARÃO DE COCAIS - MG",
    "BARBACENA - MG",
    "BARROSO - MG",
    "CAXAMBU - MG",
    "DIVINÓPOLIS - MG",
    "GOVERNADOR VALADARES - MG",
    "LAVRAS - MG",
    "MARIANA - MG",
    "PONTE NOVA - MG",
    "SABARÁ - MG",
    "SÃO LOURENÇO - MG",
    "VIÇOSA - MG",
    "UBERLÂNDIA - MG",
    "SÃO JOÃO DEL REI - MG",
    "CRISTIANO OTONI - MG",
    "BAURU - SP",
    "ARACATUBA - SP",
    "BIRIGUI - SP",
    "PEDERNEIRAS - SP",
    "ANDRADINA - SP",
    "ALVORADA - RS",
    "CACHOEIRINHA - RS",
    "CAPÃO DA CANOA - RS",
    "CHARQUEADAS - RS",
    "ESTEIO - RS",
    "FRANCISCO BELTRÃO - PR",
    "FREDERICO WESTPHALEN - RS",
    "GRAVATAÍ - RS",
    "ITAQUI - RS",
    "NOVO HAMBURGO - RS",
    "NOVO HAMBURGO - SINOS - RS",
    "PATO BRANCO - PR",
    "SANTIAGO - RS",
    "SÃO JERÔNIMO - RS",
    "SÃO LEOPOLDO - RS",
    "SÃO LEOPOLDO - SINOS - RS",
    "SÃO LUIZ GONZAGA - RS",
    "SAPUCAIA DO SUL - RS",
    "URUGUAIANA - RS",
    "VENÂNCIO AIRES - RS",
    "XANXERÊ - SC",
    "ITAPEMA - SC",
    "TIJUCAS - SC"
]

CITIES_API_PADRAO = [
    "GOIÂNIA - GO",
    "APARECIDA DE GOIÂNIA - GO",
    "SENADOR CANEDO - GO",
    "ALFREDO VASCONCELOS - MG",
    "ANTÔNIO CARLOS - MG",
    "BELO HORIZONTE - MG",
    "BICAS - MG",
    "BOM DESPACHO - MG",
    "BOM SUCESSO - MG",
    "CARANDAÍ - MG",
    "CARMO DA MATA - MG",
    "CARMÓPOLIS DE MINAS - MG",
    "CLÁUDIO - MG",
    "CONCEIÇÃO DA BARRA DE MINAS - MG",
    "CONGONHAS - MG",
    "CONSELHEIRO LAFAIETE - MG",
    "DORES DE CAMPOS - MG",
    "ENTRE RIOS DE MINAS - MG",
    "GUARARÁ - MG",
    "ITAGUARA - MG",
    "ITATIAIUÇU - MG",
    "ITAÚNA - MG",
    "JECEABA - MG",
    "JUIZ DE FORA - MG",
    "LIMA DUARTE - MG",
    "MAR DE ESPANHA - MG",
    "MARTINHO CAMPOS - MG",
    "MATIAS BARBOSA - MG",
    "NOVA SERRANA - MG",
    "OLIVEIRA - MG",
    "OURO BRANCO - MG",
    "PARÁ DE MINAS - MG",
    "PERDÕES - MG",
    "RESSAQUINHA - MG",
    "RIBEIRÃO DAS NEVES - MG",
    "RIBEIRÃO VERMELHO - MG",
    "SANTA CRUZ DE MINAS - MG",
    "SANTA LUZIA - MG",
    "SANTO ANTÔNIO DO AMPARO - MG",
    "SÃO BRÁS DO SUAÇUÍ - MG",
    "SÃO FRANCISCO DE PAULA - MG",
    "TEÓFILO OTONI - MG",
    "TIRADENTES - MG",
    "ANCHIETA - SC",
    "ARROIO DO SAL - RS",
    "BALNEÁRIO PINHAL - RS",
    "BANDEIRANTE - SC",
    "BARRACÃO - PR",
    "CAMPO ERÊ - SC",
    "CAPELA DE SANTANA - RS",
    "CARAÁ - RS",
    "CIDREIRA - RS",
    "CRUZ ALTA - RS",
    "DESCANSO - SC",
    "DIONÍSIO CERQUEIRA - SC",
    "FLOR DA SERRA DO SUL - PR",
    "GALVÃO - SC",
    "GLORINHA - RS",
    "GUARACIABA - SC",
    "GUARUJÁ DO SUL - SC",
    "IJUÍ - RS",
    "IMBÉ - RS",
    "JUPIÁ - SC",
    "MAQUINÉ - RS",
    "MARATÁ - RS",
    "MARIÓPOLIS - PR",
    "MARMELEIRO - PR",
    "MONTENEGRO - RS",
    "NOVA SANTA RITA - RS",
    "NOVO HORIZONTE - SC",
    "OSÓRIO - RS",
    "PALMA SOLA - SC",
    "PANAMBI - RS",
    "PARECI NOVO - RS",
    "PORTO ALEGRE - RS",
    "PRINCESA - SC",
    "RENASCENÇA - PR",
    "SANTO ÂNGELO - RS",
    "SANTO ANTÔNIO DA PATRULHA - RS",
    "SÃO DOMINGOS - SC",
    "SÃO JOSÉ DO CEDRO - SC",
    "SÃO JOSÉ DO SUL - RS",
    "SÃO LOURENÇO DO OESTE - SC",
    "SÃO MIGUEL DO OESTE - SC",
    "TERRA DE AREIA - RS",
    "TORRES - RS",
    "TRAMANDAÍ - RS",
    "TRÊS CACHOEIRAS - RS",
    "TRIUNFO - RS",
    "VIAMÃO - RS",
    "VITORINO - PR",
    "XANGRI-LÁ - RS"
]

CITIES_API_PRATA = [
    "BRASÍLIA - DF",
    "LUZIÂNIA - GO",
    "NOVO GAMA - GO",
    "VALPARAÍSO DE GOIÁS - GO",
    "CAMPO GRANDE - MS",
    "CALDAS NOVAS - GO",
    "CATALÃO - GO",
    "INHUMAS - GO",
    "NOVA ANDRADINA - MS",
    "PORANGATU - GO",
    "PALMEIRAS DE GOIÁS - GO",
    "ACREÚNA - GO",
    "GOIATUBA - GO",
    "GUAPÓ - GO",
    "BATAGUASSU - MS",
    "IPAMERI - GO",
    "BATAYPORÃ - MS",
    "PONTALINA - GO",
    "SÃO LUÍS DE MONTES BELOS - GO",
    "MARA ROSA - GO",
    "SANTA HELENA DE GOIÁS - GO",
    "EDÉIA - GO",
    "NOVA IGUAÇU DE GOIÁS - GO",
    "ANAURILÂNDIA - MS",
    "BELA VISTA DE GOIÁS - GO",
    "FÁTIMA DO SUL - MS",
    "HIDROLÂNDIA - GO",
    "PARAÚNA - GO",
    "INDIARA - GO",
    "ALTO HORIZONTE - GO",
    "PIRACANJUBA - GO",
    "ABADIA DE GOIÁS - GO",
    "BURITI ALEGRE - GO",
    "FIRMINÓPOLIS - GO",
    "PETROLINA DE GOIÁS - GO",
    "AMARALINA - GO",
    "VICENTINA - MS",
    "CROMÍNIA - GO",
    "ITAÚÇU - GO",
    "SANTA TEREZA DE GOIÁS - GO",
    "SÃO JOÃO DA PARAÚNA - GO",
    "CACHOEIRA ALTA - GO",
    "CEZARINA - GO",
    "JANDAIA - GO",
    "RIO QUENTE - GO",
    "TURVELÂNDIA - GO",
    "EDEALINA - GO",
    "MARZAGÃO - GO",
    "URUAÇU - GO",
    "CAMPINORTE - GO",
    "DOURADOS - MS",
    "BOA ESPERANÇA - MG",
    "BRUMADINHO - MG",
    "CAETÉ - MG",
    "CAMPO BELO - MG",
    "CARATINGA - MG",
    "CORONEL FABRICIANO - MG",
    "IGARAPÉ - MG",
    "IPATINGA - MG",
    "ITABIRITO - MG",
    "JOÃO MONLEVADE - MG",
    "LEOPOLDINA - MG",
    "MANHUAÇU - MG",
    "MATOZINHOS - MG",
    "NEPOMUCENO - MG",
    "OURO PRETO - MG",
    "PEDRO LEOPOLDO - MG",
    "PEQUERI - MG",
    "SANTA BÁRBARA - MG",
    "SANTANA DO PARAÍSO - MG",
    "SANTOS DUMONT - MG",
    "SÃO JOAQUIM DE BICAS - MG",
    "SÃO JOSÉ DA LAPA - MG",
    "TIMÓTEO - MG",
    "VESPASIANO - MG",
    "VISCONDE DO RIO BRANCO - MG",
    "LIMEIRA - SP",
    "POA - SP",
    "PRESIDENTE PRUDENTE - SP",
    "SÃO JOSÉ DO RIO PRETO - SP",
    "PIRASSUNUNGA - SP",
    "ITAQUAQUECETUBA - SP",
    "SANTA BÁRBARA D'OESTE - SP",
    "LEME - SP",
    "MAIRINQUE - SP",
    "VOTORANTIM - SP",
    "RIBEIRÃO PIRES - SP",
    "PINDAMONHANGABA - SP",
    "SÃO ROQUE - SP",
    "SÃO JOSÉ DOS CAMPOS - SP",
    "PIRACICABA - SP",
    "TATUI - SP",
    "LINS - SP",
    "PRESIDENTE EPITÁCIO - SP",
    "BOTUCATU - SP",
        "SOROCABA - SP",
    "ITU - SP",
    "CRUZEIRO - SP",
    "PEREIRA BARRETO - SP",
    "ARUJÁ - SP",
    "BARRA BONITA - SP",
    "MARTINÓPOLIS - SP",
    "FERNANDÓPOLIS - SP",
    "IGARACU DO TIETÊ - SP",
    "AMERICANA - SP",
    "SANTO ANASTÁCIO - SP",
    "LORENA - SP",
    "ILHA SOLTEIRA - SP",
    "CASTILHO - SP",
    "PRESIDENTE VENCESLAU - SP",
    "SANTA ISABEL - SP",
    "VALPARAÍSO - SP",
    "FRANCO DA ROCHA - SP",
    "APARECIDA - SP",
    "CORDEIROPOLIS - SP",
    "JALES - SP",
    "MIRANDÓPOLIS - SP",
    "PRESIDENTE BERNARDES - SP",
    "SANTA FÉ DO SUL - SP",
    "GUARARAPES - SP",
    "IRACEMAPOLIS - SP",
    "PROMISSÃO - SP",
    "CACAPAVA - SP",
    "ITAPURA - SP",
    "PIEDADE - SP",
    "CACHOEIRA PAULISTA - SP",
    "CAIEIRAS - SP",
    "SÃO JOÃO DA BOA VISTA - SP",
    "POTIM - SP",
    "AGUDOS - SP",
    "CAJAMAR - SP",
    "MACATUBA - SP",
    "IACANGA - SP",
    "SANTA CRUZ DA CONCEIÇÃO - SP",
    "SÃO PAULO - SP",
    "TORRINHA - SP",
    "RUBINEIA - SP",
    "TRÊS FRONTEIRAS - SP",
    "IPERÓ - SP",
    "NOVA INDEPENDÊNCIA - SP",
    "PIRATININGA - SP",
    "ITAPEVI - SP",
    "RIO GRANDE DA SERRA - SP",
    "SANTA MARIA DA SERRA - SP",
    "URÂNIA - SP",
    "GUAICARA - SP",
    "GUARACAI - SP",
    "JARINU - SP",
    "BROTAS - SP",
    "MURUTINGA DO SUL - SP",
    "CARAPICUÍBA - SP",
    "PIQUEROBI - SP",
    "ALFREDO MARCONDES - SP",
    "AVANHANDAVA - SP",
    "CANAS - SP",
    "PORTO FERREIRA - SP",
    "RIBEIRÃO DOS ÍNDIOS - SP",
    "CAIÚA - SP",
    "EMILIANÓPOLIS - SP",
    "IBIÚNA - SP",
    "PIRAJUÍ - SP",
    "RUBIACEA - SP",
    "SANTANA DA PONTE PENSA - SP",
    "FRANCISCO MORATO - SP",
    "LAVÍNIA - SP",
    "LAVRINHAS - SP",
    "PIRAPORA DO BOM JESUS - SP",
    "SANTA SALETE - SP",
    "TANABI - SP",
    "VARGEM GRANDE PAULISTA - SP",
    "BARUERI - SP",
    "FERRAZ DE VASCONCELOS - SP",
    "JUNDIAÍ - SP",
    "NOVA ODESSA - SP",
    "SANTO EXPEDITO - SP",
    "BENTO DE ABREU - SP",
    "SANTANA DE PARNAÍBA - SP",
    "ARARAS - SP",
    "COTIA - SP",
    "SUZANO - SP",
    "OSASCO - SP",
    "JANDIRA - SP",
    "BOM PRINCÍPIO - RS",
    "CANOAS - RS",
    "DOIS IRMÃOS - RS",
    "ESTÂNCIA VELHA - RS",
    "FELIZ - RS",
    "IVOTI - RS",
    "LINDOLFO COLLOR - RS",
    "MORRO REUTER - RS",
    "PICADA CAFÉ - RS",
    "PORTÃO - RS",
    "PORTÃO - SINOS - RS",
    "PRESIDENTE LUCENA - RS",
    "SANTA MARIA DO HERVAL - RS",
    "SANTO AUGUSTO - RS",
        "SÃO BORJA - RS",
    "SÃO JOSÉ DO HORTÊNCIO - RS",
    "SÃO SEBASTIÃO DO CAÍ - RS",
    "SÃO SEBASTIÃO DO CAÍ - SINOS - RS",
    "SAPIRANGA - RS",
    "ÁGUAS MORNAS - SC",
    "ANGELINA - SC",
    "CANELINHA - SC",
    "NOVA TRENTO - SC",
    "PORTO BELO - SC",
    "ANTÔNIO CARLOS - SC",
    "RANCHO QUEIMADO - SC",
    "SÃO JOÃO BATISTA - SC",
    "BIGUAÇU - SC",
    "FLORIANÓPOLIS - SC",
    "GOVERNADOR CELSO RAMOS - SC",
    "MAJOR GERCINO - SC",
    "PALHOÇA - SC",
    "SANTO AMARO DA IMPERATRIZ - SC",
    "SÃO JOSÉ - SC",
    "SÃO PEDRO DE ALCÂNTARA - SC"
]

CITIES_API_REDE_NEUTRA = [
    "APARECIDA DE GOIÂNIA - GO",
"BELO HORIZONTE - MG",
"CONTAGEM - MG",
"GOIÂNIA - GO",
"SENADOR CANEDO - GO",
"SETE LAGOAS - MG",
"TRINDADE - GO",
"UBÁ - MG",
"RIBEIRÃO DAS NEVES - MG",
"BETIM - MG"
]

CITIES_API_SAFIRA = [
    "VALPARAÍSO DE GOIÁS - GO",
    "TRÊS LAGOAS - MS",
    "BARBACENA - MG",
    "DIVINÓPOLIS - MG",
    "IPATINGA - MG",
    "MANHUAÇU - MG",
    "JUIZ DE FORA - MG",
    "SABARÁ - MG",
    "UBERLÂNDIA - MG",
    "BAURU - SP",
    "LIMEIRA - SP",
    "PRESIDENTE PRUDENTE - SP",
    "ITAQUAQUECETUBA - SP",
    "SANTA BÁRBARA D'OESTE - SP",
    "SÃO JOSÉ DOS CAMPOS - SP",
    "PEDERNEIRAS - SP",
    "CORDEIROPOLIS - SP",
    "IRACEMAPOLIS - SP",
    "AGUDOS - SP",
    "SÃO PAULO - SP",
    "IPERÓ - SP",
    "PIRATININGA - SP",
    "RIO GRANDE DA SERRA - SP",
    "IBIÚNA - SP",
    "BARUERI - SP",
    "FERRAZ DE VASCONCELOS - SP",
    "JUNDIAÍ - SP",
    "COTIA - SP",
    "SUZANO - SP",
    "OSASCO - SP",
    "MAQUINÉ - RS",
    "TRAMANDAÍ - RS"
]

CITYES_API_GRAFENO_75 = [
    "TRÊS LAGOAS - MS",
    "CALDAS NOVAS - GO",
    "INHUMAS - GO",
    "GOIATUBA - GO",
    "SANTA HELENA DE GOIÁS - GO",
    "CORONEL FABRICIANO - MG",
    "IPATINGA - MG",
    "LIMA DUARTE - MG",
    "MATIAS BARBOSA - MG",
    "PARÁ DE MINAS - MG",
    "TIMÓTEO - MG",
    "LIMEIRA - SP",
    "PRESIDENTE PRUDENTE - SP",
    "BIRIGUI - SP",
    "PIRASSUNUNGA - SP",
    "LEME - SP",
    "VOTORANTIM - SP",
    "SÃO JOSÉ DOS CAMPOS - SP",
    "TATUI - SP",
    "ANDRADINA - SP",
    "SOROCABA - SP",
    "AMERICANA - SP",
    "GUARARAPES - SP",
    "PIEDADE - SP",
    "AGUDOS - SP",
    "ARROIO DO SAL - RS",
    "DOIS IRMÃOS - RS",
    "FRANCISCO BELTRÃO - PR",
    "IMBÉ - RS",
    "SÃO JOSÉ DO CEDRO - SC",
    "SÃO MIGUEL DO OESTE - SC",
    "TRAMANDAÍ - RS",
    "GOVERNADOR CELSO RAMOS - SC"
]

CITYES_API_GRAFENO_80 = [
    "BARBACENA - MG",
    "CARATINGA - MG",
    "DIVINÓPOLIS - MG",
    "CONSELHEIRO LAFAIETE - MG",
    "GOVERNADOR VALADARES - MG",
    "SANTANA DO PARAÍSO - MG",
    "TEÓFILO OTONI - MG",
    "BAURU - SP",
    "ARACATUBA - SP",
    "POA - SP",
    "SÃO JOSÉ DO RIO PRETO - SP",
    "ITAQUAQUECETUBA - SP",
    "MAIRINQUE - SP",
    "RIBEIRÃO PIRES - SP",
    "PINDAMONHANGABA - SP",
    "SÃO ROQUE - SP",
    "PEDERNEIRAS - SP",
    "PIRACICABA - SP",
    "LINS - SP",
    "PRESIDENTE EPITÁCIO - SP",
    "BOTUCATU - SP",
    "ITU - SP",
    "CRUZEIRO - SP",
    "PEREIRA BARRETO - SP",
    "ARUJÁ - SP",
    "BARRA BONITA - SP",
    "MARTINÓPOLIS - SP",
    "FERNANDÓPOLIS - SP",
    "IGARACU DO TIETÊ - SP",
    "SANTO ANASTÁCIO - SP",
    "LORENA - SP",
    "ILHA SOLTEIRA - SP",
    "CASTILHO - SP",
    "PRESIDENTE VENCESLAU - SP",
    "SANTA ISABEL - SP",
    "VALPARAÍSO - SP",
    "FRANCO DA ROCHA - SP",
    "APARECIDA - SP",
    "CORDEIROPOLIS - SP",
    "JALES - SP",
    "MIRANDÓPOLIS - SP",
    "PRESIDENTE BERNARDES - SP",
    "SANTA FÉ DO SUL - SP",
    "IRACEMAPOLIS - SP",
    "PROMISSÃO - SP",
    "CACAPAVA - SP",
    "ITAPURA - SP",
    "CACHOEIRA PAULISTA - SP",
    "CAIEIRAS - SP",
    "SÃO JOÃO DA BOA VISTA - SP",
    "POTIM - SP",
    "CAJAMAR - SP",
    "MACATUBA - SP",
    "IACANGA - SP",
    "SANTA CRUZ DA CONCEIÇÃO - SP",
    "TORRINHA - SP",
    "RUBINEIA - SP",
    "TRÊS FRONTEIRAS - SP",
    "NOVA INDEPENDÊNCIA - SP",
    "PIRATININGA - SP",
    "ITAPEVI - SP",
    "SANTA MARIA DA SERRA - SP",
    "URÂNIA - SP",
    "GUAICARA - SP",
    "GUARACAI - SP",
    "JARINU - SP",
    "BROTAS - SP",
    "MURUTINGA DO SUL - SP",
    "CARAPICUÍBA - SP",
    "PIQUEROBI - SP",
    "ALFREDO MARCONDES - SP",
    "AVANHANDAVA - SP",
    "CANAS - SP",
    "PORTO FERREIRA - SP",
    "RIBEIRÃO DOS ÍNDIOS - SP",
    "CAIÚA - SP",
    "EMILIANÓPOLIS - SP",
    "PIRAJUÍ - SP",
    "RUBIACEA - SP",
    "SANTANA DA PONTE PENSA - SP",
    "FRANCISCO MORATO - SP",
    "LAVÍNIA - SP",
    "LAVRINHAS - SP",
    "PIRAPORA DO BOM JESUS - SP",
    "SANTA SALETE - SP",
    "TANABI - SP",
    "VARGEM GRANDE PAULISTA - SP",
    "NOVA ODESSA - SP",
    "SANTO EXPEDITO - SP",
    "BENTO DE ABREU - SP",
    "SANTANA DE PARNAÍBA - SP",
    "ARARAS - SP",
    "JANDIRA - SP"
]


# CIDADES DA OPERADORA GIGA+ - INTERNET

CITIES_API_TERRITORIO_T1_a_T9 = [
    "APUCARANA - PR", "ARAPONGAS - PR", "ARARUNA - PR", "CAMPO MOURÃO - PR", "CIANORTE - PR", "DOUTOR CAMARGO - PR", "ENGENHEIRO BELTRÃO - PR", "JANDAIA DO SUL - PR", "JUSSARA - PR", "MANDAGUARI - PR", "MARIALVA - PR", "MARINGÁ - PR", "PAIÇANDU - PR", "PEABIRU - PR", "ROLÂNDIA - PR", "TELÊMACO BORBA - PR", "UBIRATÃ - PR", 
    "CAMPO GRANDE - MS", "DOURADOS - MS",
    "DIADEMA - SP", "FERRAZ DE VASCONCELOS - SP", "GUARULHOS - SP", "ITAQUAQUECETUBA - SP", "MAUÁ - SP", "MOGI DAS CRUZES - SP", "POÁ - SP", "RIBEIRÃO PIRES - SP", "RIO GRANDE DA SERRA - SP", "SANTO ANDRÉ - SP", "SÃO BERNARDO DO CAMPO - SP", "SÃO PAULO - SP", "SUZANO - SP",
    "BERTIOGA - SP", "CAÇAPAVA - SP", "CARAGUATATUBA - SP", "CUBATÃO - SP", "GUARUJÁ - SP", "ILHABELA - SP", "ITANHAÉM - SP", "JACAREÍ - SP", "MONGAGUÁ - SP", "PERUÍBE - SP", "PRAIA GRANDE - SP", "SANTOS - SP", "SÃO JOSÉ DOS CAMPOS - SP", "SÃO SEBASTIÃO - SP", "SÃO VICENTE - SP", "SAO VICENTE - SP", "TAUBATÉ - SP", "TREMEMBÉ - SP", "UBATUBA - SP",
    "ARARUAMA - RJ", "ARMAÇÃO DOS BÚZIOS - RJ", "ARRAIAL DO CABO - RJ", "CABO FRIO - RJ", "CASIMIRO DE ABREU - RJ", "IGUABA GRANDE - RJ", "MACAÉ - RJ", "RIO DAS OSTRAS - RJ", "SÃO PEDRO DA ALDEIA - RJ", "SAQUAREMA - RJ",
    "ALÉM PARAÍBA - RJ", "BARRA DO PIRAÍ - RJ", "BARRA MANSA - RJ", "BOM JARDIM - RJ", "CACHOEIRAS DE MACACU - RJ", "CARMO - RJ", "COMENDADOR LEVY GASPARIAN - RJ", "GUAPIMIRIM - RJ", "ITAIPAVA - RJ", "ITATIAIA - RJ", "MAGÉ - RJ", "MIGUEL PEREIRA - RJ", "NOVA FRIBURGO - RJ", "PARAÍBA DO SUL - RJ", "PATY DO ALFERES - RJ", "PETRÓPOLIS - RJ", "PINHEIRAL - RJ", "PORTO REAL - RJ", "RESENDE - RJ", "SAPUCAIA - RJ", "SILVA JARDIM - RJ", "SUMIDOURO - RJ", "TERESÓPOLIS - RJ", "TRÊS RIOS - RJ", "VALENÇA - RJ", "VASSOURAS - RJ", "VOLTA REDONDA - RJ",
    "ANCHIETA - ES", "APERIBÉ - ES", "CACHOEIRO DE ITAPEMIRIM - ES", "CAMBUCI - ES", "CAMPOS DOS GOYTACAZES - ES", "CAMPOS DOS GOYTACAZES - RJ", "CANTAGALO - ES", "CARIACICA - ES", "CATAGUASES - ES", "CORDEIRO - ES", "DUAS BARRAS - ES", "GUARAPARI - ES", "ITAOCARA - ES", "ITAPEMIRIM - ES", "ITAPERUNA - ES", "LAJE DO MURIAÉ - ES", "MACUCO - ES", "MARATAÍZES - ES", "MIRACEMA - ES", "MURIAÉ - ES", "PIÚMA - ES", "SANTO ANTÔNIO DE PÁDUA - ES", "SÃO FIDÉLIS - ES", "SÃO JOSÉ DE UBÁ - ES", "SERRA - ES", "VILA VELHA - ES", "VITÓRIA - ES"
    "AGUANIL - MG", "ALPINÓPOLIS - MG", "ARAXÁ - MG", "BOA ESPERANÇA - MG", "CAMPO DO MEIO - MG", "CAMPOS ALTOS - MG", "CAMPOS GERAIS - MG", "CARMO DO RIO CLARO - MG", "CONQUISTA - MG", "COQUEIRAL - MG", "COROMANDEL - MG", "CRISTAIS - MG", "DELTA - MG", "FORTALEZA DE MINAS - MG", "GUAPÉ - MG", "GUARANÉSIA - MG", "GUAXUPÉ - MG", "IBIÁ - MG", "ILICÍNEA - MG", "ITAÚ DE MINAS - MG", "JACUÍ - MG", "MONTE SANTO DE MINAS - MG", "NEPOMUCENO - MG", "NOVA PONTE - MG", "PASSOS - MG", "PEDRINÓPOLIS - MG", "PERDIZES - MG", "PRATÁPOLIS - MG", "PRATINHA - MG", "SACRAMENTO - MG", "SANTA JULIANA - MG", "SANTANA DA VARGEM - MG", "SÃO GOTARDO - MG", "SÃO JOÃO BATISTA DO GLÓRIA - MG", "SÃO JOSÉ DA BARRA - MG", "SÃO SEBASTIÃO DO PARAÍSO - MG", "SÃO TOMÁS DE AQUINO - MG", "SERRA DO SALITRE - MG", "TAPIRA - MG", "UBERABA - MG", "UBERLÂNDIA - MG",
    "ALTINÓPOLIS - SP", "ARAMINA - SP", "BRASÍLIA - DF", "FRANCA - SP", "GUARÁ - SP", "IGARAPAVA - SP", "IPUÃ - SP", "ITIRAPUÃ - SP", "ITUVERAVA - SP", "MORRO AGUDO - SP", "ORLÂNDIA - SP", "PATROCÍNIO PAULISTA - SP", "RIBEIRÃO PRETO - SP", "SÃO JOAQUIM DA BARRA - SP", "SÃO JOSÉ DA BELA VISTA - SP"
]

CITIES_API_TERRITORIO_TELEFONEFIXO_T5_a_T7 = [
    "ARARUAMA - RJ", "ARMAÇÃO DOS BÚZIOS - RJ", "ARRAIAL DO CABO - RJ", 
    "CABO FRIO - RJ", "CASIMIRO DE ABREU - RJ", "IGUABA GRANDE - RJ", 
    "MACAÉ - RJ", "RIO DAS OSTRAS - RJ", "SÃO PEDRO DA ALDEIA - RJ", 
    "SAQUAREMA - RJ", "ALÉM PARAÍBA - RJ", "BARRA DO PIRAÍ - RJ", "BARRA MANSA - RJ", "BOM JARDIM - RJ", 
    "CACHOEIRAS DE MACACU - RJ", "CARMO - RJ", "COMENDADOR LEVY GASPARIAN - RJ", 
    "GUAPIMIRIM - RJ", "ITAIPAVA - RJ", "ITATIAIA - RJ", "MAGÉ - RJ", "MIGUEL PEREIRA - RJ", 
    "NOVA FRIBURGO - RJ", "PARAÍBA DO SUL - RJ", "PATY DO ALFERES - RJ", "PETRÓPOLIS - RJ", 
    "PINHEIRAL - RJ", "PORTO REAL - RJ", "RESENDE - RJ", "SAPUCAIA - RJ", "SILVA JARDIM - RJ", 
    "SUMIDOURO - RJ", "TERESÓPOLIS - RJ", "TRÊS RIOS - RJ", "VALENÇA - RJ", 
    "VASSOURAS - RJ", "VOLTA REDONDA - RJ",     "ANCHIETA - ES", "APERIBÉ - ES", "CACHOEIRO DE ITAPEMIRIM - ES", "CAMBUCI - ES", 
    "CAMPOS DOS GOYTACAZES - ES", "CANTAGALO - ES", "CARIACICA - ES", "CATAGUASES - ES", 
    "CORDEIRO - ES", "DUAS BARRAS - ES", "GUARAPARI - ES", "ITAOCARA - ES", "ITAPEMIRIM - ES", 
    "ITAPERUNA - ES", "LAJE DO MURIAÉ - ES", "MACUCO - ES", "MARATAÍZES - ES", "MIRACEMA - ES", 
    "MURIAÉ - ES", "PIÚMA - ES", "SANTO ANTÔNIO DE PÁDUA - ES", "SÃO FIDÉLIS - ES", 
    "SÃO JOSÉ DE UBÁ - ES", "SERRA - ES", "VILA VELHA - ES", "VITÓRIA - ES"
]



CITIES_API_TERRITORIO_T10_a_T14 = [ "CARNAÍBA - PE", "CARPINA - PE", "CARUARU - PE", "FLORES - PE", "GOIANÁ - PE", "ILHA DE ITAMARACÁ - PE", "IPOJUCA - PE", "ITAPISSUMA - PE", "LIMOEIRO - PE", "MIRANDIBA - PE", "NAZARÉ DA MATA - PE", "OLINDA - PE", "PARNAMIRIM - PE", "PAUDALHO - PE", "PAULISTA - PE", "SALGUEIRO - PE", "SANTA CRUZ DO CAPIBARIBE - PE", "SERRA TALHADA - PE", "SURUBIM - PE", "TERRA NOVA - PE", "TIMBAÚBA - PE", "TORITAMA - PE", "VERDEJANTE - PE",
    "ARACAJU - SE", "BARRA DOS COQUEIROS - SE", "CEDRO DE SÃO JOÃO - SE", 
    "DIVINA PASTORA - SE", "ITAPORANGA D'AJUDA - SE", "JAPOATÃ - SE", 
    "LAGARTO - SE", "LARANJEIRAS - SE", "NOSSA SENHORA DO SOCORRO - SE", 
    "PACATUBA - SE", "PROPRIÁ - SE", "ROSÁRIO DO CATETE - SE", 
    "SÃO CRISTÓVÃO - SE", "SIRIRI - SE", "TELHA - SE",
    "ACOPIARA - CE", "AIUABA - CE", "ANTONINA DO NORTE - CE", "ARARIPE - CE", 
    "ARNEIROZ - CE", "ASSARÉ - CE", "BARBALHA - CE", "BREJO SANTO - CE", 
    "CAMPOS SALES - CE", "CARIÚS - CE", "CATARINA - CE", "CEDRO - CE", 
    "CRATEÚS - CE", "CRATO - CE", "FARIAS BRITO - CE", "ICÓ - CE", "IGUATU - CE", 
    "INDEPENDÊNCIA - CE", "JATI - CE", "JUAZEIRO DO NORTE - CE", "JUCÁS - CE", 
    "LAVRAS DA MANGABEIRA - CE", "MAURITI - CE", "MISSÃO VELHA - CE", "MOMBAÇA - CE", 
    "ORÓS - CE", "PARAMBU - CE", "PIQUET CARNEIRO - CE", "PORTEIRAS - CE", "QUIXELÔ - CE", 
    "SALITRE - CE", "TARRAFAS - CE", "TAUÁ - CE", "VÁRZEA ALEGRE - CE",
    "ALTOS - PI", 
    "CAXIAS - MA", 
    "PARAUAPEBAS - PA", 
    "TERESINA - PI", 
    "TIMON - MA", 
    "CAUCAIA - CE", 
    "FORTALEZA - CE", 
    "MARACANAÚ - CE", 
    "ACARAÚ - CE", 
    "AQUIRAZ - CE", 
    "BEBERIBE - CE", 
    "CAMOCIM - CE", 
    "CASCAVEL - CE", 
    "CRUZ - CE", 
    "EUSÉBIO - CE", 
    "FORTIM - CE", 
    "FRECHEIRINHA - CE", 
    "GRAÇA - CE", 
    "GRANJA - CE", 
    "IBIAPINA - CE", 
    "ITAITINGA - CE", 
    "ITAPIPOCA - CE", 
    "ITAREMA - CE", 
    "JIJOCA DE JERICOACOARA - CE", 
    "LIMOEIRO DO NORTE - CE", 
    "MARANGUAPE - CE", 
    "MORADA NOVA - CE", 
    "MUCAMBO - CE", 
    "PACAJUS - CE", 
    "PACATUBA - CE", 
    "PACUJÁ - CE", 
    "PARACURU - CE", 
    "PARAIPABA - CE", 
    "PARNAÍBA - PI", 
    "PENTECOSTE - CE", 
    "PINDORETAMA - CE", 
    "QUIXADÁ - CE", 
    "RUSSAS - CE", 
    "SÃO BENEDITO - CE", 
    "SÃO GONÇALO DO AMARANTE - CE", 
    "SÃO LUÍS DO CURU - CE", 
    "SOBRAL - CE", 
    "TABULEIRO DO NORTE - CE", 
    "TIANGUÁ - CE", 
    "TRAIRI - CE", 
    "UBAJARA - CE"
]
CITIES_API_TERRITORIO_ALTOS_PARNAIBA_TERESINA = [
    "ALTOS - PI", "PARNAÍBA - PI", "TERESINA - PI"
]
CITIES_API_TERRITORIO_CIDADES_ESPECIAIS_1 = [
    "SÃO JOÃO BATISTA DO GLÓRIA - MG"    
]
CITIES_API_TERRITORIO_CIDADES_ESPECIAIS_2 = [
    "ITAÚ DE MINAS - MG", "SÃO JOÃO BATISTA DO GLÓRIA - MG"
]
CITIES_API_TERRITORIO_CIDADES_ESPECIAIS_3 = [
    "ITAÚ DE MINAS - MG"
]

# CIDADES DA OPERADORA DESKTOP - INTERNET

# CITIES_API_DESKTOP_BRONZE = ["MOGI GUAÇU - SP", "SÃO JOSÉ DOS CAMPOS - SP", "AGUAÍ - SP", "ÁGUAS DE SANTA BÁRBARA - SP", "AGUDOS - SP", "ALUMÍNIO - SP", "AMERICANA - SP", "AMÉRICO BRASILIENSE - SP", "AMPARO - SP", "ANGATUBA - SP", "ARAÇARIGUAMA - SP", "ARAÇOIABA DA SERRA - SP", "ARANDU - SP", "ARARAQUARA - SP", "ARARAS - SP", "AREALVA - SP", "AREIÓPOLIS - SP", "ATIBAIA - SP", "AVAÍ - SP", "AVARÉ - SP", "BARRA BONITA - SP", "BAURU - SP", "BIRITIBA MIRIM - SP", "BIRITIBA-MIRIM - SP", "BOA ESPERANÇA DO SUL - SP", "BOCAINA - SP", "BOFETE - SP", "BOITUVA - SP", "BOM JESUS DOS PERDÕES - SP", "BORBOREMA - SP", "BOREBI - SP", "BOTUCATU - SP", "BRAGANÇA PAULISTA - SP", "CABREÚVA - SP", "CAÇAPAVA - SP", "CAIEIRAS - SP", "CAMPINA DO MONTE ALEGRE - SP", "CAMPINAS - SP", "CAMPO LIMPO PAULISTA - SP", "CÂNDIDO RODRIGUES - SP", "CAPELA DO ALTO - SP", "CAPIVARI - SP", "CERQUEIRA CÉSAR - SP", "CERQUILHO - SP", "CESÁRIO LANGE - SP", "COLINA - SP", "CONCHAL - SP", "CONCHAS - SP", "CORDEIRÓPOLIS - SP", "CRISTAIS PAULISTA - SP", "DOBRADA - SP", "DOIS CÓRREGOS - SP", "DOURADO - SP", "ELIAS FAUSTO - SP", "ENGENHEIRO COELHO - SP", "FERNANDO PRESTES - SP", "FRANCA - SP", "FRANCISCO MORATO - SP", "FRANCO DA ROCHA - SP", "GAVIÃO PEIXOTO - SP", "GUAÍRA - SP", "GUARANTÃ - SP", "GUARAREMA - SP", "GUARIBA - SP", "GUARUJÁ - SP", "GUATAPARÁ - SP", "HOLAMBRA - SP", "HORTOLÂNDIA - SP", "LARAS - SP", "IBATÉ - SP", "IBITINGA - SP", "IGARAÇU DO TIETÊ - SP", "IGARATÁ - SP", "IPERÓ - SP", "IRACEMÁPOLIS - SP", "ITAÍ - SP", "ITAJOBI - SP", "ITAJU - SP", "ITANHAÉM - SP", "ITAPUÍ - SP", "ITATINGA - SP", "ITIRAPUÃ - SP", "ITU - SP", "JABORANDI - SP", "JABOTICABAL - SP", "JACAREÍ - SP", "JAGUARIÚNA - SP", "JARINU - SP", "JAÚ - SP", "JUMIRIM - SP", "JUNDIAÍ - SP", "LARANJAL PAULISTA - SP", "LENÇÓIS PAULISTA - SP", "LINDÓIA - SP", "LOUVEIRA - SP", "MACATUBA - SP", "MAIRIPORÃ - SP", "MANDURI - SP", "MATÃO - SP", "MINEIROS DO TIETÊ - SP", "MOGI DAS CRUZES - SP", "MONTE MOR - SP", "MOTUCA - SP", "NAZARÉ PAULISTA - SP", "NOVA EUROPA - SP", "NOVA ODESSA - SP", "ÓLEO - SP", "PARANAPANEMA - SP", "PARDINHO - SP", "PATROCÍNIO PAULISTA - SP", "PAULÍNIA - SP", "PEDERNEIRAS - SP", "PEDREIRA - SP", "PEREIRAS - SP", "PINDORAMA - SP", "PIRACAIA - SP", "PIRACICABA - SP", "PIRATININGA - SP", "PITANGUEIRAS - SP", "PORANGABA - SP", "PRAIA GRANDE - SP", "PRATÂNIA - SP", "PRESIDENTE ALVES - SP", "QUADRA - SP", "RAFARD - SP", "RIBEIRÃO BONITO - SP", "RIBEIRÃO CORRENTE - SP", "RIBEIRÃO PRETO - SP", "RINCÃO - SP", "RIO CLARO - SP", "RIO DAS PEDRAS - SP", "SALESÓPOLIS - SP", "SALTINHO - SP", "SALTO DE PIRAPORA - SP", "SANTA ADÉLIA - SP", "SANTA BÁRBARA D’OESTE - SP", "ITAPETININGA - SP", "ITÁPOLIS - SP", "SANTA ERNESTINA - SP", "SANTA GERTRUDES - SP", "SANTA LÚCIA - SP", "SANTO ANTÔNIO DE POSSE - SP", "SANTOS - SP", "SÃO CARLOS - SP", "SÃO MANUEL - SP", "SÃO VICENTE - SP", "SARAPUÍ - SP", "SERRA AZUL - SP", "SERRA NEGRA - SP", "SOROCABA - SP", "SUMARÉ - SP", "TABATINGA - SP", "TATUÍ - SP", "TAUBATÉ - SP", "TIETÊ - SP", "TRABIJU - SP", "TREMEMBÉ - SP", "VALINHOS - SP", "VÁRZEA PAULISTA - SP", "VINHEDO - SP", "VOTORANTIM - SP",  "MONGAGUÁ - SP"]
# CITIES_API_DESKTOP_PRATA = ["BÁLSAMO - SP", "BARRETOS - SP", "OLÍMPIA - SP"]
# CITIS_API_DESKTOP_OURO = ["BEBEDOURO - SP"]
# CITIS_API_DESKTOP_PLATINA = ["SANTA CRUZ DAS PALMEIRAS - SP", "CAFELÂNDIA - SP", "CASA BRANCA - SP", "COSMÓPOLIS - SP", "ESTIVA GERBI - SP", "INDAIATUBA - SP", "ITUPEVA - SP", "LINS - SP", "CEDRAL - SP", "ARTUR NOGUEIRA - SP", "CRAVINHOS - SP", "CUBATÃO - SP", "DESCALVADO - SP", "LEME - SP", "LIMEIRA - SP", "MIRASSOL - SP", "MOGI-MIRIM - SP", "MONTE ALEGRE DO SUL - SP", "MONTE ALTO - SP", "PERUÍBE - SP", "PILAR DO SUL - SP", "PIRASSUNUNGA - SP", "PORTO FERREIRA - SP", "SANTA RITA DO PASSA QUATRO - SP", "SÃO JOSÉ DO RIO PRETO - SP",  "TAMBAÚ - SP"]
# CITIS_API_DESKTOP_DIAMANTE = ["SÃO PAULO - SP"]
# CITIS_API_DESKTOP_ASCENDENTE = ["SANTA BRANCA - SP"]

DESKTOP_PADRAO = [
    "AGUAÍ - SP",
    "ALUMÍNIO - SP",
    "AMERICANA - SP",
    "AMÉRICO BRASILIENSE - SP",
    "AMPARO - SP",
    "ARAÇARIGUAMA - SP",
    "ARARAQUARA - SP",
    "ATIBAIA - SP",
    "AVAÍ - SP",
    "BAURU - SP",
    "BIRITIBA-MIRIM - SP",
    "BOA ESPERANÇA DO SUL - SP",
    "BOM JESUS DOS PERDÕES - SP",
    "BORBOREMA - SP",
    "BOTUCATU - SP",
    "BRAGANÇA PAULISTA - SP",
    "CABREÚVA - SP",
    "CAÇAPAVA - SP",
    "CAIEIRAS - SP",
    "CAMPINAS - SP",
    "CAMPO LIMPO PAULISTA - SP",
    "CAPIVARI - SP",
    "CASA BRANCA - SP",
    "COLINA - SP",
    "CORDEIRÓPOLIS - SP",
    "CUBATÃO - SP",
    "DESCALVADO - SP",
    "DOBRADA - SP",
    "DOURADO - SP",
    "ELIAS FAUSTO - SP",
    "ENGENHEIRO COELHO - SP",
    "FERNANDO PRESTES - SP",
    "FRANCISCO MORATO - SP",
    "FRANCO DA ROCHA - SP",
    "GAVIÃO PEIXOTO - SP",
    "GUAÍRA - SP",
    "GUARANTÃ - SP",
    "GUARAREMA - SP",
    "GUARIBA - SP",
    "GUARUJÁ - SP",
    "GUATAPARÁ - SP",
    "HOLAMBRA - SP",
    "HORTOLÂNDIA - SP",
    "IBATÉ - SP",
    "IBITINGA - SP",
    "IGARATÁ - SP",
    "IRACEMÁPOLIS - SP",
    "ITAJOBI - SP",
    "ITANHAÉM - SP",
    "ITÁPOLIS - SP",
    "JABORANDI - SP",
    "JABOTICABAL - SP",
    "JACAREÍ - SP",
    "JAGUARIÚNA - SP",
    "JARINU - SP",
    "LENÇÓIS PAULISTA - SP",
    "LINDÓIA - SP",
    "LOUVEIRA - SP",
    "MAIRIPORÃ - SP",
    "MATÃO - SP",
    "MOGI DAS CRUZES - SP",
    "MONGAGUÁ - SP",
    "MONTE ALTO - SP",
    "MONTE MOR - SP",
    "MOTUCA - SP",
    "NAZARÉ PAULISTA - SP",
    "NOVA EUROPA - SP",
    "NOVA ODESSA - SP",
    "PAULÍNIA - SP",
    "PEDREIRA - SP",
    "PINDORAMA - SP",
    "PIRACAIA - SP",
    "PIRACICABA - SP",
    "PIRAJUÍ - SP",
    "PIRATININGA - SP",
    "PITANGUEIRAS - SP",
    "PRAIA GRANDE - SP",
    "PRESIDENTE ALVES - SP",
    "RAFARD - SP",
    "RIBEIRÃO BONITO - SP",
    "RINCÃO - SP",
    "SALESÓPOLIS - SP",
    "SANTA ADÉLIA - SP",
    "SANTA BÁRBARA D'OESTE - SP",
    "SANTA BRANCA - SP",
    "SANTA GERTRUDES - SP",
    "SANTA LÚCIA - SP",
    "SANTA RITA DO PASSA QUATRO - SP",
    "SANTO ANTÔNIO DE POSSE - SP",
    "SANTOS - SP",
    "SÃO BERNARDO DO CAMPO - SP",
    "SÃO CARLOS - SP",
    "SÃO JOSÉ DOS CAMPOS - SP",
    "SÃO VICENTE - SP",
    "SERRA AZUL - SP",
    "SERRA NEGRA - SP",
    "SOROCABA - SP",
    "SUMARÉ - SP",
    "TABATINGA - SP",
    "TAUBATÉ - SP",
    "TREMEMBÉ - SP",
    "VÁRZEA PAULISTA - SP",
    "VINHEDO - SP",
    "VOTORANTIM - SP"
]

DESKTOP_BARRETOS = [
    "BARRETOS - SP",
    "BEBEDOURO - SP",
    "OLÍMPIA - SP"
]

DESKTOP_TIO_SAM = [
    "ARARAS - SP",
    "ARTUR NOGUEIRA - SP",
    "BADY BASSITT - SP",
    "CAFELÂNDIA - SP",
    "CEDRAL - SP",
    "CONCHAL - SP",
    "COSMÓPOLIS - SP",
    "CRAVINHOS - SP",
    "ESTIVA GERBI - SP",
    "GUAPIAÇU - SP",
    "INDAIATUBA - SP",
    "ITUPEVA - SP",
    "JUNDIAÍ - SP",
    "LEME - SP",
    "LIMEIRA - SP",
    "LINS - SP",
    "MIRASSOL - SP",
    "MOGI GUAÇU - SP",
    "MOGI MIRIM - SP",
    "PERUÍBE - SP",
    "PIRASSUNUNGA - SP",
    "PORTO FERREIRA - SP",
    "SANTA CRUZ DAS PALMEIRAS - SP",
    "SANTA ROSA DE VITERBO - SP",
    "SÃO JOSÉ DO RIO PRETO - SP",
    "TAMBAÚ - SP",
    "UCHOA - SP",
    "VALINHOS - SP"
]


FASTERNET_PADRAO = [
    "ANGATUBA - SP",
    "ARAÇOIABA DA SERRA - SP",
    "BOITUVA - SP",
    "CAMPINA DO MONTE ALEGRE - SP",
    "CAPELA DO ALTO - SP",
    "CERQUILHO - SP",
    "CESÁRIO LANGE - SP",
    "CONCHAS - SP",
    "CRISTAIS PAULISTA - SP",
    "IPERÓ - SP",
    "ITIRAPUÃ - SP",
    "JUMIRIM - SP",
    "LARANJAL PAULISTA - SP",
    "MONTE ALEGRE DO SUL - SP",
    "PATROCÍNIO PAULISTA - SP",
    "PEREIRAS - SP",
    "PILAR DO SUL - SP",
    "PORANGABA - SP",
    "QUADRA - SP",
    "RIBEIRÃO CORRENTE - SP",
    "RIO CLARO - SP",
    "RIO DAS PEDRAS - SP",
    "SALTINHO - SP",
    "SALTO DE PIRAPORA - SP",
    "SARAPUÍ - SP",
    "TATUÍ - SP",
    "TIETÊ - SP"
]

FASTERNET_TIO_SAM = [
    "BOFETE - SP",
    "FRANCA - SP",
    "ITAPETININGA - SP",
    "ITÚ - SP",
    "SALTO - SP"
]


LPNET_PADRAO = [
    "AGUDOS - SP",
    "AREIÓPOLIS - SP",
    "BARRA BONITA - SP",
    "BOCAINA - SP",
    "BOREBI - SP",
    "CÂNDIDO RODRIGUES - SP",
    "DOIS CÓRREGOS - SP",
    "IGARAÇU DO TIETÊ - SP",
    "ITAJU - SP",
    "ITAPUÍ - SP",
    "JAÚ - SP",
    "MACATUBA - SP",
    "MINEIROS DO TIETÊ - SP",
    "ÓLEO - SP",
    "PARANAPANEMA - SP",
    "PEDERNEIRAS - SP",
    "PRATÂNIA - SP",
    "SANTA ERNESTINA - SP",
    "SÃO MANUEL - SP",
    "TRABIJU - SP"
]

LPNET_TIO_SAM = [
    "ÁGUAS DE SANTA BÁRBARA - SP",
    "ARANDU - SP",
    "AVARÉ - SP",
    "CERQUEIRA CÉSAR - SP",
    "IARAS - SP",
    "ITAI - SP",
    "ITATINGA - SP",
    "MANDURI - SP",
    "PARDINHO - SP"
]

# CIDADES DA OPERADORA ALGAR - INTERNET

CITIES_ALGAR_600MB = ["AMERICO BRASILIENSE - SP",
    "ANAPOLIS - GO",
    "APARECIDA DE GOIANIA - GO",
    "ARACAJU - SE",
    "ARARAQUARA - SP",
    "ARARAS - SP",
    "BRUSQUE - SC",
    "BARUERI - SP",
    "CRICIUMA - SC",
    "JARAGUA DO SUL - SC",
    "LAGES - SC",
    "PALHOCA - SC",
    "SAO BENTO DO SUL - SC",
    "CARIACICA - ES",
    "CAUCAIA - CE",
    "CRAVINHOS - SP",
    "CUBATAO - SP",
    "DIADEMA - SP",
    "EUSEBIO - CE",
    "FEIRA DE SANTANA - BA",
    "GOIANIA - GO",
    "GUARA - DF",
    "GUARULHOS - SP",
    "ITU - SP",
    "JABOTICABAL - SP",
    "LAURO DE FREITAS - BA",
    "MARACANAU - CE",
    "MATAO - SP",
    "MOGI DAS CRUZES - SP",
    "MOGI GUACU - SP",
    "MOGI MIRIM - SP",
    "OSASCO - SP",
    "SALTO - SP",
    "SALVADOR - BA",
    "SANTA GERTRUDES - SP",
    "SANTO ANDRE - SP",
    "SAO BERNARDO DO CAMPO - SP",
    "SAO CAETANO DO SUL - SP",
    "SAO JOSE DO RIO PRETO - SP",
    "SÃO PAULO - SP",
    "SERRA - ES",
    "VARZEA PAULISTA - SP",
    "VILA VELHA - ES",
    "VITORIA - ES"]
CITIES_ALGAR_800MB = ["BRASÍLIA - DF", "CEILANDIA - DF", "SAMAMBAIA - DF", "SANTA BARBARA D OESTE - SP", "TAGUATINGA - DF"]
CITIES_ALGAR_SPECIALCITIES = ["PASSOS - MG", "POUSO ALEGRE - MG", "VARGINIA - MG"]

# CLUSTER BL_FIBRA

BL_FIBRA = [
    "BELO HORIZONTE - MG",
    "CONTAGEM - MG",
    "SABARÁ - MG", 
    "SANTA LUZIA - MG"
]


def get_api_url_desktop(cidade):
    if cidade in DESKTOP_PADRAO:
        return f"{URL_VPS}webhook/workflow_desktop-padrao"
    elif cidade in DESKTOP_BARRETOS:
        return f"{URL_VPS}/webhook/workflow_desktop-barretos"
    elif cidade in DESKTOP_TIO_SAM:
        return f"{URL_VPS}/webhook/workflow_desktop-tiosam"
    elif cidade in FASTERNET_PADRAO:
        return f"{URL_VPS}/webhook/workflow_fasternet-padrao"
    elif cidade in FASTERNET_TIO_SAM:
        return f"{URL_VPS}/webhook/workflow_fasternet-tiosam"
    elif cidade in LPNET_PADRAO:
        return f"{URL_VPS}/webhook/workflow_lpnet-padrao"
    elif cidade in LPNET_TIO_SAM:
        return f"{URL_VPS}/webhook/workflow_lpnet-tiosam"
    else: 
        return None


def get_api_url_giga(cidade):

    urls = []

    if cidade in CITIES_API_TERRITORIO_T1_a_T9:
        urls.append(f"{URL_VPS}/webhook/workflowt1_a_t9")
    if cidade in CITIES_API_TERRITORIO_T10_a_T14:
        urls.append(f"{URL_VPS}/webhook/workflowt10_t14")
    if cidade in CITIES_API_TERRITORIO_TELEFONEFIXO_T5_a_T7:
        urls.append(f"{URL_VPS}/webhook/workflow_TELEFONEFIXO_T5_a_T7")
    if cidade in CITIES_API_TERRITORIO_ALTOS_PARNAIBA_TERESINA:
        urls.append(f"{URL_VPS}/webhook/workflowt_ALTOS_PARNAIBA_TERESINA")
    if cidade in CITIES_API_TERRITORIO_CIDADES_ESPECIAIS_1:
        urls.append(f"{URL_VPS}/webhook/workflowt_CIDADES_ESPECIAIS_1")
    if cidade in CITIES_API_TERRITORIO_CIDADES_ESPECIAIS_2:
        urls.append(f"{URL_VPS}/webhook/workflowt_CIDADES_ESPECIAIS_2")
    if cidade in CITIES_API_TERRITORIO_CIDADES_ESPECIAIS_3:
        urls.append(f"{URL_VPS}/webhook/workflowt_CIDADES_ESPECIAIS_3") 

    return urls or None

def get_api_url_vero(cidade):

    urls = []

    if cidade in CITIES_API_OURO:
        urls.append(f"{URL_VPS}/webhook/workflowouro")
    if cidade in CITYES_API_GRAFENO_75:
        urls.append(f"{URL_VPS}/webhook/workflow_grafeno_75")
    if cidade in CITYES_API_GRAFENO_80:
        urls.append(f"{URL_VPS}/webhook/workflow_grafeno_80")
    if cidade in CITIES_API_SAFIRA:
        urls.append(f"{URL_VPS}/webhook/workflow_safira")
    if cidade in CITIES_API_PADRAO:
        urls.append(f"{URL_VPS}/webhook/workflowpadrao")
    if cidade in CITIES_API_REDE_NEUTRA:
        urls.append(f"{URL_VPS}/webhook/workflowredeneutra")
    if cidade in CITIES_API_PRATA:
        urls.append(f"{URL_VPS}/webhook/workflowprata")
    
    return urls or None 


def get_api_url_algar(cidade):
    if cidade in CITIES_ALGAR_600MB:
        return f"{URL_VPS}/webhook/workflow_algar_600MB"
    elif cidade in CITIES_ALGAR_800MB:
        return f"{URL_VPS}/webhook/workflow_algar_800MB"
    elif cidade in CITIES_ALGAR_SPECIALCITIES:
        return f"{URL_VPS}/webhook/workflow_algar_specialcities"
    else: 
        return f"{URL_VPS}/webhook/workflow_algar"



def atualizar_campo_no_crm(dados):
    pass


def atualizar_campo_e_chamar_api_algar(cidade, entity_id):

    atualizar_campo_no_crm(entity_id)

    url_api = get_api_url_algar(cidade)
    if url_api:
        response = requests.post(f"{url_api}?deal_id={entity_id}", json={"cidade": cidade})
        return response.json()  
    else:
        return {"error": "Cidade não mapeada"}



def atualizar_campo_e_chamar_api_desktop(cidade, entity_id):

    atualizar_campo_no_crm(entity_id)

    url_api = get_api_url_desktop(cidade)
    
    if url_api:
        response = requests.post(f"{url_api}?deal_id={entity_id}", json={"cidade": cidade})
        return response.json()  
    else:
        return {"error": "Cidade não mapeada"}
        

def atualizar_campo_e_chamar_api_giga(cidade, entity_id):

    atualizar_campo_no_crm(entity_id)


    urls = get_api_url_giga(cidade) 


    if not urls:
        return {"error": "Cidade não mapeada"}


    responses = []
    for url in urls:
        try:
           
            response = requests.post(f"{url}?deal_id={entity_id}", json={"cidade": cidade})
            responses.append({"url": url, "status_code": response.status_code, "response": response.json()})
        except Exception as e:
            responses.append({"url": url, "error": str(e)})

    return responses

def atualizar_campo_e_chamar_api_vero(cidade, entity_id):
    

    atualizar_campo_no_crm(entity_id)


    urls = get_api_url_vero(cidade) 


    if not urls:
        return {"error": "Cidade não mapeada"}


    responses = []
    for url in urls:
        try:
           
            response = requests.post(f"{url}?deal_id={entity_id}", json={"cidade": cidade})
            responses.append({"url": url, "status_code": response.status_code, "response": response.json()})
        except Exception as e:
            responses.append({"url": url, "error": str(e)})

    return responses

def atualizar_campo_e_chamar_api_bl(cidade, entity_id):
    

    atualizar_campo_no_crm(entity_id)


    url = f"{URL_VPS}/webhook/workflow_bl-fibra" 


    if cidade not in BL_FIBRA:
        return {"error": "Cidade não mapeada"}


    
    try:
    
        response = requests.post(f"{url}?deal_id={entity_id}", json={"cidade": cidade})
        response = response.json()
    except Exception as e:
        response = {"url": url, "error": str(e)}

    return response



def make_request_with_retries(method, url, **kwargs):
    max_retries = 5  
    for attempt in range(max_retries):
        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code in [200, 201]:  
                return response
            else:
                log_erro(f"Erro {response.status_code} na tentativa {attempt + 1}", response.text)
        except requests.exceptions.RequestException as e:
            log_erro("Erro de conexão", e)
        time.sleep(2)  
    return None


def handle_request_errors(response, error_message, details=None):
    if response is None or response.status_code >= 400:
        return jsonify({"error": error_message, "details": details or response.text if response else "Nenhuma resposta"}), 400




@app.route('/update-plan-desktop/<string:entity_id>', methods=['POST'])
def update_plan_desktop(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries('GET', get_deal_url, params={"id": entity_id})
        handle_request_errors(get_deal_response, "Falha ao buscar os dados da negociação")
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data['result'].get("UF_CRM_1731588487")
        uf = get_deal_data['result'].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400
        
        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries('POST', update_url, json={
            "id": entity_id,
            "fields": {"UF_CRM_1733493949": cidade_completa}
        })

        api_response = atualizar_campo_e_chamar_api_desktop(cidade_completa, entity_id)
        return jsonify ({"message": "Campo atualizado com sucesso!", "cidade_completa": cidade_completa, "api_response": api_response}), 200
    
    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500



@app.route('/update-plan-algar/<string:entity_id>', methods=['POST'])
def update_plan_algar(entity_id):
    try:
        print("ola")
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        print("tudo bem")

        get_deal_response = make_request_with_retries('GET', get_deal_url, params={"id": entity_id})
        print("bom dia")

        handle_request_errors(get_deal_response, "Falha ao buscar os dados da negociação")
        print("e aí")

        get_deal_data = get_deal_response.json()
        print("como vai")


        cidade = get_deal_data['result'].get("UF_CRM_1731588487")
        print("como estas")

        uf = get_deal_data['result'].get("UF_CRM_1731589190")

        print("Boa tarder")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        print("vamos")
        
        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        print("sim")

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        print("print")

        update_response = make_request_with_retries('POST', update_url, json={
            "id": entity_id,
            "fields": {"UF_CRM_1733493949": cidade_completa}
        })

        print("calma")

        api_response = atualizar_campo_e_chamar_api_algar(cidade_completa, entity_id)

        print("quase")
        return jsonify ({"message": "Campo atualizado com sucesso!", "cidade_completa": cidade_completa, "api_response": api_response}), 200
    
    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"atualizado_em":"14/02", "error": "Erro interno no servidor", "details": str(e)}), 500





@app.route('/update-plan-giga/<string:entity_id>', methods=['POST'])
def update_plan_giga(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries('GET', get_deal_url, params={"id": entity_id})
        handle_request_errors(get_deal_response, "Falha ao buscar os dados da negociação")
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data['result'].get("UF_CRM_1731588487")
        uf = get_deal_data['result'].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400
        
        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries('POST', update_url, json={
            "id": entity_id,
            "fields": {"UF_CRM_1733493949": cidade_completa}
        })

        api_response = atualizar_campo_e_chamar_api_giga(cidade_completa, entity_id)
        return jsonify ({"message": "Campo atualizado com sucesso!", "cidade_completa": cidade_completa, "api_response": api_response}), 200
    
    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@app.route('/update-plan-vero/<string:entity_id>', methods=['POST'])
def update_plan_vero(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries('GET', get_deal_url, params={"id": entity_id})
        handle_request_errors(get_deal_response, "Falha ao buscar os dados da negociação")
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data['result'].get("UF_CRM_1731588487")
        uf = get_deal_data['result'].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400
        
        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries('POST', update_url, json={
            "id": entity_id,
            "fields": {"UF_CRM_1733493949": cidade_completa}
        })

        api_response = atualizar_campo_e_chamar_api_vero(cidade_completa, entity_id)
        return jsonify ({"message": "Campo atualizado com sucesso!", "cidade_completa": cidade_completa, "api_response": api_response}), 200
    
    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500
    
@app.route('/update-plan-bl/<string:entity_id>', methods=['POST'])
def update_plan_bl(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries('GET', get_deal_url, params={"id": entity_id})
        handle_request_errors(get_deal_response, "Falha ao buscar os dados da negociação")
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data['result'].get("UF_CRM_1731588487")
        uf = get_deal_data['result'].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400
        
        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries('POST', update_url, json={
            "id": entity_id,
            "fields": {"UF_CRM_1733493949": cidade_completa}
        })

        api_response = atualizar_campo_e_chamar_api_bl(cidade_completa, entity_id)
        return jsonify ({"message": "Campo atualizado com sucesso!", "cidade_completa": cidade_completa, "api_response": api_response}), 200
    
    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1473)
