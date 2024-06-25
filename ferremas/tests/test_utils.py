import unittest
from unittest.mock import patch
from utils import obtener_valor_dolar, authenticate_user
import pandas as pd
from datetime import datetime, timedelta



class TestUtils(unittest.TestCase):

    @patch('utils.bcchapi.Siete')
    def test_obtener_valor_dolar(self, MockSiete):
        data = {'dolar_day': [750, 755, 760]}
        index = pd.date_range(start=(datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"), periods=3, freq='D')
        mock_df = pd.DataFrame(data, index=index)
        
        mock_instance = MockSiete.return_value
        mock_instance.cuadro.return_value = mock_df

        valor_dolar = obtener_valor_dolar('fake_user', 'fake_password')

        self.assertEqual(valor_dolar, 760)
        mock_instance.cuadro.assert_called_once_with(
            series=['F073.TCO.PRE.Z.D'],
            nombres=['dolar_day'],
            desde=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            hasta=datetime.now().strftime("%Y-%m-%d")
        )

    @patch('utils.bcchapi.Siete')
    def test_obtener_valor_dolar_empty_dataframe(self, MockSiete):
        mock_df = pd.DataFrame(columns=['dolar_day'])
        
        mock_instance = MockSiete.return_value
        mock_instance.cuadro.return_value = mock_df

        valor_dolar = obtener_valor_dolar('fake_user', 'fake_password')

        self.assertIsNone(valor_dolar)

    @patch('utils.bcchapi.Siete')
    def test_obtener_valor_dolar_all_nan(self, MockSiete):
        data = {'dolar_day': [float('nan'), float('nan'), float('nan')]}
        index = pd.date_range(start=(datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"), periods=3, freq='D')
        mock_df = pd.DataFrame(data, index=index)
        
        mock_instance = MockSiete.return_value
        mock_instance.cuadro.return_value = mock_df

        valor_dolar = obtener_valor_dolar('fake_user', 'fake_password')

        self.assertIsNone(valor_dolar)

    @patch('utils.bcchapi.Siete')
    def test_obtener_valor_dolar_intercalated_nan(self, MockSiete):
        data = {'dolar_day': [750, float('nan'), 760]}
        index = pd.date_range(start=(datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"), periods=3, freq='D')
        mock_df = pd.DataFrame(data, index=index)
        
        mock_instance = MockSiete.return_value
        mock_instance.cuadro.return_value = mock_df

        valor_dolar = obtener_valor_dolar('fake_user', 'fake_password')

        self.assertEqual(valor_dolar, 760)

    @patch('utils.bcchapi.Siete')
    def test_obtener_valor_dolar_single_valid_value(self, MockSiete):
        data = {'dolar_day': [float('nan'), 755, float('nan')]}
        index = pd.date_range(start=(datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"), periods=3, freq='D')
        mock_df = pd.DataFrame(data, index=index)
        
        mock_instance = MockSiete.return_value
        mock_instance.cuadro.return_value = mock_df

        valor_dolar = obtener_valor_dolar('fake_user', 'fake_password')

        self.assertEqual(valor_dolar, 755)

    @patch('utils.bcchapi.Siete')
    def test_obtener_valor_dolar_non_chronological_order(self, MockSiete):
        data = {'dolar_day': [760, 750, 755]}
        index = pd.date_range(start=(datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"), periods=3, freq='D')
        index = index[[2, 0, 1]]  # Reorder to non-chronological
        mock_df = pd.DataFrame(data, index=index)
        
        mock_instance = MockSiete.return_value
        mock_instance.cuadro.return_value = mock_df

        valor_dolar = obtener_valor_dolar('fake_user', 'fake_password')

        self.assertEqual(valor_dolar, 760)










class TestAuthUtils(unittest.TestCase):
    
    def test_authenticate_user_success(self):
        # Prueba de autenticación exitosa
        self.assertTrue(authenticate_user('user1', 'password1'))
    
    def test_authenticate_user_failure(self):
        # Prueba de autenticación fallida
        self.assertFalse(authenticate_user('user1', 'wrong_password'))
        self.assertFalse(authenticate_user('unknown_user', 'password1'))

if __name__ == '__main__':
    unittest.main()
