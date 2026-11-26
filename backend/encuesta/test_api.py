from rest_framework.test import APITestCase

from encuesta.models import Alternativa_orden, Solucion_texto


class SurveyApiTestCase(APITestCase):
    def setUp(self):
        self.client.post('/auth/users/create/', {
            'username': 'demo', 'email': 'demo@example.com',
            'password': 'S3cure-demo-pw'}, format='json')
        token = self.client.post('/auth/jwt/create/', {
            'username': 'demo', 'password': 'S3cure-demo-pw'},
            format='json').data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def post(self, path, data, status=201):
        response = self.client.post(path, data, format='json')
        self.assertEqual(response.status_code, status, getattr(response, 'data', None))
        return response.data['url'] if status == 201 else response

    @staticmethod
    def pk(url):
        return url.split('=')[1].split('/')[0]

    def question(self, tipo, opciones=()):
        pregunta = self.post('/api/pregunta/', {
            'titulo': 'P', 'enunciado': 'Enunciado', 'tipo': tipo})
        urls = []
        for texto in opciones:
            alternativa = self.post('/api/alternativa/', {'texto': texto})
            self.post('/api/pregunta_detalle/', {
                'pregunta': pregunta, 'alternativa': alternativa})
            urls.append(alternativa)
        return pregunta, urls

    def survey_with(self, pregunta):
        encuesta = self.post('/api/encuesta/', {
            'nombre': 'Habitos', 'descripción': 'Encuesta de prueba'})
        encuesta_pregunta = self.post('/api/encuesta_pregunta/', {
            'encuesta': encuesta, 'pregunta': pregunta})
        return encuesta, encuesta_pregunta

    def report(self, encuesta, encuesta_pregunta):
        response = self.client.get('/api/reporte=%s/detail' % self.pk(encuesta))
        self.assertEqual(response.status_code, 200)
        return response.data[encuesta][encuesta_pregunta]


class OptionsAndQuestionsTest(SurveyApiTestCase):
    def test_option_detail_returns_that_option(self):
        self.post('/api/alternativa/', {'texto': 'Si'})
        no = self.post('/api/alternativa/', {'texto': 'No'})
        response = self.client.get('/api/alternativa=%s/detail' % self.pk(no))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['texto'], 'No')
        self.assertEqual(response.data['url'], no)

    def test_question_lists_its_options(self):
        pregunta, opciones = self.question(1, ['Si', 'No'])
        response = self.client.get('/api/pregunta=%s/detail' % self.pk(pregunta))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['tipo'], 1)
        self.assertEqual(sorted(response.data['alternativas']), sorted(opciones))

    def test_question_type_must_be_0_1_or_2(self):
        response = self.post('/api/pregunta/', {
            'titulo': 'P', 'enunciado': 'E', 'tipo': 3}, status=400)
        self.assertIn('tipo', response.data)

    def test_an_option_is_linked_to_a_question_once(self):
        pregunta, (si,) = self.question(1, ['Si'])
        self.post('/api/pregunta_detalle/', {
            'pregunta': pregunta, 'alternativa': si}, status=400)

    def test_survey_lists_its_questions_and_can_be_renamed(self):
        pregunta, _ = self.question(0)
        encuesta, _ = self.survey_with(pregunta)
        detail = self.client.get('/api/encuesta=%s/detail' % self.pk(encuesta)).data
        self.assertEqual(detail['preguntas'], [pregunta])
        response = self.client.patch('/api/encuesta=%s/update' % self.pk(encuesta),
                                     {'nombre': 'Otra'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nombre'], 'Otra')

    def test_anonymous_cannot_create_questions_but_can_read(self):
        self.question(0)
        self.client.credentials()
        self.post('/api/pregunta/', {'titulo': 'P', 'enunciado': 'E', 'tipo': 0},
                  status=401)
        self.assertEqual(len(self.client.get('/api/pregunta/').data), 1)


class AnswersAndReportTest(SurveyApiTestCase):
    def test_text_answers_are_counted_per_word(self):
        pregunta, _ = self.question(0)
        encuesta, ep = self.survey_with(pregunta)
        self.client.credentials()  # answering is public
        for texto in ('cafe con leche', 'cafe solo', 'te'):
            self.post('/api/solucion_texto_detalle/', {'pregunta': ep, 'texto': texto})
        self.assertEqual(Solucion_texto.objects.get(texto='cafe').count, 2)
        textos = self.report(encuesta, ep)['textos']
        self.assertEqual(textos, {'cafe': 2, 'con': 1, 'leche': 1, 'solo': 1, 'te': 1})
        self.assertEqual(list(textos)[0], 'cafe')

    def test_choice_answer_rejected_for_text_question(self):
        pregunta, _ = self.question(0)
        _, ep = self.survey_with(pregunta)
        alternativa = self.post('/api/alternativa/', {'texto': 'Si'})
        self.post('/api/solucion_alternativa_detalle/', {
            'pregunta': ep, 'alternativa': alternativa}, status=400)

    def test_ranking_answers_are_aggregated(self):
        pregunta, (a, b) = self.question(2, ['A', 'B'])
        encuesta, ep = self.survey_with(pregunta)
        for alternativa, orden in ((a, 1), (b, 2), (a, 1), (b, 1), (a, 2), (a, 1)):
            self.post('/api/alternativa_orden/', {
                'pregunta': ep, 'alternativa': alternativa, 'orden': orden})
        self.assertEqual(Alternativa_orden.objects.get(
            alternativa__id=self.pk(a), orden=1).total, 3)
        ranking = self.report(encuesta, ep)['alternativas_orden']
        self.assertEqual(ranking[a]['total'], 4)
        self.assertEqual(ranking[a]['orden'], {1: 0.75, 2: 0.25})
        self.assertEqual(ranking[b]['orden'], {1: 0.5, 2: 0.5})

    def test_ranking_rejects_a_position_out_of_range_or_a_foreign_option(self):
        pregunta, (a, b) = self.question(2, ['A', 'B'])
        _, ep = self.survey_with(pregunta)
        otra = self.post('/api/alternativa/', {'texto': 'otra'})
        for alternativa, orden in ((a, 0), (a, 3), (otra, 1)):
            with self.subTest(alternativa=alternativa, orden=orden):
                self.post('/api/alternativa_orden/', {
                    'pregunta': ep, 'alternativa': alternativa, 'orden': orden},
                    status=400)
        self.assertEqual(Alternativa_orden.objects.count(), 0)

    def test_report_covers_every_question_of_the_survey(self):
        texto, _ = self.question(0)
        eleccion, (si, no) = self.question(1, ['Si', 'No'])
        encuesta, ep_texto = self.survey_with(texto)
        ep_eleccion = self.post('/api/encuesta_pregunta/', {
            'encuesta': encuesta, 'pregunta': eleccion})
        self.post('/api/solucion_texto_detalle/', {'pregunta': ep_texto, 'texto': 'hola'})
        self.post('/api/solucion_alternativa_detalle/', {
            'pregunta': ep_eleccion, 'alternativa': no})
        report = self.client.get('/api/reporte=%s/detail' % self.pk(encuesta)).data[encuesta]
        self.assertEqual(set(report), {ep_texto, ep_eleccion})
        self.assertEqual(report[ep_texto]['problema'], texto)
        self.assertEqual(report[ep_texto]['textos'], {'hola': 1})
        self.assertEqual(report[ep_eleccion]['alternativas'], {no: 1.0})

    def test_report_of_a_missing_survey_is_400(self):
        self.assertEqual(self.client.get('/api/reporte=999/detail').status_code, 400)
