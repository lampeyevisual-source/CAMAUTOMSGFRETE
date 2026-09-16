from playwright.sync_api import sync_playwright

# =========================
# CONTAR MOTORISTAS
# =========================

def contar_motoristas(page):

    try:

        print("\nContando motoristas...")

        # Aguarda a lista aparecer
        lista = page.locator(
            '[data-testid="suggested-trucker-list"]'
        )

        lista.wait_for(
            state="visible",
            timeout=15000
        )

        # Conta os LI que representam os motoristas
        cards_motoristas = lista.locator(
            '[data-testid="trucker-list-item"]'
        )

        quantidade = cards_motoristas.count()

        print(
            f"Motoristas encontrados: {quantidade}"
        )

        return quantidade

    except Exception as erro:

        print("\nErro ao contar motoristas:")
        print(erro)

        return 0
    
def selecionar_todos_motoristas(page):

    try:

        print("\nSelecionando todos os motoristas...")

        checkbox_todos = page.locator(
            "[data-testid='list-header'] label.fuel-checkbox-label"
        )

        if checkbox_todos.count() == 0:

            print("Nenhum motorista encontrado.")

            page.go_back()

            return False

        checkbox_todos.scroll_into_view_if_needed()

        checkbox_todos.click(force=True)

        page.wait_for_timeout(2000)

        print("Todos os motoristas selecionados!")

        return True

    except Exception as erro:

        print(erro)

        page.go_back()

        return False        
    
# =========================
# ABRIR CHAT (ENVIO FINAL)
# =========================

def abrir_chat_envio(page):

    try:

        print("\nAbrindo chat de envio...")

        page.wait_for_timeout(3000)

        botao_chat = page.locator(
            "button[data-testid='share-freight']"
        ).first

        botao_chat.wait_for(
            state="visible",
            timeout=15000
        )

        botao_chat.scroll_into_view_if_needed()

        botao_chat.click(force=True)

        page.wait_for_timeout(5000)

        print("Chat aberto com sucesso!")

    except Exception as erro:

        print("\nErro ao abrir chat:")

        print(erro)

        page.go_back()

# =========================
# CLICAR EM COMPARTILHAR
# =========================

# =========================
# CLICAR EM COMPARTILHAR
# =========================

def enviar_chat_compartilhar(page):

    try:

        print("\nAguardando 5 segundos antes de clicar em Compartilhar...")
        
        # =========================
        # 1. PREENCHER TEXTO
        # =========================r
        campo_texto = page.locator("textarea.fuel-textarea__input").first
    
        campo_texto.wait_for(
            state="visible",
            timeout=10000
        )

        campo_texto.click(force=True)

        page.wait_for_timeout(500)

        campo_texto.fill(".")
        campo_texto.press("Tab")
        

        print("Mensagem preenchida!")

        page.wait_for_timeout(5000)

        # Localiza EXATAMENTE o botão mostrado no HTML
        botao_compartilhar = page.locator(
            'button.fuel-button.fuel-button--primary.fuel-button--large'
            '[aria-label="Compartilhar"]'
            '[data-variant="primary"]'
            '[data-size="large"]'
            '[data-icon-only="false"]'
        )

        quantidade = botao_compartilhar.count()

        print(f"Botões compatíveis encontrados: {quantidade}")

        if quantidade == 0:
            print("ERRO: botão Compartilhar não encontrado.")
            return False

        # Se houver mais de um, procura o visível
        for i in range(quantidade):

            botao = botao_compartilhar.nth(i)

            if not botao.is_visible():
                print(f"Botão #{i} não está visível.")
                continue

            print(f"Botão Compartilhar #{i} encontrado e visível.")

            botao.scroll_into_view_if_needed()

            page.wait_for_timeout(500)

            # Verifica se está habilitado
            if not botao.is_enabled():
                print(f"Botão #{i} está desabilitado.")
                continue

            print(f"Clicando no botão Compartilhar #{i}...")

            botao.click(
                force=True,
                timeout=10000
            )

            print("Compartilhar clicado com sucesso!")

            return True

        print("Nenhum botão Compartilhar visível/habilitado encontrado.")

        return False

    except Exception as erro:

        print("\nErro ao clicar em Compartilhar:")
        print(erro)

        return False