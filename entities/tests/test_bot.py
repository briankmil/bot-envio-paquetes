import unittest
# from logic import Logic
import logic


class TestBot(unittest.TestCase):

    ##PRUEBAS PARA LISTAR PAQUETES
    def test_is_Admin(self):        
        self.assertTrue(logic.verifique_admin(1898458696))

    def test_is_Admin_Fail(self):        
        self.assertFalse(logic.verifique_admin(1234))

    def test_Listar_Paquetes_usuario(self):        
        self.assertIn("Listado de paquetes:", logic.listar_paquetes_por_usuario(1898458696))

    def test_Listar_Paquetes_usuario_Fail(self):        
        self.assertEqual(logic.listar_paquetes_por_usuario(1234),"No se encontraron paquetes para este usuario")
    
    def test_Listar_Paquetes_admin(self):        
        self.assertIn("Listado de paquetes:", logic.listar_paquetes_admin())

    