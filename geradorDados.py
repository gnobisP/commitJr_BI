import pandas as pd
import random
import faker
from faker import Faker
from faker.providers import BaseProvider
import random
import pandas as pd
from datetime import date

# Inicializa o gerador de dados falsos
fake = faker.Faker('pt_BR')
random.seed(42)
# -----------------
# Geração de pessoa.csv (7 linhas)
# -----------------
pessoa_data = []
for i in range(1, 7
               ):
    pessoa_data.append([
        i,
        fake.name(),
        fake.email(),
        fake.phone_number()
    ])

pessoa_df = pd.DataFrame(pessoa_data, columns=["id_pessoa", "nome", "email", "telefone"])
pessoa_df.to_csv("fake_data/pessoa.csv", index=False)

# -----------------
# Geração de empresa.csv (20 linhas)
# -----------------
companyActivity = ["PetShop", "Advocacia", "E-commerce", "Ensino", "Design", "Eventos", "Entretenimento", "Outros"]
empresa_data = []
for i in range(1, 31):
    empresa_data.append([
        i,
        fake.company(),
        fake.cnpj(),
        fake.phone_number(),
        fake.email(),
        random.randint(1000, 20000),
        fake.address(),
        companyActivity[random.randint(0, 7)]
    ])

empresa_df = pd.DataFrame(empresa_data, columns=["id_empresa", "nome", "cnpj","telefone","email","capital_social", "endereco", "area_empresa"])
empresa_df.to_csv("fake_data/empresa.csv", index=False)
# -----------------
# Geração de area_projeto.csv (3 linhas)
# -----------------
areas = ["Desenvolvimento Web", "Criação de Jogos", "Automação"]
area_data = [[i+1, areas[i]] for i in range(3)]
area_df = pd.DataFrame(area_data, columns=["id_area", "nome_area"])
area_df.to_csv("fake_data/area_projeto.csv", index=False)

# -----------------
# Geração de servico.csv (100 linhas)
# -----------------
# --- Provider customizado ---
class EJServiceProvider(BaseProvider):
    web_titles = [
        "Desenvolvimento de site institucional",
        "E-commerce com checkout integrado",
        "Landing page de campanha",
        "Portal com CMS e blog",
        "API REST e painel administrativo",
        "Refatoração e otimização de performance web",
        "Integração com gateway de pagamento",
        "Sistema de autenticação e área do cliente"
    ]
    web_features = [
        "layout responsivo", "SEO on-page", "otimização de imagens",
        "cache e CDN", "analytics e eventos", "acessibilidade (WCAG)",
        "integração com CRM", "formulários com validação"
    ]
    web_stacks = [
        "Next.js + Node.js + PostgreSQL",
        "React + Django + PostgreSQL",
        "Vue + Laravel + MySQL",
        "WordPress + WooCommerce",
        "SvelteKit + Supabase"
    ]

    game_titles = [
        "Protótipo de jogo 2D de plataforma",
        "Jogo mobile de puzzles",
        "Runner infinito com ranking",
        "Serious game educativo",
        "Advergame para campanha",
        "Port do jogo para Android",
        "Minigames para evento"
    ]
    game_features = [
        "sistema de fases", "ranking online", "conquistas",
        "IA básica de inimigos", "controle por toque/teclado",
        "salvamento de progresso", "HUD e menus",
        "efeitos sonoros e trilha"
    ]
    game_engines = ["Unity", "Godot", "Unreal (Blueprints)", "Phaser"]

    auto_titles = [
        "Automação de deploy (CI/CD)",
        "RPA para extração de dados",
        "Integração de APIs e webhooks",
        "Robô de testes end-to-end",
        "Monitoramento e alertas",
        "Automação de relatórios semanais"
    ]
    auto_features = [
        "pipelines GitHub Actions", "containers Docker",
        "agendamento com cron", "logs centralizados",
        "orquestração de tarefas", "testes E2E com Playwright/Selenium",
        "integração com Slack/Discord"
    ]
    auto_tools = ["Python RPA", "Playwright", "Selenium", "Node-RED", "Airflow", "GitHub Actions"]

    def service_title(self, area: str) -> str:
        if area == "Desenvolvimento Web":
            return random.choice(self.web_titles)
        if area == "Desenvolvimento de Jogos":
            return random.choice(self.game_titles)
        return random.choice(self.auto_titles)

    def service_description(self, area: str) -> str:
        if area == "Desenvolvimento Web":
            feats = ", ".join(random.sample(self.web_features, k=3))
            stack = random.choice(self.web_stacks)
            return f"Projeto web com foco em {feats}. Stack utilizada: {stack}."
        if area == "Desenvolvimento de Jogos":
            feats = ", ".join(random.sample(self.game_features, k=3))
            engine = random.choice(self.game_engines)
            alvo = random.choice(["web", "Android", "PC"])
            return f"Jogo com {feats}. Desenvolvido na engine {engine}, com build para {alvo}."
        feats = ", ".join(random.sample(self.auto_features, k=3))
        tool = random.choice(self.auto_tools)
        return f"Automação implementada usando {tool}, com {feats}."

fake.add_provider(EJServiceProvider)

# --- Áreas disponíveis ---
areas = {
    1: "Desenvolvimento de Jogos",
    2: "Desenvolvimento Web",
    3: "Automação"
}

# --- Função auxiliar para valores ---
def gerar_valor(area_nome: str) -> float:
    if area_nome == "Desenvolvimento de Jogos":
        return round(random.uniform(150, 1200), 2)
    if area_nome == "Desenvolvimento Web":
        return round(random.uniform(150, 1500), 2)
    return round(random.uniform(300, 1700), 2)  # Automação

# --- Geração dos serviços ---
servico_data = []
for i in range(1, 101):
    # Distribuição de áreas
    if random.random() < 0.2:
        id_area = 1
    elif random.random() < 0.5:
        id_area = 2
    else:
        id_area = 3
    area_nome = areas[id_area]

    # Gerar dados
    id_servico = i
    titulo = fake.service_title(area_nome)
    descricao = fake.service_description(area_nome)
    valor = gerar_valor(area_nome)
    data_inicio = fake.date_between(start_date=date(2018, 1, 1), end_date="today")

    if random.random() < 0.3:  # 30% em andamento
        data_fim = None
        status = "Em andamento"
    else:
        data_fim = fake.date_between(start_date=data_inicio, end_date="today")
        status = random.choice(["Concluído", "Cancelado"])

    # Cliente (pessoa ou empresa)
    if random.random() < 0.1:
        id_pessoa = random.randint(1, 7)
        id_empresa = None
    else:
        id_pessoa = None
        id_empresa = random.randint(1, 31)

    servico_data.append([
        id_servico,
        titulo,
        descricao,
        valor,
        data_inicio,
        data_fim,
        status,
        id_area,
        id_pessoa,
        id_empresa
    ])

# --- Salvar em CSV ---
servico_df = pd.DataFrame(
    servico_data,
    columns=["id_servico", "titulo", "descricao", "valor", "data_inicio", "data_fim", "status", "id_area", "id_pessoa", "id_empresa"]
)
servico_df.to_csv("fake_data/servico.csv", index=False, encoding="utf-8")


# -----------------
# Geração de tributo.csv (~120 linhas)
# -----------------
tributo_data = []
tributos_possiveis = ["ISS", "ICMS", "IPI", "COFINS", "PIS", "IRPJ"]
id_counter = 1
for i in range(1, 101):
    n_tributos = 1 if random.random() < 0.8 else 2  # média de 1,2 tributos por serviço
    for _ in range(n_tributos):
        tributo_data.append([
            id_counter,
            random.choice(tributos_possiveis),
            round(random.uniform(1, 20), 2),  # percentual
            i  # id_servico
        ])
        id_counter += 1

tributo_df = pd.DataFrame(tributo_data, columns=["id_tributo", "tipo", "percentual", "id_servico"])
tributo_df.to_csv("fake_data/tributo.csv", index=False)



# -----------------
# Geração de despesa.csv (30 linhas)
# -----------------
despesa_data = []
categorias_despesa = [
    "Cursos",
    "Licença para produção",
    "Troca de gestão",
    "Contabilidade",
    "Manutenção",
    "Outros"
]

# Gerar dados de despesas
despesa_data = []
for i in range(1, 30):
    despesa_data.append([
        i,
        fake.sentence(nb_words=4),  # descrição curta
        round(random.uniform(50, 1000), 2),  # valor aleatório
        fake.date_between(start_date="-8y", end_date="today"),  # data nos últimos 8 anos
        random.choice(categorias_despesa)  # categoria aleatória
    ])

despesa_df = pd.DataFrame(despesa_data, columns=["id_despesa", "descricao", "valor", "data", "categoria"])
despesa_df.to_csv("fake_data/despesa.csv", index=False)

