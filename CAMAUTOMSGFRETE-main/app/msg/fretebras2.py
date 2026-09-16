from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import csv
import os
import random
import re
import time
from datetime import datetime

# ============================================================
# CONFIGURAÇÕES
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CAMINHO_CSV = os.path.join(BASE_DIR, "contatosfrete.csv")
PASTA_MENSAGENS = os.path.join(BASE_DIR, "mensagens")

URL_CHAT = "https://novacentral.fretebras.com.br/chat"

TEMPO_MINIMO_ENTRE_ENVIOS = 140  # minutos
TEMPO_ENTRE_TENTATIVAS = 6       # segundos
TEMPO_APOS_RECARREGAR = 8        # segundos
TEMPO_APOS_ABRIR_CHAT = 2        # segundos

mensagens = []


# ============================================================
# UTILIDADES
# ============================================================

def recarregar_chat(page, espera=TEMPO_APOS_RECARREGAR):
    """Reabre o chat e espera a lista de cards carregar."""
    print("\nRecarregando lista do Fretebras...")

    try:
        page.goto(
            URL_CHAT,
            wait_until="domcontentloaded",
            timeout=120000
        )
        page.wait_for_timeout(espera * 1000)
        return True

    except Exception as erro:
        print("Erro ao recarregar Fretebras:", erro)
        return False


def esperar_cards(page, timeout=15000):
    """Espera a lista de chats aparecer."""
    try:
        page.locator(
            "button[data-testid='channel-preview-id']"
        ).first.wait_for(
            state="visible",
            timeout=timeout
        )
        return True

    except Exception:
        return False

# ============================================================
# LOGIN
# ============================================================

def logar_fretebras(page):
    """
    Abre o Fretebras, faz o login quando necessário e confirma o login
    somente quando o navegador realmente volta para o domínio da Central.
    """

    print("\nAbrindo Fretebras...")

    try:
        page.goto(
            URL_CHAT,
            wait_until="domcontentloaded",
            timeout=120000
        )
    except Exception as erro:
        print("\n❌ Erro ao abrir o Fretebras:")
        print(erro)
        return False

    page.wait_for_timeout(3000)

    campo_usuario = page.locator("#username")

    # ========================================================
    # VERIFICAR SE PRECISA FAZER LOGIN
    # ========================================================

    try:
        precisa_login = campo_usuario.count() > 0 and campo_usuario.first.is_visible()
    except Exception:
        precisa_login = False

    if precisa_login:
        print("\nTela de login encontrada.")

        try:
            campo_usuario.first.wait_for(
                state="visible",
                timeout=10000
            )
            campo_usuario.first.fill("contact.camgroup@gmail.com")

            campo_senha = page.locator("#password")
            campo_senha.first.wait_for(
                state="visible",
                timeout=10000
            )
            campo_senha.first.fill("Lhm@4856")

            print("Usuário e senha preenchidos.")

            botao = page.locator(
                "#kc-content-wrapper > div > section > div > div > form > button"
            )

            botao.first.wait_for(
                state="visible",
                timeout=10000
            )

            print("Clicando em entrar...")
            botao.first.click()

        except Exception as erro:
            print("\n❌ Erro ao preencher/enviar login:")
            print(erro)
            print("URL atual:", page.url)
            return False

        # ====================================================
        # CONFIRMAÇÃO REAL DO LOGIN
        # ====================================================
        #
        # NÃO usamos mais:
        #     "#username desapareceu = login confirmado"
        #
        # Durante o SSO o #username pode desaparecer
        # temporariamente. O que confirma é o retorno ao
        # domínio da Central do Fretebras.
        # ====================================================

        print("Aguardando retorno do login...")

        login_confirmado = False

        try:
            page.wait_for_url(
                re.compile(r"^https://novacentral\.fretebras\.com\.br/"),
                timeout=60000
            )
            login_confirmado = True

        except PlaywrightTimeoutError:
            login_confirmado = False

        # Dá alguns segundos para o callback terminar.
        if login_confirmado:
            page.wait_for_timeout(3000)

        if not login_confirmado:
            print("\n❌ LOGIN NÃO CONFIRMADO.")
            print("O navegador não voltou para a Central do Fretebras.")
            print("URL atual:", page.url)
            return False

        # Se voltou para a Central, ainda verificamos se o login
        # não foi redirecionado novamente para o SSO.
        if "sso-external.fretebras.com.br" in page.url:
            print("\n❌ LOGIN NÃO CONFIRMADO.")
            print("O Fretebras ainda está no SSO.")
            print("URL atual:", page.url)
            return False

        print("\n✅ LOGIN CONFIRMADO!")

    else:
        # Pode existir uma sessão já autenticada.
        if "sso-external.fretebras.com.br" in page.url:
            print("\n❌ Página de SSO encontrada, mas não há sessão autenticada.")
            print("URL atual:", page.url)
            return False

        print("\nUsuário já está logado.")

    # ========================================================
    # ABRIR CHAT DEPOIS DO LOGIN
    # ========================================================

    print("\nAbrindo chat...")

    try:
        page.goto(
            URL_CHAT,
            wait_until="domcontentloaded",
            timeout=120000
        )

        page.wait_for_timeout(5000)

    except Exception as erro:
        print("\n❌ Erro ao abrir o chat:")
        print(erro)
        print("URL atual:", page.url)
        return False

    # ========================================================
    # VERIFICAR SE VOLTOU PARA O LOGIN
    # ========================================================

    if "sso-external.fretebras.com.br" in page.url:
        print("\n❌ ATENÇÃO: Fretebras voltou para a tela de login.")
        print("URL atual:", page.url)
        return False

    try:
        campo_login = page.locator("#username")

        if campo_login.count() > 0 and campo_login.first.is_visible():
            print("\n❌ ATENÇÃO: Fretebras voltou para a tela de login.")
            print("URL atual:", page.url)
            return False

    except Exception:
        pass

    # Espera a aplicação terminar de carregar.
    print("\n✅ Chat aberto.")
    page.wait_for_timeout(5000)

    return True


# ============================================================
# CSV
# ============================================================

def buscar_contato_csv(id_motorista):
    try:
        if not os.path.exists(CAMINHO_CSV):
            print("CSV não encontrado:", CAMINHO_CSV)
            return None

        with open(
            CAMINHO_CSV,
            "r",
            encoding="utf-8",
            newline=""
        ) as arquivo:

            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                if linha.get("id") == id_motorista:
                    return linha

        return None

    except Exception as erro:
        print("Erro CSV:", erro)
        return None


def atualizar_csv(id_motorista, nome="", ddd=""):
    linhas = []
    encontrado = False

    try:
        if os.path.exists(CAMINHO_CSV):
            with open(
                CAMINHO_CSV,
                "r",
                encoding="utf-8",
                newline=""
            ) as arquivo:

                leitor = csv.DictReader(arquivo)

                for linha in leitor:

                    if linha.get("id") == id_motorista:
                        encontrado = True

                        linha["data_envio"] = datetime.now().strftime(
                            "%d/%m/%Y %H:%M"
                        )

                        try:
                            quantidade = int(
                                linha.get("quantidade_envios") or 0
                            )
                        except ValueError:
                            quantidade = 0

                        linha["quantidade_envios"] = str(
                            quantidade + 1
                        )

                    linhas.append(linha)

        if not encontrado:
            linhas.append({
                "id": id_motorista,
                "nome": nome,
                "ddd": ddd,
                "data_envio": datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                ),
                "quantidade_envios": "1"
            })

        os.makedirs(os.path.dirname(CAMINHO_CSV), exist_ok=True)

        with open(
            CAMINHO_CSV,
            "w",
            newline="",
            encoding="utf-8"
        ) as arquivo:

            campos = [
                "id",
                "nome",
                "ddd",
                "data_envio",
                "quantidade_envios"
            ]

            escritor = csv.DictWriter(
                arquivo,
                fieldnames=campos
            )

            escritor.writeheader()
            escritor.writerows(linhas)

        print("CSV atualizado:", id_motorista)
        return True

    except Exception as erro:
        print("Erro ao atualizar CSV:", erro)
        return False


# ============================================================
# MENSAGENS
# ============================================================

def carregar_mensagens(nome_arquivo="atrasi.txt"):
    global mensagens

    arquivo = os.path.join(
        PASTA_MENSAGENS,
        nome_arquivo
    )

    try:
        with open(
            arquivo,
            "r",
            encoding="utf-8"
        ) as f:
            conteudo = f.read()

        mensagens = [
            mensagem.strip()
            for mensagem in conteudo.split("###")
            if mensagem.strip()
        ]

        print(f"{len(mensagens)} mensagens carregadas.")
        return True

    except Exception as erro:
        print("Erro carregando mensagens:", erro)
        mensagens = []
        return False


def pegar_mensagem():
    if not mensagens:
        return None

    return random.choice(mensagens)


# ============================================================
# CONTROLE DE ENVIO
# ============================================================

def verificar_envio(contato):

    # Contato novo
    if contato is None:
        print("Contato novo. Liberado para envio.")
        return True

    try:
        data_ultimo_envio = datetime.strptime(
            contato["data_envio"],
            "%d/%m/%Y %H:%M"
        )

        agora = datetime.now()

        diferenca = (
            agora - data_ultimo_envio
        ).total_seconds() / 20

        print(
            f"Último envio há {int(diferenca)} minutos"
        )

        if diferenca >= TEMPO_MINIMO_ENTRE_ENVIOS:
            print("Liberado para envio.")
            return True

        print("Contato ainda não liberado.")
        return False

    except Exception as erro:
        print("Erro verificando data:", erro)

        # Mantém o comportamento do código original:
        # se não conseguir interpretar a data, libera.
        return True


# ============================================================
# CHAT
# ============================================================

def abrir_chat(card):
    try:
        card.scroll_into_view_if_needed()

        card.wait_for(
            state="visible",
            timeout=5000
        )

        card.click()

        print("Chat aberto!")

        return True

    except Exception as erro:
        print("Erro ao abrir chat:", erro)
        return False


def escrever_mensagem(page):

    try:
        mensagem = pegar_mensagem()

        if not mensagem:
            print("Nenhuma mensagem disponível.")
            return False

        caixa = page.locator(
            "textarea[data-testid='message-input']"
        )

        if caixa.count() == 0:
            print("Chat sem caixa de mensagem. Pulando...")
            return False

        caixa.first.wait_for(
            state="visible",
            timeout=5000
        )

        caixa.first.click()
        page.wait_for_timeout(500)

        caixa.first.fill(mensagem)
        page.wait_for_timeout(500)

        caixa.first.press("Enter")

        print("Mensagem enviada!")

        return True

    except Exception as erro:
        print(
            "Não foi possível enviar a mensagem. "
            "Pulando para o próximo chat."
        )
        print(erro)
        return False


# ============================================================
# IDENTIFICAR MOTORISTA
# ============================================================

def obter_dados_card(card):

    nome = ""
    ddd = ""
    id_motorista = None

    texto = card.inner_text()

    try:
        nome = (
            card
            .locator("p")
            .first
            .inner_text()
            .strip()
        )
    except Exception:
        nome = ""

    if "DDD:" in texto:
        try:
            ddd = (
                texto
                .split("DDD:", 1)[1]
                .split("\n", 1)[0]
                .strip()
            )
        except Exception:
            ddd = ""

    imagem = card.locator("img").get_attribute("src")

    if not imagem:
        return None

    if "/truckers/" not in imagem:
        print("Chat diferente encontrado.")
        print("Pulando este card...")
        return None

    try:
        id_motorista = (
            imagem
            .split("/truckers/", 1)[1]
            .split("/", 1)[0]
        )
    except Exception:
        return None

    return {
        "nome": nome,
        "ddd": ddd,
        "id": id_motorista
    }


# ============================================================
# PROCESSAR UM CARD
# ============================================================

def processar_card(page, indice):

    try:
        # IMPORTANTE:
        # O locator é recriado a cada tentativa.
        # Isso evita usar um elemento antigo depois que a página muda.
        cards = page.locator(
            "button[data-testid='channel-preview-id']"
        )

        quantidade = cards.count()

        if indice >= quantidade:
            return "fim"

        card = cards.nth(indice)

        dados = obter_dados_card(card)

        if not dados:
            return "ignorar"

        nome = dados["nome"]
        ddd = dados["ddd"]
        id_motorista = dados["id"]

        print("\n-----------------------------------")
        print(f"Card: {indice + 1}/{quantidade}")
        print(f"Nome: {nome}")
        print(f"ID: {id_motorista}")
        print("-----------------------------------")

        contato = buscar_contato_csv(id_motorista)

        if not verificar_envio(contato):
            return "ignorar"

        if not abrir_chat(card):
            return "erro"

        page.wait_for_timeout(
            TEMPO_APOS_ABRIR_CHAT * 1000
        )

        if not escrever_mensagem(page):
            return "erro"

        atualizar_csv(
            id_motorista,
            nome,
            ddd
        )

        print("Envio concluído.")

        return "enviado"

    except PlaywrightTimeoutError as erro:
        print("Timeout no card:", erro)
        return "erro"

    except Exception as erro:
        print("\nErro no processamento do card:")
        print(erro)
        return "erro"


# ============================================================
# LOOP PRINCIPAL
# ============================================================

def analisar_cards(page):

    print("\n======================================")
    print("AUTOMAÇÃO EM LOOP CONTÍNUO")
    print("======================================")

    carregar_mensagens("atrasi.txt")

    contador_ciclos = 0

    while True:

        contador_ciclos += 1

        print("\n")
        print("======================================")
        print(f"NOVO CICLO: {contador_ciclos}")
        print("======================================")

        # ----------------------------------------------------
        # GARANTIR QUE OS CARDS EXISTEM
        # ----------------------------------------------------

        if not esperar_cards(page):

            print("Nenhum card carregado.")

            if not recarregar_chat(page):
                print(
                    f"Falha ao recarregar. "
                    f"Tentando novamente em {TEMPO_ENTRE_TENTATIVAS}s..."
                )

                time.sleep(TEMPO_ENTRE_TENTATIVAS)

            continue

        # ----------------------------------------------------
        # PROCESSAR OS CARDS
        # ----------------------------------------------------

        indice = 0
        houve_envio = False
        houve_erro = False

        while True:

            cards = page.locator(
                "button[data-testid='channel-preview-id']"
            )

            quantidade = cards.count()

            print(
                f"\nCards disponíveis neste momento: {quantidade}"
            )

            if quantidade == 0:
                break

            if indice >= quantidade:
                break

            resultado = processar_card(
                page,
                indice
            )

            # ------------------------------------------------
            # ENVIOU
            # ------------------------------------------------

            if resultado == "enviado":

                houve_envio = True

                print(
                    "\nMensagem enviada."
                    "\nRecarregando lista antes de continuar..."
                )

                recarregar_chat(page)

                # NÃO incrementa o índice.
                # Depois do reload, o primeiro card pode ter
                # mudado de posição.
                indice = 0

                continue

            # ------------------------------------------------
            # ERRO
            # ------------------------------------------------

            if resultado == "erro":

                houve_erro = True

                print(
                    "\nErro neste card."
                    "\nRecarregando a página e retomando o loop..."
                )

                if not recarregar_chat(page):
                    time.sleep(TEMPO_ENTRE_TENTATIVAS)

                # Volta para o início porque os cards podem
                # ter sido recriados pelo navegador.
                indice = 0

                continue

            # ------------------------------------------------
            # IGNORAR
            # ------------------------------------------------

            if resultado == "ignorar":

                indice += 1
                continue

            # ------------------------------------------------
            # FIM
            # ------------------------------------------------

            if resultado == "fim":
                break

        # ----------------------------------------------------
        # FINAL DO CICLO
        # ----------------------------------------------------

        print("\n======================================")
        print(f"CICLO {contador_ciclos} FINALIZADO")
        print(f"Houve envio: {houve_envio}")
        print(f"Houve erro: {houve_erro}")
        print("======================================")

        # Sempre recarrega e começa outro ciclo.
        # Isso é o que mantém a automação realmente contínua.
        print(
            f"\nAguardando {TEMPO_ENTRE_TENTATIVAS}s "
            "antes do próximo ciclo..."
        )

        time.sleep(TEMPO_ENTRE_TENTATIVAS)

        recarregar_chat(page)


# ============================================================
# INICIAR AUTOMAÇÃO
# ============================================================

if __name__ == "__main__":

    with sync_playwright() as p:

        contexto = p.chromium.launch_persistent_context(
            user_data_dir=os.path.join(BASE_DIR, "perfil"),
            headless=False,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled"
            ],
            no_viewport=True
        )

        pagina = (
            contexto.pages[0]
            if contexto.pages
            else contexto.new_page()
        )

        try:

            login_ok = logar_fretebras(pagina)

            if not login_ok:
                print(
                    "\n❌ Automação interrompida: "
                    "login não foi confirmado."
                )
            else:
                print("\nLogin confirmado. Iniciando automação...")
                analisar_cards(pagina)

        except KeyboardInterrupt:

            print("\nAutomação interrompida pelo usuário.")

        except Exception as erro:

            print("\nERRO FATAL:")
            print(erro)

        finally:

            print("\nFechando navegador...")
            contexto.close()
