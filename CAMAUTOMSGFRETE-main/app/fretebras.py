from playwright.sync_api import sync_playwright


# =====================================
# ABRIR FRETEBRAS
# =====================================

def abrir_fretebras(estado):

    playwright = sync_playwright().start()

    context = playwright.chromium.launch_persistent_context(
        user_data_dir="perfil",
        headless=False,

        args=[
            "--start-maximized",
            "--disable-blink-features=AutomationControlled"
        ],

        no_viewport=True
    )

    page = (
        context.pages[0]
        if context.pages
        else context.new_page()
    )

    url = (
            f"https://www.fretebras.com.br/fretes/"
            f"carga-de-{estado}/"
            f"carroceria-cacamba"
        )

    print(f"\nURL gerada: {url}")

    print(
        f"\nBuscando fretes de {estado.upper()}"
    )

    page.wait_for_timeout(5000)

    print(
        f"\nFretebras carregado para {estado.upper()}!"
    )

    return playwright, context, page


# =====================================
# CAPTURAR FRETE
# =====================================

def capturar_fretes(page, indice_card):

    print("\nClassificando fretes...")

    # =====================================
    # CAPTURA DOS CARDS
    # =====================================

    print("\nCapturando cards...")

    cards = page.locator("section").all()

    print(f"\nFretes encontrados: {len(cards)}")

    # =====================================
    # VERIFICA LIMITE
    # =====================================

    if indice_card >= len(cards):

        return None

    try:

        card = cards[indice_card]

        cidades = card.locator(
            "h2"
        ).all_text_contents()

        print("\n====================")

        if len(cidades) >= 2:

            origem = cidades[0]

            destino = cidades[1]

            print(
                "Origem:",
                origem
            )

            print(
                "Destino:",
                destino
            )

            return {

                "origem": origem,

                "destino": destino

            }

    except Exception as e:

        print(
            "\nErro ao capturar frete:"
        )

        print(e)

    return None

# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    playwright, context, page = abrir_fretebras()

    fretes = capturar_fretes(page)

    print("\n====================================")
    print("FRETES CAPTURADOS")
    print("====================================")

    for i, frete in enumerate(fretes, start=1):

        print(f"\nFRETE {i}")

        print(
            f"Origem : {frete['origem']}"
        )

        print(
            f"Destino: {frete['destino']}"
        )


    input("\nPressione ENTER para fechar...")

    context.close()

    playwright.stop()