from rest_framework.test import APITestCase


class EncuestaApiTest(APITestCase):
    """Build a one-question survey through the API and read its report."""

    def setUp(self):
        self.client.post('/auth/users/create/', {
            'username': 'demo', 'email': 'demo@example.com',
            'password': 'S3cure-demo-pw'}, format='json')
        token = self.client.post('/auth/jwt/create/', {
            'username': 'demo', 'password': 'S3cure-demo-pw'},
            format='json').data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def post(self, path, data):
        response = self.client.post(path, data, format='json')
        self.assertEqual(response.status_code, 201, response.data)
        return response.data['url']

    def test_anonymous_cannot_create(self):
        self.client.credentials()
        response = self.client.post('/api/encuesta/', {'nombre': 'x'})
        self.assertEqual(response.status_code, 401)

    def test_multiple_choice_report(self):
        si = self.post('/api/alternativa/', {'texto': 'Si'})
        no = self.post('/api/alternativa/', {'texto': 'No'})
        pregunta = self.post('/api/pregunta/', {
            'titulo': 'Cafe', 'enunciado': 'Te gusta el cafe?', 'tipo': 1})
        for alternativa in (si, no):
            self.post('/api/pregunta_detalle/', {
                'pregunta': pregunta, 'alternativa': alternativa})
        encuesta = self.post('/api/encuesta/', {
            'nombre': 'Habitos', 'descripción': 'Encuesta de prueba'})
        encuesta_pregunta = self.post('/api/encuesta_pregunta/', {
            'encuesta': encuesta, 'pregunta': pregunta})
        for answer in (si, si, si, no):
            self.post('/api/solucion_alternativa_detalle/', {
                'pregunta': encuesta_pregunta, 'alternativa': answer})

        encuesta_id = encuesta.split('encuesta=')[1].split('/')[0]
        report = self.client.get('/api/reporte=%s/detail' % encuesta_id).data
        shares = report[encuesta][encuesta_pregunta]['alternativas']
        self.assertEqual(shares, {si: 0.75, no: 0.25})

    def test_text_answer_rejected_for_choice_question(self):
        pregunta = self.post('/api/pregunta/', {
            'titulo': 'Cafe', 'enunciado': 'Te gusta el cafe?', 'tipo': 1})
        encuesta = self.post('/api/encuesta/', {
            'nombre': 'Habitos', 'descripción': 'Encuesta de prueba'})
        encuesta_pregunta = self.post('/api/encuesta_pregunta/', {
            'encuesta': encuesta, 'pregunta': pregunta})
        response = self.client.post('/api/solucion_texto_detalle/', {
            'pregunta': encuesta_pregunta, 'texto': 'mucho'}, format='json')
        self.assertEqual(response.status_code, 400)
