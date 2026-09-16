from playwright.sync_api import sync_playwright


# =====================================
# ABRIR REPLICADOR
# =====================================

def abrir_replicador(page):

    try:

        print(
            "\nAbrindo tela do replicador..."
        )

        page.goto(
            "https://novacentral.fretebras.com.br/meus-fretes/cadastrar",
            wait_until="domcontentloaded",
            timeout=120000
        )

        page.wait_for_timeout(3000)

        print(
            "Tela aberta com sucesso!"
        )

        return True

    except Exception as erro:

        print(
            "\nErro ao abrir tela:"
        )

        print(erro)

        return False
    
# =====================================
# PREENCHER ORIGEM
# =====================================

def preencher_origem(
    page,
    frete
):

    try:

        origem = frete["origem"]

        print(
            f"\nPreenchendo origem: "
            f"{origem}"
        )

        campo_origem = page.locator(
            "#fuel-input"
        ).nth(0)

        campo_origem.scroll_into_view_if_needed()

        campo_origem.click()

        page.wait_for_timeout(2000)

        campo_origem.fill(
            origem
        )

        page.wait_for_timeout(2000)

        page.keyboard.press(
            "Tab"
        )

        page.wait_for_timeout(2000)

        print(
            "Origem preenchida!"
        )
        return True

    except Exception as erro:

        print(
            "\nErro ao preencher origem:"
        )

        print(erro)
        return False



# =====================================
# PREENCHER DESTINO
# =====================================

def preencher_destino(
    page,
    frete
):

    try:

        # pega o SEGUNDO campo fuel-input
        campo_destino = page.locator(
            "#fuel-input"
         ).nth(1)

        
        campo_destino.click()

        page.wait_for_timeout(2000)

        campo_destino.fill(
            "Belo horizonte, MG"
        )

        page.wait_for_timeout(2000)

        page.keyboard.press(
            "Tab"
        )
        page.wait_for_timeout(2000)
        return True
       
    except Exception as erro:

        print(
            "\nErro ao preencher destino:"
        )

        print(erro)
        return False

      

# =====================================
# CLICAR NEGOCIADOR 1
# =====================================

def clicar_negociador(page):

    try:

        print("\nSelecionando Luiz C...")

        negociador = page.locator(
            "p:text-is('Luiz C')"
        ).nth(1)

        negociador.wait_for(
            state="visible",
            timeout=10000
        )

        negociador.scroll_into_view_if_needed()

        negociador.click()

        page.wait_for_timeout(2000)

        print("Luiz selecionado!")
        return True

    except Exception as erro:

        print(
            "\nErro ao selecionar negociador:"
        )

        print(erro)
        return False


# =====================================
# PREENCHER produto
# =====================================

def preencher_produto(
    page,
    
):

    try:

        campo_produto = page.locator('input[name="productName"]').first
        

        campo_produto.scroll_into_view_if_needed()


        campo_produto.click()
        page.wait_for_timeout(1000)


        campo_produto.fill(
            "Milho"
        )

        page.wait_for_timeout(1000)

        page.keyboard.press(
            "Tab"
        )

        page.wait_for_timeout(2000)

        print(
            "Produto preenchido!"
        )
        return True

    except Exception as erro:

        print(
            "\nErro ao preencher produto:"
        )

        print(erro)
        return False


# =====================================
# PREENCHER DESTINO
# =====================================

def preencher_carga(
    page
):

    try:
        campo_carga = page.locator('input[name="productTypeId"]'
        ).first

        campo_carga.click()

        page.wait_for_timeout(1000)

        page.get_by_text(
        "Granel sólido",
        exact=True
        ).click()

        page.wait_for_timeout(1000)

        page.keyboard.press(
            "Tab"
        )

        page.wait_for_timeout(2000)

        print(
            "Carga preenchida!"
        )
        return True

    except Exception as erro:

        print(
            "\nErro ao preencher carga:"
        )

        print(erro)     
        return False

# =====================================
# PREENCHER DESTINO
# =====================================

def preencher_lote(
    page
):

    try:

        campo_lote = page.locator(
        "div.fuel-switch__background"
        ).first.click(force=True)

        page.wait_for_timeout(2000)

        print(
            "Lote preenchido!"
        )
        return True

    except Exception as erro:

        print(
            "\nErro ao preencher lote:"
        )

        print(erro)
        return False

# =====================================
# PREENCHER DESTINO
# =====================================

def preencher_caminhao(
    page
):

    try:

        campo_caminhao = page.locator(
         "text=Todos os pesados"
        ).first.click(force=True)

        page.wait_for_timeout(2000)

        print(
            "Caminhão preenchido!"
        )
        return True

    except Exception as erro:

        print(
            "\nErro ao preencher caminhao:"
        )

        print(erro)
        return False
      
              

# =====================================
# PREENCHER DESTINO
# =====================================

def preencher_carroceria(
    page
):

    try:

        page.locator(
            "text=Caçamba"
        ).first.click(force=True)

        page.wait_for_timeout(1000)

        page.locator(
            "text=Graneleiro"
        ).first.click(force=True)

        page.wait_for_timeout(1000)

        print(
            "Carrocerias selecionadas!"
        )
        return True
    except Exception as erro:

        print(
            "\nErro ao preencher carroceria:"
        )

        print(erro)
        page.go_back()

        return False

# =====================================
# PREENCHER DESTINO
# =====================================

def preencher_pagamento(
    page
):

    try:

        page.locator(
        "text=A combinar"
        ).first.click(force=True)

        page.wait_for_timeout(2000)

        print("Pagamento selecionado!")
        return True

    except Exception as erro:

        print(
            "\nErro ao preencher Pagamento:"
        )

        print(erro)
        return False

# =====================================
# PREENCHER DESTINO
# =====================================

def preencher_final(
    page
):

    try:
        
        campo_final = page.locator(
            "label:has(input[name='freightTypeRadio'])"
        ).first

        campo_final.click(force=True)

        page.wait_for_timeout(10000)

        campo_final.click(force=True)

        print(
            "Final preenchido!"
        )
        return True

    except Exception as erro:

        print(
            "\nErro ao preencher final:"
        )

        print(erro)
        return False

# =====================================
# PREENCHER DESTINO
# =====================================

def preencher_publicar(
    page
):

    try:
        
        page.locator(
        "text=Publicar agora"
        ).first.click(force=True)

        page.wait_for_timeout(2000)

        print("Frete Publicado!")
        return True

    except Exception as erro:

        print(
            "\nErro ao publicar:"
        )

        print(erro)
        return False

    page.wait_for_timeout(10000)


