from selenium.webdriver.common.by import By

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.campo_nombre = (By.ID, "first-name")
        self.campo_apellido = (By.ID, "last-name")
        self.campo_codigo_postal = (By.ID, "postal-code")
        self.boton_continuar = (By.ID, "continue")
        self.boton_finalizar = (By.ID, "finish")
        self.mensaje_exito = (By.CLASS_NAME, "complete-header")

    def completar_informacion(self, nombre, apellido, codigo_postal):
        self.driver.find_element(*self.campo_nombre).send_keys(nombre)
        self.driver.find_element(*self.campo_apellido).send_keys(apellido)
        self.driver.find_element(*self.campo_codigo_postal).send_keys(codigo_postal)
        self.driver.find_element(*self.boton_continuar).click()

    def finalizar_compra(self):
        self.driver.find_element(*self.boton_finalizar).click()

    def obtener_mensaje_exito(self):
        return self.driver.find_element(*self.mensaje_exito).text

