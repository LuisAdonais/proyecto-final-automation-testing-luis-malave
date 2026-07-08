# pages/login_page.py
# Page Object de la pantalla de Login en SauceDemo.
# Los tests NO deben usar localizadores directos: todo pasa por esta clase.


class LoginPage:
    """
    Representa la pagina de login.
    Guardamos selectores y acciones en un solo lugar (patron POM).
    """

    # URL de la aplicacion
    URL = "https://www.saucedemo.com/"

    # Localizadores del login
    CAMPO_USUARIO = "#user-name"
    CAMPO_PASSWORD = "#password"
    BOTON_LOGIN = "#login-button"
    MENSAJE_ERROR = "[data-test='error']"

    def __init__(self, driver):
        """Recibimos el navegador (driver) desde el test."""
        self.driver = driver

    def abrir(self):
        """Abre la pagina de login en el navegador."""
        self.driver.get(self.URL)

    def login(self, usuario, password):
        """
        Hace login con usuario y contraseña.

        Parametros:
            usuario: nombre de usuario
            password: contraseña
        """
        campo_usuario = self.driver.find_element("css selector", self.CAMPO_USUARIO)
        campo_usuario.clear()
        campo_usuario.send_keys(usuario)

        campo_password = self.driver.find_element("css selector", self.CAMPO_PASSWORD)
        campo_password.clear()
        campo_password.send_keys(password)

        boton = self.driver.find_element("css selector", self.BOTON_LOGIN)
        boton.click()

    def obtener_mensaje_error(self):
        """Devuelve el texto del mensaje de error visible en pantalla."""
        mensaje = self.driver.find_element("css selector", self.MENSAJE_ERROR)
        return mensaje.text

    def esta_en_login(self):
        """
        Indica si seguimos en la pantalla de login.
        Util para validar login fallido o usuario bloqueado.
        """
        return self.driver.current_url == self.URL
