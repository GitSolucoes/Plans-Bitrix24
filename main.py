from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import time

app = Flask(__name__)

load_dotenv()

BITRIX_WEBHOOK_URL = os.getenv("BITRIX_WEBHOOK_URL")
URL_VPS = os.getenv("URL_VPS")

BITRIX_WEBHOOK_URL = f"{BITRIX_WEBHOOK_URL}"


def log_erro(mensagem, e=None):
    """Função de log de erro para registrar exceções"""
    import traceback

    erro_detalhado = traceback.format_exc()
    print(f"\n[ERRO] {mensagem}")
    if e:
        print(f"[DETALHES] {str(e)}")
    print(f"[TRACEBACK] {erro_detalhado}\n")


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
    CITIES_API_OI_PADRAO
)



# FUNCÃO PARA VERO
def get_api_url_vero(cidade):
    clusters = []
    if cidade in  CITIES_API_ADAPTER_PADRAO:
        clusters.append("VERO ADAPTER PADRAO")
    if cidade in CITIES_API_ADAPTER_OURO:
        clusters.append("VERO ADAPTER OURO")
    if cidade in CITIES_API_ADAPTER_PRATA:
        clusters.append("VERO ADAPTER PRATA")
    if cidade in CITIES_API_ADAPTER_ESPECIAIS:
        clusters.append("VERO ADAPTER ESPECIAIS")
    if cidade in CITIES_API_IXC_ESPECIAIS:
        clusters.append("VERO IXC ESPECIAIS")
    if cidade in CITIES_API_IXC_OURO:
        clusters.append("VERO IXC OURO")
    if cidade in CITIES_API_IXC_PRATA:
        clusters.append("VERO IXC PRATA")
    if cidade in CITIES_API_NG_OURO:
        clusters.append("VERO NG OURO")
    if cidade in CITIES_API_NG_PADRAO:
        clusters.append("VERO NG PADRAO")
    if cidade in CITIES_API_NG_PRATA:
        clusters.append("VERO NG PRATA")
    if cidade in CITIES_API_NG_ESPECIAIS:
        clusters.append("VERO NG ESPECIAL")
    if cidade in CITIES_API_SIMETRA_ESPECIAS:
        clusters.append("VERO SIMETRA ESPECIAL")
    if cidade in CITIES_API_SIMETRA_OURO:
        clusters.append("VERO SIMETRA OURO")
    if cidade in CITIES_API_SIMETRA_PRATA:
        clusters.append("VERO SIMENTRA PRATA")
    return clusters


# FUNÇÃO PARA DESKTOP
def get_api_url_desktop(cidade):
    clusters = []
    if cidade in CITIES_API_DESKTOP_PADRAO:
        clusters.append("DESKTOP PADRAO")
    if cidade in CITIES_API_DESKTOP_BARRETOS:
        clusters.append("DESKTOP BARRETOS")
    if cidade in CITIES_API_DESKTOP_TIO_SAM:
        clusters.append("DESKTOP TIOSAM")
    if cidade in CITIES_API_DESKTOP_FASTERNET_PADRAO:
        clusters.append("FASTERNET PADRAO")
    if cidade in CITIES_API_DESKTOP_FASTERNET_TIO_SAM:
        clusters.append("FASTERNET TIOSAM")
    if cidade in CITIES_API_DESKTOP_LPNET_PADRAO:
        clusters.append("LPNET PADRAO")
    return clusters


# FUNÇÃO PARA GIGA+
def get_api_url_giga(cidade):
    clusters = []
    if cidade in CITIES_API_GIGA_TERRITORIO_T1_a_T9:
        clusters.append("GIGA T1 A T9")
    if cidade in CITIES_API_GIGA_TERRITORIO_T10_a_T14:
        clusters.append("GIGA T10 A T14")
    if cidade in CITIES_API_GIGA_TERRITORIO_CIDADES_ESPECIAIS:
        clusters.append("GIGA CIDADES ESPECIAIS")
    return clusters


# FUNÇÃO PARA BL FIBRA
def get_api_url_blfibra(cidade):
    clusters = []
    if cidade in CITIES_API_BL_FIBRA_PADRAO:
        clusters.append("BL FIBRA PADRAO")
    return clusters


# FUNÇÃO PARA MASTER
def get_api_url_master(cidade):
    clusters = []
    if cidade in CITIES_API_MASTER_PADRAO:
        clusters.append("MASTER PADRAO")
    return clusters

def get_api_url_oi(cidade):
    clusters = []
    if cidade in CITIES_API_OI_PADRAO:
        clusters.append("OI PADRAO")
    return clusters

# FUNCÃO PARA IMPLANTAR
def get_api_url_implantar(cidade):
    clusters = []
    if cidade in CITIES_API_IMPLANTAR_PADRAO:
        clusters.append("IMPLANTAR PADRAO")
    return clusters


# FUNÇÃO UPDATE_CALL_WORKFLOW_VERO
def update_field_and_call_workflow_vero(cidade, entity_id):
    clusters = get_api_url_vero(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}"
        )
        return {"error": "Error"}

    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}


# FUNÇÃO UPDATE_CALL_WORKFLOW_GIGA+
def update_field_and_call_workflow_giga(cidade, entity_id):
    clusters = get_api_url_giga(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}"
        )
        return {"error": "Error"}

    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}


# FUNÇÃO UPDATE_CALL_WORKFLOW_DESKTOP
def update_field_and_call_workflow_desktop(cidade, entity_id):
    clusters = get_api_url_desktop(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}"
        )
        return {"error": "Error"}

    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}


# FUNÇÃO UPDATE_CALL_WORKFLOW_MASTER
def update_field_and_call_workflow_master(cidade, entity_id):
    clusters = get_api_url_master(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}"
        )
        return {"error": "Error"}

    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}


# FUNÇÃO UPDATE_CALL_WORKFLOW_BL_FIBRA
def update_field_and_call_workflow_blfibra(cidade, entity_id):
    clusters = get_api_url_blfibra(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}"
        )
        return {"error": "Error"}

    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}

# FUNÇÃO UPDATE_CALL_WORKFLOW_IMPLANTAR
def update_field_and_call_workflow_implantar(cidade, entity_id):
    clusters = get_api_url_implantar(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}"
        )
        return {"error": "Error"}

    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}



def update_field_and_call_workflow_oi(cidade, entity_id):
    clusters = get_api_url_oi(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}"
        )
        return {"error": "Error"}

    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}



def make_request_with_retries(method, url, **kwargs):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code in [200, 201]:
                return response
            else:
                log_erro(
                    f"Erro {response.status_code} na tentativa {attempt + 1}",
                    response.text,
                )
        except requests.exceptions.RequestException as e:
            log_erro("Erro de conexão", e)
        time.sleep(2)
    return None


def handle_request_errors(response, error_message, details=None):
    if response is None or response.status_code >= 400:
        return (
            jsonify(
                {
                    "error": error_message,
                    "details": (
                        details or response.text if response else "Nenhuma resposta"
                    ),
                }
            ),
            400,
        )


@app.route("/update-plan-desktop/<string:entity_id>", methods=["POST"])
def update_plan_desktop(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_desktop(
            cidade_completa, entity_id
        )
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@app.route("/update-plan-giga/<string:entity_id>", methods=["POST"])
def update_plan_giga(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_giga(cidade_completa, entity_id)
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@app.route("/update-plan-vero/<string:entity_id>", methods=["POST"])
def update_plan_vero(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_vero(cidade_completa, entity_id)
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@app.route("/update-plan-blfibra/<string:entity_id>", methods=["POST"])
def update_plan_blfibra(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_blfibra(
            cidade_completa, entity_id
        )
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@app.route("/update-plan-master/<string:entity_id>", methods=["POST"])
def update_plan_master(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_master(cidade_completa, entity_id)
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@app.route("/update-plan-oi/<string:entity_id>", methods=["POST", "GET"])
def update_plan_oi(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_oi(cidade_completa, entity_id)
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@app.route("/update-plan-implantar/<string:entity_id>", methods=["POST"])
def update_plan_implantar(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_implantar(
            cidade_completa, entity_id
        )
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(port=1421, host="0.0.0.0")
