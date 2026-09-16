from fretebras import abrir_fretebras, capturar_fretes
from replicador import (
    abrir_replicador,
    preencher_origem,
    preencher_destino,
    clicar_negociador,
    preencher_produto,
    preencher_carga,
    preencher_lote,
    preencher_caminhao,
    preencher_carroceria,
    preencher_pagamento,
    preencher_final,
    preencher_publicar
)
from mensagem import(
    contar_motoristas,
    selecionar_todos_motoristas,
    abrir_chat_envio,
    enviar_chat_compartilhar
    
)

import os
import random
import time
import re



# =========================
# PASTA / ARQUIVO
# =========================

PASTA_DATA = "data"

ARQUIVO_PROCESSADOS = (
    f"{PASTA_DATA}/processados.txt"
)

os.makedirs(
    PASTA_DATA,
    exist_ok=True
)


# =========================
# TIMER
# =========================

def iniciar_timer():

    return time.time()


def finalizar_timer(
    nome_acao,
    inicio
):

    tempo = round(
        time.time() - inicio,
        2
    )

    print(
        f"[TEMPO] {nome_acao}: {tempo}s"
    )


# =========================
# CARREGA PROCESSADOS
# =========================

def carregar_processados():

    try:

        with open(
            ARQUIVO_PROCESSADOS,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return set(

                linha.strip()

                for linha in arquivo.readlines()

            )

    except:

        return set()

# =========================
# SALVA PROCESSADO
# =========================
def salvar_processado(frete_id):

    with open(
        ARQUIVO_PROCESSADOS,
        "a",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(f"{frete_id}\n")
        arquivo.flush()
        os.fsync(arquivo.fileno())
# =========================
# USUÁRIO
# =========================

def abrir_login(page):

    campo_usuario = page.locator(
        "#username"
    )

    campo_usuario.wait_for(
        state="visible",
        timeout=4000
    )

    campo_usuario.click()

    campo_usuario.fill(
        "contact.camgroup@gmail.com"
    )

    print(
        "Usuário preenchido."
    )

    # =========================
    # SENHA
    # =========================

    campo_senha = page.locator(
        "#password"
    )

    campo_senha.wait_for(
        state="visible",
        timeout=4000
    )

    campo_senha.click()

    campo_senha.fill(
        "Lhm@4856"
    )

    print(
        "Senha preenchida."
    )

    # =========================
    # SENHA
    # =========================

    campo_entrar = page.locator(
        "#kc-content-wrapper > div > section > div > div > form > button > span.fuel-button__content"
    )

    campo_entrar.wait_for(
        state="visible",
        timeout=4000
    )

    campo_entrar.click()

    print(
        "Acesso Iniciado."
    )

    page.wait_for_timeout(40000)


# =========================
# ESTADO
# =========================

estado = input(
    "\nDigite o estado (MT, GO, SP, PR...): "
).strip().lower()

# =========================
# MAIN
# =========================

def main():


   # =========================
# ABRE FRETEBRAS
# =========================

    inicio_sistema = iniciar_timer()

    playwright, context, page = abrir_fretebras(
        estado
    )

    finalizar_timer(
        "Abrir Fretebras",
        inicio_sistema
    )

    # Variável global do ciclo
    pagina_atual = 1
    total_paginas = 1

    indice_card = 0

    # =========================
    # CONTADOR
    # =========================

    fretes_processados = 0

    # =========================
    # LOOP PRINCIPAL
    # =========================

    while True:

        ciclo_inicio = iniciar_timer()

        try:

            print("\n===================================")
            print("NOVO CICLO")
            print("===================================\n")

            # =========================
            # ATUALIZA FRETES
            # =========================

            etapa_inicio = iniciar_timer()

            # =========================
            # DEFINE URL
            # =========================

            if pagina_atual == 1:

                url = (
                    f"https://www.fretebras.com.br/fretes/carga-de-{estado}/carroceria-cacamba"
                )

            else:

                url = (
                    f"https://www.fretebras.com.br/fretes/carga-de-{estado}/carroceria-cacamba/{pagina_atual}"
                )

            print(
                f"Página atual: {pagina_atual}"
            )

            # =========================
            # ACESSA PÁGINA
            # =========================

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            try:

                elemento = page.locator("p").filter(
                    has_text="páginas"
                ).first

                print(
                    "Quantidade encontrada:",
                    elemento.count()
                )

                texto_paginas = elemento.inner_text()

                match = re.search(
                    r"de\s+(\d+)\s+páginas",
                    texto_paginas
                )
                if match:

                    total_paginas = int(
                        match.group(1)
                    )

                    print(
                        f"Total de páginas: {total_paginas}"
                    )

            except Exception as e:

                print(
                    f"Erro ao capturar total de páginas: {e}"
                )
                
            finalizar_timer(
                "Atualizar fretes",
                etapa_inicio
            )
            # =========================
            # PROCESSADOS
            # =========================

            processados = carregar_processados()

            print(

                f"\nProcessados carregados: "
                f"{len(processados)}"

            )
            # =========================
            # TOTAL DE FRETES
            # =========================

            cards = page.locator(
                "section"
            ).all()

            total_cards = len(cards)

            print(
                f"\nTotal de cards na página: "
                f"{total_cards}"
            )

            # =========================
            # VERIFICA TROCA DE PÁGINA
            # =========================

            if indice_card >= total_cards:

                indice_card = 0
                pagina_atual += 1

                if pagina_atual > total_paginas:
                    pagina_atual = 1

                print(f"\nIndo para a página {pagina_atual}")

            
            # =========================
            # CAPTURA FRETE
            # =========================

            etapa_inicio = iniciar_timer()

            frete = capturar_fretes(page, indice_card)

            finalizar_timer(
                "Capturar fretes",
                etapa_inicio
            )

            if frete is None:
                indice_card += 1
                continue


            # =========================
            # CRIA ID
            # =========================

            frete_id = frete["origem"]

            # =========================
            # VERIFICA DUPLICADO
            # =========================

            if frete_id in processados:

                print(f"\nOrigem já processada: {frete_id}")

                indice_card += 1
                continue    
                
            # =========================
            # IGNORA ORIGEM GOIÂNIA
            # =========================

            try:

                origem = (
                    frete["origem"]
                    .strip()
                    .lower()
                    .replace("â", "a")
                )

                if "goiania" in origem:

                    print("\nIgnorando frete de Goiânia:")
                    print(frete["origem"])

                    indice_card += 1
                    continue

                origem = (
                    frete["origem"]
                    .strip()
                    .lower()
                    .replace("á", "a")
                )

                if "Santa Maria de Jetiba" in origem:

                    print("\nIgnorando frete de Goiânia:")
                    print(frete["origem"])

                    indice_card += 1
                    continue

            except Exception as e:

                print(f"\nErro ao verificar origem: {e}")

                indice_card += 1
                continue

            # =========================
            # FRETE VÁLIDO
            # =========================

            print(
                f"\nFrete válido: {frete['origem']} -> {frete['destino']}"
            )


            # =========================
            # NOVO FRETE ENCONTRADO
            # =========================

            print("\nNOVO FRETE ENCONTRADO")
            print("========================")

            print(f"Origem : {frete['origem']}")
            print(f"Destino: {frete['destino']}")
            
    
            # =========================
            # SALVA PROCESSADO
            # =========================

            print("\nSalvando frete...")

            try:

                print(f"ID do frete: {frete_id}")

                salvar_processado(frete_id)

                processados.add(frete_id)

                fretes_processados += 1

                print("Frete salvo com sucesso.")

                # =========================
                # PAUSA A CADA 10 FRETES
                # =========================

                if fretes_processados >= 5:

                    print("\nForam processados 10 fretes.")
                    print("Aguardando 5 minutos para continuar...")

                    time.sleep(300)  # 5 minutos

                    fretes_processados = 0

                    print("Retomando processamento...")

            except Exception as e:

                print(f"ERRO AO SALVAR: {e}")

            print(f"\nTOTAL PROCESSADOS: {fretes_processados}")

        
            # =========================
            # ABRIR LOGIN
            # =========================

            page.goto(
                "https://novacentral.fretebras.com.br/meus-fretes",
                wait_until="domcontentloaded",
                timeout=120000
            )

            print("\nReplicador carregado!")

            page.wait_for_timeout(4000)

            inicio_login = iniciar_timer()

            campo_usuario = page.locator("#username")

            if campo_usuario.count() > 0:

                print("Tela de login encontrada.")

                abrir_login(
                    page
                )

            else:

                print("Usuário já está logado.")

            finalizar_timer(
                "Abrir Login",
                inicio_login
            )

            time.sleep(15)


            # =========================
            # ABRIR REPLICADOR
            # =========================

            inicio_replicador = iniciar_timer()

            resultado = abrir_replicador(
                page
            )
            if not resultado:
                continue

            finalizar_timer(
                "Abrir Replicador",
                inicio_replicador
            )   

            # =========================
            # PREENCHER ORIGEM
            # =========================

            inicio_origem = iniciar_timer()

            resultado = preencher_origem(
                page,
                frete
            )
            if not resultado:
                continue
            finalizar_timer(
                "Preencher Origem",
                inicio_origem
            )
            page.wait_for_timeout(4000)

            # =========================
            # PREENCHER DESTINO
            # =========================

            inicio_destino = iniciar_timer()

            resultado = preencher_destino(
                page,
                frete
            )
            if not resultado:
                continue
            finalizar_timer(
                "Preencher Destino",
                inicio_destino
            )
            page.wait_for_timeout(4000)

            # =========================
            # PREENCHER
            # =========================

            inicio_negociador = iniciar_timer()

            resultado = clicar_negociador(
                page
            )
            if not resultado:
                continue
            finalizar_timer(
                "Preencher Negociador",
                inicio_negociador
            )
            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            resultado = preencher_produto(
                page
            )
          
            if not resultado:
                continue
            finalizar_timer(
                "Preencher Produto",
                inicio_destino
            )
            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            resultado = preencher_carga(
                page
            )

            if not resultado:
                continue

            finalizar_timer(
                "Preencher Carga",
                inicio_destino
            )
            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            resultado = preencher_lote(
                page
            )

            if not resultado:
                continue

            finalizar_timer(
                "Preencher Lote",
                inicio_destino
            )   
            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            resultado = preencher_caminhao(
                page
            )

            if not resultado:
                continue
    
            finalizar_timer(
                "Preencher Caminhão",
                inicio_destino
            )

            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            resultado = preencher_carroceria(page)

            if not resultado:

                continue

            finalizar_timer(
                "Preencher Carroceria",
                inicio_destino
            )

            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            preencher_pagamento(
                page        
            )

            finalizar_timer(
                "Preencher Pagamento",
                inicio_destino
            )

            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            preencher_final(
                page        
            )

            finalizar_timer(
                "Preencher Final",
                inicio_destino
            )

            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            preencher_publicar(
                page        
            )

            finalizar_timer(
                "Preencher Publicar",
                inicio_destino
            )

            page.wait_for_timeout(3000)
            # =========================
            # ABRIR MOTORISTAS SUGERIDOS
            # =========================

            inicio_motoristas = iniciar_timer()

            try:

                page.goto(
                    "https://novacentral.fretebras.com.br/meus-fretes",
                    wait_until="domcontentloaded",
                    timeout=120000
                )
                page.wait_for_timeout(30000)

                origem = frete["origem"]

                print(
                    f"\nProcurando frete publicado: {origem}"
                )

                frete_encontrado = False

                for tentativa in range(10):

                    try:

                        page.wait_for_timeout(6000)

                        # Procura todos os elementos que possuem exatamente o texto da origem
                        origens = page.get_by_text(origem, exact=True)

                        total = origens.count()

                        print(f"Foram encontradas {total} ocorrências da origem.")

                        for i in range(total):

                            origem_elemento = origens.nth(i)

                            try:

                                # Sobe até o primeiro ancestral que possui o botão
                                card = origem_elemento.locator(
                                    "xpath=ancestor::*[.//button[@data-testid='suggested-trucker-list-item-beta']][1]"
                                )

                                botao = card.locator(
                                    '[data-testid="suggested-trucker-list-item-beta"]'
                                )

                                if botao.count() == 0:
                                    continue

                                print(f"Frete localizado: {origem}")

                                botao.click(force=True)

                                page.wait_for_timeout(3000)

                                print("Motoristas sugeridos aberto!")

                                frete_encontrado = True

                                break

                            except Exception:
                                continue

                        if frete_encontrado:
                            break

                    except Exception as erro:

                        print(f"Erro na tentativa {tentativa+1}: {erro}")

                    print(f"Tentativa {tentativa+1}/10")

                    page.reload(wait_until="domcontentloaded")
            except Exception as erro:

                print("\nErro ao abrir motoristas sugeridos:")
                print(erro)

            finalizar_timer(
                "Abrir Motoristas Sugeridos",
                inicio_motoristas
            )
            # =========================
            # CONTAR MOTORISTAS
            # =========================

            inicio_motoristas = iniciar_timer()

            contar_motoristas(
                page
            )

            finalizar_timer(
                "Contar Motoristas",
                inicio_motoristas
            )
            
            # =========================
            # SELECIONAR MOTORISTAS
            # =========================

            inicio_selecionar_motoristas = iniciar_timer()

            selecionar_todos_motoristas(
                page
            )

            finalizar_timer(
                "Selecionar Motoristas",
                inicio_selecionar_motoristas
            )

            # =========================
            # ABRIR CHAT
            # =========================

            abrir_chats= iniciar_timer()

            abrir_chat_envio(
                page
            )

            finalizar_timer(
                "Chat Aberto",
                abrir_chats
            )

            # =========================
            # ABRIR CHAT
            # =========================

            chat_enviar= iniciar_timer()

            enviar_chat_compartilhar(
                page
            )

            finalizar_timer(
                "Chat Enviado",
                chat_enviar
            )

            # =======================
            # AGUARDAR ANTES DO PRÓXIMO PROCESSO
            # =========================

            tempo_espera = random.randint(60, 120)

            print(f"\nAguardando {tempo_espera} segundos para iniciar um novo processo...")

            time.sleep(tempo_espera)

        except Exception as erro_geral:

            print("\nERRO GERAL:")

            print(erro_geral)

            page

            time.sleep(10)

        print("\nTodos os cards da página foram analisados.")

        indice_card = 0

        if pagina_atual < total_paginas:

            pagina_atual += 1

            print(f"Indo para página {pagina_atual}")

        else:

            pagina_atual = 1

            print("Voltando para página 1")

        continue
if __name__ == "__main__":
    main()