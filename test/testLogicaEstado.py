import unittest
import logic

class TestLogicaEstado(unittest.TestCase):
    
    def test_cambiar_estado(self):
        """prueba del cambio del estado de un paquete"""
        resultado_cambio = logic.cambiar_estado(4,1923311798, 'recogido')
        self.assertTrue(resultado_cambio)

    def test_cambiar_estado_pq_inexistente(self):
        """prueba del cambio del estado de un paquete inexistente"""
        resultado_cambio = logic.cambiar_estado(16,1923311798, 'recogido')
        self.assertFalse(resultado_cambio)
    
    def test_eliminar_estado(self):
        """prueba de la eliminacion de un estado"""
        resultado_cambio = logic.remover_estado(26)
        self.assertTrue(resultado_cambio)

    def test_eliminar_estado_pq_inexistente(self):
        """prueba de la eliminacion de un estado asignado a un paquete existene"""
        resultado_cambio = logic.remover_estado(28)
        self.assertFalse(resultado_cambio)
