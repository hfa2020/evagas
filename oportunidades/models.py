from django.db import models
from django.conf import settings

# Create your models here.


class Oportunidades(models.Model):
    UM = 1
    DOIS = 2
    TRES = 3
    ACIMA = 4

    FAIXA_SALARIAL = [
        (UM, "Até 1.000"),
        (DOIS, "De 1.000 a 2.000"),
        (TRES, "De 2.000 a 3.000"),
        (ACIMA, "Acima de 3.000"),
    ]

    FUNDAMENTAL = 1
    MEDIO = 2
    TECNOLOGO = 3
    SUPERIOR = 4
    POS = 5
    DOUTORADO = 6

    ESCOLARIDADE = [(FUNDAMENTAL, "Ensino Fundamental"),
                    (MEDIO, "Ensino Médio"), (TECNOLOGO, "Tecnólogo"),
                    (SUPERIOR, "Ensino Superior"),
                    (POS, "Pós / MBA / Mestrado"), (DOUTORADO, "Doutorado")]

    nome = models.CharField(max_length=50)
    requisitos = models.TextField()
    empresa = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name="Empresa")
    faixa_salario = models.IntegerField(choices=FAIXA_SALARIAL,
                                        default=1,
                                        verbose_name="Faixa Salarial")
    escolaridade = models.IntegerField(choices=ESCOLARIDADE,
                                       default=FUNDAMENTAL,
                                       verbose_name="Escolaridade Mínima")
    data = models.DateField(auto_now_add=True,
                            blank=True,
                            verbose_name="Data de Criação")

    @property
    def NmrCandidaturas(self):
        return self.candidaturas_set.count()

    def __str__(self):
        return f"Vaga para {self.nome} em {self.empresa.first_name}"

    class Meta:
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas"


class Candidaturas(models.Model):
    vaga = models.ForeignKey(Oportunidades,
                             on_delete=models.CASCADE,
                             verbose_name="Vaga")
    candidato = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  verbose_name="Candidato")
    salario_pretendido = models.DecimalField(decimal_places=2,
                                             max_digits=10,
                                             verbose_name="Salário Pretendido",
                                             default=1000.00)
    data = models.DateField(auto_now_add=True,
                            blank=True,
                            verbose_name="Data de Candidatura")

    @property
    def score(self):
        if self.salario_pretendido < 1000:
            sal_pret_range = 1
        elif self.salario_pretendido < 2000:
            sal_pret_range = 2
        elif self.salario_pretendido < 3000:
            sal_pret_range = 3
        else:
            sal_pret_range = 4

        print(
            f'Vaga:{self}\nCandidato:{self.candidato}\nSalario candidato:{sal_pret_range}\nSalario vaga: {self.vaga.faixa_salario}'
        )
        if sal_pret_range <= self.vaga.faixa_salario:
            sal_score = 1
        else:
            sal_score = 0

        print(
            f'\nEscolaridade candidato: {self.candidato.ult_escola}; Escolaridade Vaga: {self.vaga.escolaridade}\n'
        )
        if self.candidato.ult_escola >= self.vaga.escolaridade:
            esc_score = 1
        else:
            esc_score = 0

        print(f'SCORE: {sal_score + esc_score}\n\n')
        return sal_score + esc_score

    def __str__(self):
        return f"Candidatura de {self.candidato} para {self.vaga}"

    class Meta:

        constraints = [
            models.UniqueConstraint(fields=['vaga', 'candidato'],
                                    name='unique_vaga_candidato')
        ]
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"
