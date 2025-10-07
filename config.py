# Configurações do Dashboard EJ
# Modifique este arquivo para personalizar o dashboard

# --- CONFIGURAÇÕES GERAIS ---
APP_TITLE = "Dashboard Empresa Junior - Análise Financeira"
APP_PORT = 8050
DEBUG_MODE = True

# --- CORES DO TEMA ---
COLORS = {
    'primary': '#1E40AF',        # Azul principal da EJ
    'secondary': '#7C3AED',      # Roxo para destaques
    'accent': '#F59E0B',         # Amarelo/Laranja para alertas
    'success': '#10B981',        # Verde para valores positivos
    'danger': '#EF4444',         # Vermelho para valores negativos
    'background': '#F8FAFC',     # Fundo da página
    'card_bg': '#FFFFFF',        # Fundo dos cards
    'text': '#1F2937',          # Cor do texto principal
    'border': '#E5E7EB',        # Bordas e separadores
}

# --- CAMINHOS DOS DADOS ---
DATA_PATHS = {
    'areas': 'fake_data/area_projeto.csv',
    'empresas': 'fake_data/empresa.csv',
    'pessoas': 'fake_data/pessoa.csv',
    'servicos': 'fake_data/servico.csv',
    'despesas': 'fake_data/despesa.csv',
    'tributos': 'fake_data/tributo.csv'
}

# --- CONFIGURAÇÕES DE VISUALIZAÇÃO ---
CHART_CONFIG = {
    'height': 400,
    'template': 'plotly_white',
    'title_font_size': 16,
    'show_legend': False
}

# --- CONFIGURAÇÕES DE KPIs ---
KPI_CONFIG = {
    'decimal_places': 2,
    'currency_symbol': 'R$ ',
    'thousands_separator': '.',
    'decimal_separator': ','
}

# --- MENSAGENS CUSTOMIZÁVEIS ---
MESSAGES = {
    'loading_success': "✅ Dados da Empresa Junior carregados com sucesso!",
    'loading_error': "❌ Erro ao carregar dados. Verifique se a pasta 'fake_data' existe.",
    'startup_message': "🚀 Iniciando Dashboard Empresa Junior...",
    'access_url': "📊 Acesse: http://localhost:{port}",
    'stop_instruction': "⏹️  Para parar: Ctrl+C"
}

# --- FILTROS PADRÃO ---
DEFAULT_FILTERS = {
    'area': 'all',
    'status': 'all',
    'date_format': 'DD/MM/YYYY'
}

# --- CONFIGURAÇÕES DE EXPORTAÇÃO ---
EXPORT_CONFIG = {
    'enable_export': True,
    'formats': ['png', 'pdf', 'html'],
    'filename_prefix': 'dashboard_ej'
}

# --- CONFIGURAÇÕES DE PERFORMANCE ---
PERFORMANCE = {
    'enable_caching': True,
    'cache_timeout': 300,  # 5 minutos
    'max_data_points': 1000
}

# --- CUSTOMIZAÇÕES POR ÁREA ---
AREA_COLORS = {
    'Desenvolvimento Web': '#1E40AF',
    'Criação de Jogos': '#7C3AED',
    'Automação': '#F59E0B'
}

# --- STATUS MAPPING ---
STATUS_COLORS = {
    'Concluído': '#10B981',
    'Em andamento': '#1E40AF',
    'Cancelado': '#EF4444'
}

# --- CONFIGURAÇÕES DE NOTIFICAÇÃO ---
ALERTS = {
    'low_revenue_threshold': 10000,  # R$ 10.000
    'high_tax_rate_threshold': 20,   # 20%
    'completion_rate_warning': 70    # 70%
}