import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback_context
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# --- CARREGAR DADOS DA EMPRESA JUNIOR ---
try:
    # Dados da Empresa Junior
    areas = pd.read_csv('fake_data/area_projeto.csv')
    empresas = pd.read_csv('fake_data/empresa.csv')
    pessoas = pd.read_csv('fake_data/pessoa.csv')
    servicos = pd.read_csv('fake_data/servico.csv', parse_dates=['data_inicio', 'data_fim'])
    despesas = pd.read_csv('fake_data/despesa.csv', parse_dates=['data'])
    tributos = pd.read_csv('fake_data/tributo.csv')
    
    print("✅ Dados da Empresa Junior carregados com sucesso!")
    print(f"📊 {len(servicos)} serviços, {len(empresas)} empresas, {len(despesas)} despesas")
    
except FileNotFoundError as e:
    print(f"❌ Arquivo não encontrado: {e}")
    print("Certifique-se que a pasta 'fake_data' existe com todos os arquivos CSV.")
    exit()

# --- PREPARAÇÃO DOS DADOS ---
# Juntar serviços com áreas
data = servicos.merge(areas, on='id_area', how='left')

# Juntar com empresas (quando há empresa)
data = data.merge(empresas[['id_empresa', 'nome', 'area_empresa', 'capital_social']], 
                 left_on='id_empresa', right_on='id_empresa', how='left', suffixes=('', '_empresa'))

# Juntar com pessoas (quando há pessoa)
data = data.merge(pessoas[['id_pessoa', 'nome']], 
                 left_on='id_pessoa', right_on='id_pessoa', how='left', suffixes=('', '_pessoa'))

# Adicionar tributos agregados por serviço
tributos_agg = tributos.groupby('id_servico').agg({
    'percentual': ['sum', 'mean', 'count']
}).reset_index()
tributos_agg.columns = ['id_servico', 'total_tributos', 'media_tributos', 'qtd_tributos']

data = data.merge(tributos_agg, on='id_servico', how='left')

# Preencher valores nulos
data['total_tributos'] = data['total_tributos'].fillna(0)
data['media_tributos'] = data['media_tributos'].fillna(0)
data['qtd_tributos'] = data['qtd_tributos'].fillna(0)

# Calcular valor líquido (valor - tributos estimados)
data['valor_tributos_estimado'] = data['valor'] * (data['total_tributos'] / 100)
data['valor_liquido'] = data['valor'] - data['valor_tributos_estimado']

# Criar colunas auxiliares para data
data['mes_inicio'] = data['data_inicio'].dt.to_period('M').dt.to_timestamp()
data['ano_inicio'] = data['data_inicio'].dt.year
data['trimestre_inicio'] = data['data_inicio'].dt.quarter

# Definir cores do tema EJ
COLORS = {
    'primary': '#1E40AF',        # Azul EJ
    'secondary': '#7C3AED',      # Roxo
    'accent': '#F59E0B',         # Amarelo/Laranja
    'success': '#10B981',        # Verde
    'danger': '#EF4444',         # Vermelho 
    'background': '#F8FAFC',     # Cinza muito claro
    'card_bg': '#FFFFFF',        # Branco
    'text': '#1F2937',          # Cinza escuro
    'border': '#E5E7EB',        # Cinza claro
    'gradient_start': '#1E40AF',
    'gradient_end': '#7C3AED'
}

# --- DASH APP ---
app = Dash(__name__)
app.title = "Dashboard Empresa Junior - Análise Financeira"

# Estilo CSS customizado para EJ
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
            
            body {
                font-family: 'Inter', system-ui, -apple-system, sans-serif;
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }
            
            .header {
                background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 50%, #7C3AED 100%);
                color: white;
                padding: 3rem 0;
                margin-bottom: 2rem;
                box-shadow: 0 8px 32px rgba(30,64,175,0.15);
                position: relative;
                overflow: hidden;
            }
            
            .header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100"><path d="M0,20 Q250,60 500,20 T1000,20 L1000,100 L0,100 Z" fill="rgba(255,255,255,0.1)"/></svg>') repeat-x bottom;
                background-size: 100% 50px;
            }
            
            .kpi-card {
                background: white;
                padding: 2rem;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                margin: 0 10px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                border-left: 4px solid #1E40AF;
                position: relative;
                overflow: hidden;
            }
            
            .kpi-card::before {
                content: '';
                position: absolute;
                top: 0;
                right: 0;
                width: 80px;
                height: 80px;
                background: linear-gradient(45deg, rgba(30,64,175,0.1), rgba(124,58,237,0.15));
                border-radius: 50%;
                transform: translate(25px, -25px);
            }
            
            .kpi-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 8px 40px rgba(0,0,0,0.12);
                border-left-color: #7C3AED;
            }
            
            .kpi-value {
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0.8rem 0;
                color: #1F2937;
                position: relative;
                z-index: 2;
                line-height: 1.1;
            }
            
            .kpi-label {
                font-size: 0.875rem;
                color: #6B7280;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin: 0;
                font-weight: 600;
                position: relative;
                z-index: 2;
            }
            
            .kpi-icon {
                font-size: 2.5rem;
                opacity: 0.8;
                position: absolute;
                top: 2rem;
                right: 2rem;
                z-index: 2;
            }
            
            .chart-container {
                background: white;
                padding: 2.5rem;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                margin: 1.5rem 0;
                border: 1px solid #F3F4F6;
            }
            
            .filters-container {
                background: white;
                padding: 2.5rem;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                margin-bottom: 2rem;
                border: 1px solid #F3F4F6;
            }
            
            .section-title {
                color: #1F2937;
                font-size: 1.4rem;
                font-weight: 700;
                margin: 0 0 30px 0;
                padding-bottom: 12px;
                border-bottom: 3px solid #E5E7EB;
                position: relative;
            }
            
            .section-title::after {
                content: '';
                position: absolute;
                bottom: -3px;
                left: 0;
                width: 60px;
                height: 3px;
                background: linear-gradient(90deg, #1E40AF, #7C3AED);
                border-radius: 2px;
            }
            
            .metric-change {
                font-size: 0.875rem;
                margin-top: 10px;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 4px;
            }
            
            .metric-up { color: #10B981; }
            .metric-down { color: #EF4444; }
            .metric-neutral { color: #6B7280; }
            
            .filter-group {
                margin-bottom: 24px;
            }
            
            .filter-label {
                font-weight: 600;
                margin-bottom: 10px;
                display: block;
                color: #374151;
                font-size: 0.95rem;
            }
            
            .status-badge {
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .status-concluido { background: #D1FAE5; color: #065F46; }
            .status-andamento { background: #DBEAFE; color: #1E40AF; }
            .status-cancelado { background: #FEE2E2; color: #991B1B; }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.H1([
                html.I(className="fas fa-chart-line", style={'marginRight': '20px'}),
                "Dashboard Empresa Junior"
            ], style={
                'textAlign': 'center', 
                'margin': '0', 
                'fontSize': '3rem',
                'fontWeight': '700',
                'position': 'relative',
                'zIndex': '10'
            }),
            html.P("Análise completa de projetos, receitas e performance financeira", 
                   style={'textAlign': 'center', 'margin': '20px 0 0 0', 'opacity': '0.95', 
                         'fontSize': '1.2rem', 'position': 'relative', 'zIndex': '10'})
        ])
    ], className="header"),
    
    # Container principal
    html.Div([
        # Filtros
        html.Div([
            html.H3([
                html.I(className="fas fa-filter", style={'marginRight': '12px'}),
                "Filtros de Análise"
            ], className="section-title"),
            
            html.Div([
                html.Div([
                    html.Label("Período de Análise:", className="filter-label"),
                    dcc.DatePickerRange(
                        id='date-range-ej',
                        min_date_allowed=data['data_inicio'].min(),
                        max_date_allowed=data['data_inicio'].max(),
                        start_date=data['data_inicio'].min(),
                        end_date=data['data_inicio'].max(),
                        display_format='DD/MM/YYYY',
                        style={'width': '100%'}
                    )
                ], className="filter-group", style={'flex': '1', 'marginRight': '20px'}),
                
                html.Div([
                    html.Label("Área de Projeto:", className="filter-label"),
                    dcc.Dropdown(
                        id='area-filter',
                        options=[{'label': 'Todas as Áreas', 'value': 'all'}] + 
                               [{'label': area, 'value': area} for area in data['nome_area'].unique()],
                        value='all',
                        clearable=False
                    )
                ], className="filter-group", style={'flex': '1', 'marginRight': '20px'}),
                
                html.Div([
                    html.Label("Status do Projeto:", className="filter-label"),
                    dcc.Dropdown(
                        id='status-filter',
                        options=[{'label': 'Todos os Status', 'value': 'all'}] + 
                               [{'label': status, 'value': status} for status in data['status'].unique()],
                        value='all',
                        clearable=False
                    )
                ], className="filter-group", style={'flex': '1'})
            ], style={'display': 'flex', 'alignItems': 'end'})
        ], className="filters-container"),

        # KPIs principais
        html.Div([
            html.H3([
                html.I(className="fas fa-chart-bar", style={'marginRight': '12px'}),
                "Indicadores Principais"
            ], className="section-title"),
            
            html.Div([
                html.Div(id='total-receita-ej', style={'flex': '1'}),
                html.Div(id='total-projetos-ej', style={'flex': '1'}),
                html.Div(id='ticket-medio-ej', style={'flex': '1'}),
                html.Div(id='total-empresas-ej', style={'flex': '1'}),
            ], style={
                'display': 'flex', 
                'gap': '20px',
                'marginBottom': '30px',
                'flexWrap': 'wrap'
            })
        ]),

        # KPIs operacionais
        html.Div([
            html.H3([
                html.I(className="fas fa-cogs", style={'marginRight': '12px'}),
                "Métricas Operacionais"
            ], className="section-title"),
            
            html.Div([
                html.Div(id='receita-liquida-ej', style={'flex': '1'}),
                html.Div(id='tributos-totais-ej', style={'flex': '1'}),
                html.Div(id='taxa-conclusao-ej', style={'flex': '1'}),
            ], style={
                'display': 'flex', 
                'gap': '20px',
                'marginBottom': '40px',
                'flexWrap': 'wrap'
            })
        ]),

        # Gráficos principais
        html.Div([
            html.Div([
                dcc.Graph(id='receita-evolucao-ej')
            ], className="chart-container"),

            html.Div([
                html.Div([
                    dcc.Graph(id='projetos-area-ej')
                ], style={'flex': '1', 'marginRight': '10px'}),
                
                html.Div([
                    dcc.Graph(id='status-projetos-ej')
                ], style={'flex': '1', 'marginLeft': '10px'})
            ], style={'display': 'flex', 'gap': '20px'}, className="chart-container"),

            html.Div([
                html.Div([
                    dcc.Graph(id='empresas-areas-ej')
                ], style={'flex': '1', 'marginRight': '10px'}),
                
                html.Div([
                    dcc.Graph(id='tributos-analise-ej')
                ], style={'flex': '1', 'marginLeft': '10px'})
            ], style={'display': 'flex', 'gap': '20px'}, className="chart-container"),
        ])
    ], style={
        'maxWidth': '1400px', 
        'margin': '0 auto', 
        'padding': '0 20px'
    }),
    
    # Seção de despesas
    html.Div([
        html.Div([
            html.H3([
                html.I(className="fas fa-money-bill-wave", style={'marginRight': '12px'}),
                "Análise de Despesas"
            ], className="section-title"),
            dcc.Graph(id='despesas-analise-ej')
        ], className="chart-container")
    ], style={
        'maxWidth': '1400px', 
        'margin': '0 auto', 
        'padding': '0 20px'
    })
])

# --- CALLBACKS ---
@app.callback(
    [Output('total-receita-ej', 'children'),
     Output('total-projetos-ej', 'children'),
     Output('ticket-medio-ej', 'children'),
     Output('total-empresas-ej', 'children'),
     Output('receita-liquida-ej', 'children'),
     Output('tributos-totais-ej', 'children'),
     Output('taxa-conclusao-ej', 'children'),
     Output('receita-evolucao-ej', 'figure'),
     Output('projetos-area-ej', 'figure'),
     Output('status-projetos-ej', 'figure'),
     Output('empresas-areas-ej', 'figure'),
     Output('tributos-analise-ej', 'figure'),
     Output('despesas-analise-ej', 'figure')],
    [Input('date-range-ej', 'start_date'),
     Input('date-range-ej', 'end_date'),
     Input('area-filter', 'value'),
     Input('status-filter', 'value')]
)
def update_dashboard_ej(start_date, end_date, area_filter, status_filter):
    # Filtrar dados
    filtered = data.copy()
    
    # Filtro de data
    filtered = filtered[(filtered['data_inicio'] >= start_date) & 
                       (filtered['data_inicio'] <= end_date)]
    
    # Filtro de área
    if area_filter != 'all':
        filtered = filtered[filtered['nome_area'] == area_filter]
    
    # Filtro de status
    if status_filter != 'all':
        filtered = filtered[filtered['status'] == status_filter]

    # --- MÉTRICAS ---
    total_receita = filtered['valor'].sum()
    total_projetos = len(filtered)
    ticket_medio = total_receita / total_projetos if total_projetos > 0 else 0
    total_empresas = filtered['id_empresa'].nunique()
    
    receita_liquida = filtered['valor_liquido'].sum()
    tributos_totais = filtered['valor_tributos_estimado'].sum()
    
    projetos_concluidos = len(filtered[filtered['status'] == 'Concluído'])
    taxa_conclusao = (projetos_concluidos / total_projetos * 100) if total_projetos > 0 else 0

    # Função para criar KPI card
    def create_kpi_card_ej(title, value, icon, color, prefix="", suffix=""):
        return html.Div([
            html.I(className=f"{icon} kpi-icon", style={'color': color}),
            html.H4(title, className="kpi-label"),
            html.H2(f"{prefix}{value}{suffix}", className="kpi-value"),
        ], className="kpi-card")

    # KPI Cards
    kpi_receita = create_kpi_card_ej(
        "Receita Total", 
        f"{total_receita:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
        "fas fa-dollar-sign", COLORS['success'], "R$ "
    )

    kpi_projetos = create_kpi_card_ej(
        "Total de Projetos", 
        f"{total_projetos:,}".replace(',', '.'),
        "fas fa-project-diagram", COLORS['primary']
    )

    kpi_ticket = create_kpi_card_ej(
        "Ticket Médio", 
        f"{ticket_medio:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
        "fas fa-receipt", COLORS['secondary'], "R$ "
    )
    
    kpi_empresas = create_kpi_card_ej(
        "Empresas Clientes", 
        f"{total_empresas:,}".replace(',', '.'),
        "fas fa-building", COLORS['accent']
    )
    
    kpi_liquida = create_kpi_card_ej(
        "Receita Líquida", 
        f"{receita_liquida:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
        "fas fa-hand-holding-usd", COLORS['success'], "R$ "
    )
    
    kpi_tributos = create_kpi_card_ej(
        "Tributos Totais", 
        f"{tributos_totais:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
        "fas fa-file-invoice-dollar", COLORS['danger'], "R$ "
    )
    
    kpi_conclusao = create_kpi_card_ej(
        "Taxa de Conclusão", 
        f"{taxa_conclusao:.1f}",
        "fas fa-check-circle", COLORS['success'], "", "%"
    )

    # --- GRÁFICOS ---
    
    # 1. Evolução da Receita
    receita_mensal = filtered.groupby('mes_inicio')['valor'].sum().reset_index()
    
    fig_evolucao = px.line(receita_mensal, x='mes_inicio', y='valor',
                          title='💹 Evolução da Receita Mensal',
                          template='plotly_white')
    fig_evolucao.update_traces(line=dict(color=COLORS['primary'], width=3))
    fig_evolucao.update_layout(title_font_size=18, title_x=0.02)

    # 2. Projetos por Área
    area_data = filtered.groupby('nome_area').size().reset_index(name='quantidade')
    
    fig_areas = px.bar(area_data, x='quantidade', y='nome_area', orientation='h',
                      title='🎯 Projetos por Área',
                      template='plotly_white',
                      color='quantidade',
                      color_continuous_scale=[[0, COLORS['primary']], [1, COLORS['secondary']]])
    fig_areas.update_layout(title_font_size=16, title_x=0.02, showlegend=False)

    # 3. Status dos Projetos
    status_data = filtered['status'].value_counts()
    colors_status = {
        'Concluído': COLORS['success'],
        'Em andamento': COLORS['primary'], 
        'Cancelado': COLORS['danger']
    }
    
    fig_status = px.pie(values=status_data.values, names=status_data.index,
                       title='📊 Status dos Projetos',
                       template='plotly_white',
                       color=status_data.index,
                       color_discrete_map=colors_status)
    fig_status.update_layout(title_font_size=16, title_x=0.02)

    # 4. Empresas por Área de Atuação
    empresa_area = filtered.dropna(subset=['area_empresa']).groupby('area_empresa').size().reset_index(name='quantidade')
    
    fig_emp_areas = px.bar(empresa_area, x='area_empresa', y='quantidade',
                          title='🏢 Clientes por Área de Atuação',
                          template='plotly_white',
                          color='quantidade',
                          color_continuous_scale=[[0, COLORS['accent']], [1, COLORS['primary']]])
    fig_emp_areas.update_layout(title_font_size=16, title_x=0.02, showlegend=False)
    fig_emp_areas.update_xaxes(tickangle=45)

    # 5. Análise de Tributos
    tributos_area = filtered.groupby('nome_area')['total_tributos'].mean().reset_index()
    
    fig_tributos = px.bar(tributos_area, x='nome_area', y='total_tributos',
                         title='📋 Carga Tributária Média por Área (%)',
                         template='plotly_white',
                         color='total_tributos',
                         color_continuous_scale=[[0, COLORS['secondary']], [1, COLORS['danger']]])
    fig_tributos.update_layout(title_font_size=16, title_x=0.02, showlegend=False)

    # 6. Análise de Despesas
    despesas_categoria = despesas.groupby('categoria')['valor'].sum().sort_values(ascending=True)
    
    fig_despesas = px.bar(x=despesas_categoria.values, y=despesas_categoria.index,
                         orientation='h',
                         title='💸 Despesas por Categoria',
                         template='plotly_white',
                         color=despesas_categoria.values,
                         color_continuous_scale=[[0, COLORS['accent']], [1, COLORS['danger']]])
    fig_despesas.update_layout(title_font_size=16, title_x=0.02, showlegend=False)

    return (kpi_receita, kpi_projetos, kpi_ticket, kpi_empresas,
            kpi_liquida, kpi_tributos, kpi_conclusao,
            fig_evolucao, fig_areas, fig_status, fig_emp_areas, fig_tributos, fig_despesas)


if __name__ == '__main__':
    print("🚀 Iniciando Dashboard Empresa Junior...")
    print("📊 Acesse: http://localhost:8050")
    print("⏹️  Para parar: Ctrl+C")
    
    app.run(debug=True, host='0.0.0.0', port=8050)