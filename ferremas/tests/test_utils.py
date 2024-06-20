import unittest
from unittest.mock import patch
from utils import obtener_valor_dolar
import pandas as pd
from datetime import datetime, timedelta

class TestUtils(unittest.TestCase):

    @patch('utils.bcchapi.Siete')
    def test_obtener_valor_dolar(self, MockSiete):
        # Crear un DataFrame de pandas simulado
        data = {
            'dolar_day': [750, 755, 760]
        }
        index = pd.date_range(start=(datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"), periods=3, freq='D')
        mock_df = pd.DataFrame(data, index=index)

        # Configurar el Mock
        mock_instance = MockSiete.return_value
        mock_instance.cuadro.return_value = mock_df

        # Llamar a la función con el mock configurado
        valor_dolar = obtener_valor_dolar('fake_user', 'fake_password')

        # Aserciones
        self.assertEqual(valor_dolar, 760)
        mock_instance.cuadro.assert_called_once_with(
            series=['F073.TCO.PRE.Z.D'],
            nombres=['dolar_day'],
            desde=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            hasta=datetime.now().strftime("%Y-%m-%d")
        )

if __name__ == '__main__':
    unittest.main()
