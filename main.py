from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import time

app = Flask(__name__)
load_dotenv()

BITRIX_WEBHOOK_URL = "https://marketingsolucoes.bitrix24.com.br/rest/35002/6boa127nfoawdnwh/"
URL_VPS = "https://grupo--solucoes-workflow-bitrix24.rvc6im.easypanel.host"

from cities import (
    CITIES_API_ADAPTER_PADRAO,
    CITIES_API_ADAPTER_OURO,
    CITIES_API_ADAPTER_PRATA,
    CITIES_API_ADAPTER_ESPECIAIS,
    CITIES_API_IXC_ESPECIAIS,
    CITIES_API_IXC_PRATA,
    CITIES_API_IXC_OURO,
    CITIES_API_NG_OURO,
    CITIES_API_NG_PADRAO,
    CITIES_API_NG_PRATA,
    CITIES_API_NG_ESPECIAIS,
    CITIES_API_SIMETRA_PRATA,
    CITIES_API_SIMETRA_ESPECIAS,
    CITIES_API_SIMETRA_OURO,
    CITIES_API_GIGA_TERRITORIO_T1_a_T9,
    CITIES_API_GIGA_TERRITORIO_T10_a_T14,
    CITIES_API_GIGA_TERRITORIO_CIDADES_ESPECIAIS,
    CITIES_API_DESKTOP_PADRAO,
    CITIES_API_DESKTOP_BARRETOS,
    CITIES_API_DESKTOP_TIO_SAM,
    CITIES_API_DESKTOP_FASTERNET_PADRAO,
    CITIES_API_DESKTOP_FASTERNET_TIO_SAM,
    CITIES_API_DESKTOP_LPNET_PADRAO,
    CITIES_API_BL_FIBRA_PADRAO,
    CITIES_API_MASTER_PADRAO,
    CITIES_API_IMPLANTAR_PADRAO,
    CITIES_API_NIO_PADRAO,
    CITIES_API_REDE_NEUTRA_PADRAO,
    CITIES_API_CDB_PADRAO
)

def get_api_url_vero(cidade):
    clusters = []
    if cidade in CITIES_API_REDE_NEUTRA_PADRAO: 
        clusters.append("REDE NEUTRA PADRAO")
    return clusters

def get_api_url_giga(cidade):
    clusters = []
    if cidade in CITIES_API_GIGA_TERRITORIO_T1_a_T9:
        clusters.append("GIGA T1 A T9")
    return clusters

def get_api_url_desktop(cidade):
    clusters = []
    if cidade in CITIES_API_DESKTOP_PADRAO:
        clusters.append("DESKTOP PADRAO")
    return clusters

def get_api_url_blfibra(cidade):
    clusters = []
    if cidade in CITIES_API_BL_FIBRA_PADRAO:
        clusters.append("BL FIBRA PADRAO")
    return clusters

def get_api_url_master(cidade):
    clusters = []
    if cidade in CITIES_API_MASTER_PADRAO:
        clusters.append("MASTER PADRAO")
    return clusters

def get_api_url_implantar(cidade):
    clusters = []
    if cidade in CITIES_API_IMPLANTAR_PADRAO:
        clusters.append("IMPLANTAR PADRAO")
    return clusters

def get_api_url_nio(cidade):
    clusters = []
    if cidade in CITIES_API_NIO_PADRAO:
        clusters.append("NIO PADRAO")
    return clusters


def get_api_url_cdb(cidade):
    clusters = []
    if cidade in CITIES_API_CDB_PADRAO:
        clusters.append("CDB PADRAO")
    return clusters




def make_request_with_retries(method, url, **kwargs):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code in [200, 201]:
                return response
        except:
            time.sleep(1)
    return None

def adicionar_clusters_no_deal(entity_id, novos_clusters):
    get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
    get_deal_response = make_request_with_retries("GET", get_deal_url, params={"id": entity_id})
    deal_data = get_deal_response.json()
    cluster_atual = deal_data["result"].get("UF_CRM_1741717512", "")
    clusters_existentes = [c.strip() for c in cluster_atual.split(",") if c.strip()]
    clusters_novos = [c for c in novos_clusters if c not in clusters_existentes]
    clusters_final = clusters_existentes + clusters_novos
    clusters_to_string = ", ".join(clusters_final)
    requests.post(f"{BITRIX_WEBHOOK_URL}/crm.deal.update", json={"id": entity_id, "fields": {"UF_CRM_1741717512": clusters_to_string}})
    return clusters_to_string

@app.route("/update-plan/<string:entity_id>", methods=["POST"])
def update_plan(entity_id):
    get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
    get_deal_response = make_request_with_retries("GET", get_deal_url, params={"id": entity_id})
    get_deal_data = get_deal_response.json()
    cidade = get_deal_data["result"].get("UF_CRM_1731588487")
    uf = get_deal_data["result"].get("UF_CRM_1731589190")
    viabilidade_raw = get_deal_data["result"].get("UF_CRM_1699452141037", [])
    cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

    operadora_funcoes = {
        "132": get_api_url_vero,
        "34652": get_api_url_giga,
        "48764": get_api_url_desktop,
        "49750": get_api_url_master,
        "60994": get_api_url_blfibra,
        "61062": get_api_url_implantar,
        "61156": get_api_url_cdb,
        "61158": get_api_url_nio
    }

    clusters_gerais = []
    for operadora_id in viabilidade_raw:
        funcao = operadora_funcoes.get(str(operadora_id))
        if funcao:
            clusters_gerais += funcao(cidade_completa)

    clusters_gerais = list(set(clusters_gerais))
    adicionar_clusters_no_deal(entity_id, clusters_gerais)

    requests.post(f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}")

    return jsonify({"message": "Clusters atualizados e workflow disparado.", "clusters": clusters_gerais}), 200

if __name__ == "__main__":
    app.run(port=1421, host="0.0.0.0")
