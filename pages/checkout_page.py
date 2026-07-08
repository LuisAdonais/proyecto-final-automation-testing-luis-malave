# pages/checkout_page.py
# Page Object del flujo de checkout en SauceDemo.
# Paso 1: datos del comprador | Paso 2: resumen | Paso 3: confirmacion


class CheckoutPage:
    """
    Representa las pantallas de checkout.
    Los localizadores viven aqui para que los tests no los repitan.
    """

    # --- Paso 1: formulario de informacion ---
    CAMPO_NOMBRE = "#first-name"
    CAMPO_APELLIDO = "#last-name"
    CAMPO_CODIGO_POSTAL = "#postal-code"
    BOTON_CONTINUAR = "#continue"

    # --- Paso 2: resumen de compra ---
    BOTON_FINALIZAR = "#finish"

    # --- Paso 3: mensaje de exito ---
    MENSAJE_CONFIRMACION = ".complete-header"

    # --- Mensajes de error (campos vacios o datos invalidos) ---
    MENSAJE_ERROR = "[data-test='error']"
    CAMPO_CON_ERROR = ".input_error"

    def __init__(self, driver):
        """Recibimos el navegador desde el test o fixture."""
        self.driver = driver

    def completar_datos(self, nombre, apellido, codigo_postal):
        """
        Completa el formulario del paso 1 del checkout.

        Parametros:
            nombre: primer nombre del comprador
            apellido: apellido del comprador
            codigo_postal: codigo postal
        """
        campo_nombre = self.driver.find_element("css selector", self.CAMPO_NOMBRE)
        campo_nombre.clear()
        campo_nombre.send_keys(nombre)

        campo_apellido = self.driver.find_element("css selector", self.CAMPO_APELLIDO)
        campo_apellido.clear()
        campo_apellido.send_keys(apellido)

        campo_cp = self.driver.find_element("css selector", self.CAMPO_CODIGO_POSTAL)
        campo_cp.clear()
        campo_cp.send_keys(codigo_postal)

    def continuar(self):
        """Hace click en Continue para ir al resumen de la compra."""
        boton = self.driver.find_element("css selector", self.BOTON_CONTINUAR)
        boton.click()

    def finalizar_compra(self):
        """Hace click en Finish para completar la compra."""
        boton = self.driver.find_element("css selector", self.BOTON_FINALIZAR)
        boton.click()

    def obtener_mensaje_confirmacion(self):
        """
        Devuelve el mensaje de compra exitosa.
        Ejemplo esperado: 'Thank you for your order!'
        """
        mensaje = self.driver.find_element("css selector", self.MENSAJE_CONFIRMACION)
        return mensaje.text

    def obtener_mensaje_error(self):
        """
        Devuelve el texto de error visible en pantalla.
        Sirve para validar cuando faltan datos obligatorios.
        """
        # Buscamos mensajes de error visibles (SauceDemo los muestra al fallar validacion)
        errores = self.driver.find_elements("css selector", self.MENSAJE_ERROR)
        textos = [error.text.strip() for error in errores if error.text.strip()]

        if textos:
            return textos[0]

        # Si no hay texto, verificamos si hay campos marcados con error
        campos_invalidos = self.driver.find_elements("css selector", self.CAMPO_CON_ERROR)
        if campos_invalidos:
            return "Error: faltan datos obligatorios en el formulario"

        return ""
