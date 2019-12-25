from django.test import TestCase
from .models import Usuarios
from oportunidades.models import Candidaturas, Oportunidades
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from django.test.utils import override_settings

# Create your tests here.


class TesteScore(TestCase):
    def setUp(self):
        Usuarios.objects.create_user(email="teste1@gmail.com",
                                     first_name="Teste1",
                                     experiencia="Sem experiência",
                                     ult_escola=1,
                                     is_empresa=False)
        Usuarios.objects.create_user(email="teste2@gmail.com",
                                     first_name="Teste2",
                                     experiencia="Sem experiência",
                                     is_empresa=True)
        Usuarios.objects.create_user(email="teste3@gmail.com",
                                     first_name="Teste3",
                                     experiencia="Sem experiência",
                                     ult_escola=6,
                                     is_empresa=False)
        Usuarios.objects.create_user(email="teste4@gmail.com",
                                     first_name="Teste4",
                                     experiencia="Sem experiência",
                                     ult_escola=5,
                                     is_empresa=False)
        Usuarios.objects.create_user(email="teste5@gmail.com",
                                     first_name="Teste5",
                                     experiencia="Sem experiência",
                                     ult_escola=1,
                                     is_empresa=False)

        Oportunidades.objects.create(
            nome="Vaga 1",
            requisitos="Experiênia com Django",
            empresa=Usuarios.objects.get(email="teste2@gmail.com"),
            faixa_salario=2,
            escolaridade=3)

    def test_is_score_working(self):

        teste1 = Usuarios.objects.get(email="teste1@gmail.com")
        teste2 = Usuarios.objects.get(email="teste2@gmail.com")
        teste3 = Usuarios.objects.get(email="teste3@gmail.com")
        teste4 = Usuarios.objects.get(email="teste4@gmail.com")
        teste5 = Usuarios.objects.get(email="teste5@gmail.com")

        Candidaturas.objects.create(
            vaga=Oportunidades.objects.get(nome="Vaga 1"),
            candidato=teste1,
            salario_pretendido=1250)
        Candidaturas.objects.create(
            vaga=Oportunidades.objects.get(nome="Vaga 1"),
            candidato=teste3,
            salario_pretendido=2450)
        Candidaturas.objects.create(
            vaga=Oportunidades.objects.get(nome="Vaga 1"),
            candidato=teste4,
            salario_pretendido=1700)
        Candidaturas.objects.create(
            vaga=Oportunidades.objects.get(nome="Vaga 1"),
            candidato=teste5,
            salario_pretendido=2900)

        cand_teste1 = Candidaturas.objects.get(candidato=teste1)
        cand_teste3 = Candidaturas.objects.get(candidato=teste3)
        cand_teste4 = Candidaturas.objects.get(candidato=teste4)
        cand_teste5 = Candidaturas.objects.get(candidato=teste5)

        self.assertEqual(cand_teste1.score, 1)
        self.assertEqual(cand_teste3.score, 1)
        self.assertEqual(cand_teste4.score, 2)
        self.assertEqual(cand_teste5.score, 0)


class testaLoginPermissao(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(4)

        Usuarios.objects.create_user(email="teste1@gmail.com",
                                     password="jobconvo2020",
                                     first_name="Teste1",
                                     experiencia="Sem experiência",
                                     ult_escola=1,
                                     is_empresa=False)

        Usuarios.objects.create_user(email="teste2@gmail.com",
                                     password="jobconvo2020",
                                     first_name="Teste2",
                                     experiencia="Sem experiência",
                                     is_empresa=True)

        Oportunidades.objects.create(
            nome="Vaga 1",
            requisitos="Experiênia com Django",
            empresa=Usuarios.objects.get(email="teste2@gmail.com"),
            faixa_salario=2,
            escolaridade=3)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


class testaLogin_Permissao1(testaLoginPermissao):
    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('teste1@gmail.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('jobconvo2020')
        self.selenium.find_element_by_tag_name('button').click()


class testaLogin_Permissao2(testaLoginPermissao):
    def test_permissao_empresa_candidatar_nao(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('teste2@gmail.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('jobconvo2020')
        self.selenium.find_element_by_tag_name('button').click()

        self.selenium.get('%s%s' %
                          (self.live_server_url, '/vagas/candidatar/1'))

        wait = WebDriverWait(self.selenium, 10)
        element = wait.until(
            EC.text_to_be_present_in_element((
                By.TAG_NAME, "h1"
            ), "A página não existe, ou você não tem permissão para acessá-la."
                                             ))


class testaLogin_Permissao3(testaLoginPermissao):
    def test_permissao_candidato_criar_vaga_nao(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('teste1@gmail.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('jobconvo2020')
        self.selenium.find_element_by_tag_name('button').click()

        self.selenium.get('%s%s' % (self.live_server_url, '/vagas/criar/'))

        wait = WebDriverWait(self.selenium, 10)
        element = wait.until(
            EC.text_to_be_present_in_element((
                By.TAG_NAME, "h1"
            ), "A página não existe, ou você não tem permissão para acessá-la."
                                             ))



class testaLogin_Permissao4(testaLoginPermissao):
    def test_permissao_empresa_candidatar_nao(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('teste1@gmail.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('jobconvo2020')
        self.selenium.find_element_by_tag_name('button').click()

        self.selenium.get('%s%s' %
                          (self.live_server_url, '/vagas/estatisticas/'))

        wait = WebDriverWait(self.selenium, 10)
        element = wait.until(
            EC.text_to_be_present_in_element((
                By.TAG_NAME, "h1"
            ), "A página não existe, ou você não tem permissão para acessá-la."
                                             ))
