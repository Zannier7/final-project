# services/users/project/test/test_users.py
import json
import unittest

from project.test.base import BaseTestCase
from project import db
from project.api.models import Auto


def add_auto(marca, modelo, tipo, color, placa):
    auto = Auto(marca=marca, modelo=modelo,
                tipo=tipo, color=color, placa=placa)
    db.session.add(auto)
    db.session.commit()
    return auto


class TestUserService(BaseTestCase):
    """Prueba para el servicio users."""

    def test_users(self):
        """Asegurando que la ruta /ping se comporta correctamente."""
        response = self.client.get('/autos/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])

    def test_add_autos(self):
        """ Asegunrando de que se pueda agregar un
        nuevo registro del auto a la base de datos."""
        with self.client:
            response = self.client.post(
                '/autos',
                data=json.dumps({
                    'marca': 'bmw',
                    'modelo': 'ci3',
                    'tipo': 'deportivo',
                    'color': 'blanco',
                    'placa': '7u456a'
                }),
                content_type='application/json',
            )

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('7u456a a sido agregado!', data['message'])
        self.assertIn('satisfactorio', data['status'])

    def test_add_autos_invalid_json(self):
        """ Asegurando de que se arroje
        un error si el objeto JSON está vacío."""

        with self.client:
            response = self.client.post(
                '/autos',
                data=json.dumps({}),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_autos_invalid_json_keys(self):
        """Asegurando de que se produce un error
        si el objeto JSON no tiene los campos completos."""

        with self.client:
            response = self.client.post(
                '/autos',
                data=json.dumps({
                    'placa': '7u456a'
                }),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_auto_duplicate_placa(self):
        """Asegurando de que se haya
        producido un error si la placa ya existe."""

        with self.client:
            self.client.post(
                '/autos',
                data=json.dumps({
                    'marca': 'bmw',
                    'modelo': 'ci3',
                    'tipo': 'deportivo',
                    'color': 'blanco',
                    'placa': '7u456a'}),
                content_type='application/json',
            )
        response = self.client.post(
            '/autos',
            data=json.dumps({
                'marca': 'bmw',
                'modelo': 'ci3',
                'tipo': 'deportivo',
                'color': 'blanco',
                'placa': '7u456a'
            }),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Disculpe. Esta placa ya existe.', data['mensaje'])
        self.assertIn('fallo', data['estado'])

    def test_single_user(self):
        """ Asegurando de que el usuario
        individual se comporte correctamente."""
        auto = add_auto('bmw', 'ci3', 'deportivo', 'blanco', '7u456a')
        with self.client:
            response = self.client.get(f'/autos/{auto.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('bmw', data['data']['marca'])
            self.assertIn('ci3', data['data']['modelo'])
            self.assertIn('deportivo', data['data']['tipo'])
            self.assertIn('blanco', data['data']['color'])
            self.assertIn('7u456a', data['data']['placa'])
            self.assertIn('satisfactorio', data['estado'])

    def test_single_auto_no_id(self):
        """Asegúrese de que se arroje un error
        si no se proporciona una identificación."""

        with self.client:
            response = self.client.get('/autos/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El auto no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_single_auto_incorrect_id(self):
        """Asegurando de que se arroje un error
        si la identificación no existe."""

        with self.client:
            response = self.client.get('/autos/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El auto no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_all_users(self):
        """ Asegurando de que todos los usuarios se comporten correctamente."""

        add_auto('bmw', 'ci3', 'deportivo', 'blanco', '7u456a')
        add_auto('audio', 'uik', '4x4', 'negro', '5625as')
        with self.client:
            response = self.client.get('/autos')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['autos']), 2)

            self.assertIn('bmw', data['data']['autos'][0]['marca'])
            self.assertIn('ci3', data['data']['autos'][0]['modelo'])
            self.assertIn('deportivo', data['data']['autos'][0]['tipo'])
            self.assertIn('blanco', data['data']['autos'][0]['color'])
            self.assertIn('7u456a', data['data']['autos'][0]['placa'])

            self.assertIn('audio', data['data']['autos'][1]['marca'])
            self.assertIn('uik', data['data']['autos'][1]['modelo'])
            self.assertIn('4x4', data['data']['autos'][1]['tipo'])
            self.assertIn('negro', data['data']['autos'][1]['color'])
            self.assertIn('5625as', data['data']['autos'][1]['placa'])
            self.assertIn('satisfactorio', data['estado'])

    def test_main_no_autos(self):
        """Ensure the main route behaves correctly when no users have been
        added to the database."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Autos', response.data)
        self.assertIn(b'<p>No autos!</p>', response.data)

    def test_main_with_users(self):
        """Ensure the main route behaves correctly when users have been
        added to the database."""
        add_auto('bmw', 'ci3', 'deportivo', 'blanco', '7u456a')
        add_auto('audio', 'uik', '4x4', 'negro', '5625as')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Autos', response.data)
            self.assertNotIn(b'<p>No autos!</p>', response.data)
            self.assertIn(b'bmw', response.data)
            self.assertIn(b'audio', response.data)

    def test_main_add_auto(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(marca='bmw', modelo='ci3',
                          tipo='deportivo', color='blanco', placa='7u456a'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Autos', response.data)
            self.assertNotIn(b'<p>No autos!</p>', response.data)
            self.assertIn(b'bmw', response.data)


if __name__ == '__main__':
    unittest.main()
