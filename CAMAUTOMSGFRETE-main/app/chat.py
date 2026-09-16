from playwright.sync_api import sync_playwright


# =====================================
# ABRIR CHAT
# =====================================

def abrir_chat():

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

    page.goto(
        "https://novacentral.fretebras.com.br/chat",
        wait_until="domcontentloaded",
        timeout=120000
    )

    page.wait_for_timeout(5000)

    print("\nChat carregado!")

    return playwright, context, page


# =====================================
# CAPTURAR FRETES
# =====================================

def iniciar_chat(page):

    