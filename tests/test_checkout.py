from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

def test_flujo_compra(driver):
    driver.get("https://www.saucedemo.com/")
    
    inicio_sesion = LoginPage(driver)
    inicio_sesion.abrir_pagina().login_completo("standard_user", "secret_sauce")
    
    inventario = InventoryPage(driver)
    inventario.agregar_producto_por_nombre("Sauce Labs Backpack")
    inventario.abrir_carrito()

    carrito = CartPage(driver)
    carrito.proceder_checkout()

    checkout = CheckoutPage(driver)
    checkout.completar_informacion("Test", "User", "1234")
    checkout.finalizar_compra()

    assert checkout.obtener_mensaje_exito() == "Thank you for your order!"
