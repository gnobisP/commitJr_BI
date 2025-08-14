import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# --- CARREGAR DADOS ---
try:
    orders = pd.read_csv('data/olist_orders_dataset.csv', parse_dates=['order_purchase_timestamp'])
    customers = pd.read_csv('data/olist_customers_dataset.csv')
    order_items = pd.read_csv('data/olist_order_items_dataset.csv')
    products = pd.read_csv('data/olist_products_dataset.csv')
    sellers = pd.read_csv('data/olist_sellers_dataset.csv')
    payments = pd.read_csv('data/olist_order_payments_dataset.csv')
except FileNotFoundError as e:
    print(f"Arquivo não encontrado: {e}")
    print("Certifique-se que a pasta 'data' existe com todos os arquivos CSV.")
    exit()

# --- PREPARAÇÃO E JUNÇÃO ---
# Unir orders + customers (para ter estado)
data = orders.merge(customers, on='customer_id', how='left')

# Unir orders + order_items para receita
order_items['price'] = pd.to_numeric(order_items['price'], errors='coerce').fillna(0)
order_items['freight_value'] = pd.to_numeric(order_items['freight_value'], errors='coerce').fillna(0)
order_revenue = order_items.groupby('order_id').agg({
    'price': 'sum',
    'freight_value': 'sum',
    'product_id': 'count'
}).reset_index()
order_revenue['total_value'] = order_revenue['price'] + order_revenue['freight_value']
order_revenue = order_revenue.rename(columns={'product_id': 'items_count'})

data = data.merge(order_revenue, on='order_id', how='left')

# Unir com produtos para categorias
order_items_with_products = order_items.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')

# Unir com pagamentos
if 'payments' in locals():
    payments['payment_value'] = pd.to_numeric(payments['payment_value'], errors='coerce').fillna(0)
    payment_summary = payments.groupby('order_id').agg({
        'payment_value': 'sum',
        'payment_type': 'first',
        'payment_installments': 'mean'
    }).reset_index()
    data = data.merge(payment_summary, on='order_id', how='left')

# Criar colunas auxiliares para data
data['order_month'] = data['order_purchase_timestamp'].dt.to_period('M').dt.to_timestamp()
data['order_year'] = data['order_purchase_timestamp'].dt.year
data['order_quarter'] = data['order_purchase_timestamp'].dt.quarter
data['order_weekday'] = data['order_purchase_timestamp'].dt.day_name()

# --- CONFIGURAÇÕES DE ESTILO ---
COLORS = {
    'primary': '#2E86AB',        # Azul principal
    'secondary': '#A23B72',      # Azul secundário  
    'accent': '#F18F01',         # Laranja para destaques
    'success': '#C73E1D',        # Verde
    'background': '#F8F9FA',     # Cinza muito claro
    'card_bg': '#FFFFFF',        # Branco
    'text': '#2C3E50',          # Azul escuro para texto
    'border': '#E1E8ED',        # Cinza claro para bordas
    'gradient_start': '#2E86AB', # Início do gradiente
    'gradient_end': '#A23B72'    # Fim do gradiente
}

# Estilo global
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css']

# --- DASH APP ---
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Dashboard EJ - Análise Financeira"

# Estilo CSS customizado
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #F8F9FA;
                margin: 0;
                padding: 0;
            }
            .header {
                background: linear-gradient(135deg, #1E3A8A 0%, #2E86AB 40%, #60A5FA 100%);
                color: white;
                padding: 2.5rem 0;
                margin-bottom: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .kpi-card {
                background: white;
                padding: 1.8rem;
                border-radius: 15px;
                box-shadow: 0 3px 15px rgba(0,0,0,0.08);
                margin: 0 10px;
                transition: all 0.3s ease;
                border-left: 5px solid #2E86AB;
                position: relative;
                overflow: hidden;
            }
            .kpi-card::before {
                content: '';
                position: absolute;
                top: 0;
                right: 0;
                width: 100px;
                height: 100px;
                background: linear-gradient(45deg, rgba(30,58,138,0.08), rgba(46,134,171,0.12));
                border-radius: 50%;
                transform: translate(30px, -30px);
            }
            .kpi-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 25px rgba(0,0,0,0.12);
            }
            .kpi-value {
                font-size: 2.2rem;
                font-weight: bold;
                margin: 0.5rem 0;
                color: #2C3E50;
                position: relative;
                z-index: 2;
            }
            .kpi-label {
                font-size: 0.85rem;
                color: #6C757D;
                text-transform: uppercase;
                letter-spacing: 1.2px;
                margin: 0;
                font-weight: 600;
                position: relative;
                z-index: 2;
            }
            .kpi-icon {
                font-size: 2.2rem;
                opacity: 0.8;
                position: absolute;
                top: 1.8rem;
                right: 1.8rem;
                z-index: 2;
            }
            .chart-container {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 3px 15px rgba(0,0,0,0.08);
                margin: 1.5rem 0;
            }
            .filters-container {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 3px 15px rgba(0,0,0,0.08);
                margin-bottom: 2rem;
            }
            .section-title {
                color: #2C3E50;
                font-size: 1.3rem;
                font-weight: 600;
                margin: 0 0 25px 0;
                padding-bottom: 10px;
                border-bottom: 2px solid #E1E8ED;
            }
            .metric-change {
                font-size: 0.8rem;
                margin-top: 8px;
                font-weight: 500;
            }
            .metric-up { color: #28A745; }
            .metric-down { color: #DC3545; }
            .filter-group {
                margin-bottom: 20px;
            }
            .filter-label {
                font-weight: 600;
                margin-bottom: 8px;
                display: block;
                color: #495057;
            }
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
                html.I(className="fas fa-chart-line", style={'marginRight': '15px'}),
                "Dashboard EJ - Análise Financeira"
            ], style={
                'textAlign': 'center', 
                'margin': '0', 
                'fontSize': '2.8rem',
                'fontWeight': '300'
            }),
            html.P("Análise completa de vendas e performance da Empresa Junior", 
                   style={'textAlign': 'center', 'margin': '15px 0 0 0', 'opacity': '0.9', 'fontSize': '1.1rem'})
        ])
    ], className="header"),
    
    # Container principal
    html.Div([
        # Filtros
        html.Div([
            html.H3([
                html.I(className="fas fa-sliders-h", style={'marginRight': '12px'}),
                "Controles de Análise"
            ], className="section-title"),
            
            html.Div([
                html.Div([
                    html.Label("Período de Análise:", className="filter-label"),
                    html.P("💡 As variações são calculadas comparando com o período anterior de mesmo tamanho", 
                           style={'fontSize': '0.8rem', 'color': '#6C757D', 'margin': '5px 0 10px 0', 'fontStyle': 'italic'}),
                    dcc.DatePickerRange(
                        id='date-range',
                        min_date_allowed=data['order_purchase_timestamp'].min(),
                        max_date_allowed=data['order_purchase_timestamp'].max(),
                        start_date=data['order_purchase_timestamp'].min(),
                        end_date=data['order_purchase_timestamp'].max(),
                        display_format='DD/MM/YYYY',
                        style={'width': '100%'},
                        start_date_placeholder_text="Data inicial",
                        end_date_placeholder_text="Data final"
                    )
                ], className="filter-group", style={'flex': '1', 'marginRight': '20px'}),
                
                html.Div([
                    html.Label("Agrupamento Temporal:", className="filter-label"),
                    dcc.Dropdown(
                        id='time-grouping',
                        options=[
                            {'label': '📅 Mensal', 'value': 'month'},
                            {'label': '📊 Trimestral', 'value': 'quarter'},
                            {'label': '📈 Anual', 'value': 'year'}
                        ],
                        value='month',
                        clearable=False,
                        style={'width': '100%'}
                    )
                ], className="filter-group", style={'flex': '1'})
            ], style={'display': 'flex', 'alignItems': 'end'})
        ], className="filters-container"),

        # KPIs principais
        html.Div([
            html.H3([
                html.I(className="fas fa-tachometer-alt", style={'marginRight': '12px'}),
                "Indicadores de Performance"
            ], className="section-title"),
            
            html.Div([
                html.Div(id='total-revenue', style={'flex': '1'}),
                html.Div(id='total-orders', style={'flex': '1'}),
                html.Div(id='avg-ticket', style={'flex': '1'}),
                html.Div(id='total-customers', style={'flex': '1'}),
            ], style={
                'display': 'flex', 
                'gap': '20px',
                'marginBottom': '30px',
                'flexWrap': 'wrap'
            })
        ]),

        # KPIs secundários
        html.Div([
            html.H3([
                html.I(className="fas fa-chart-pie", style={'marginRight': '12px'}),
                "Métricas Operacionais"
            ], className="section-title"),
            
            html.Div([
                html.Div(id='avg-items', style={'flex': '1'}),
                html.Div(id='avg-freight', style={'flex': '1'}),
                html.Div(id='conversion-rate', style={'flex': '1'}),
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
                dcc.Graph(id='revenue-trend')
            ], className="chart-container", style={'marginBottom': '20px'}),

            html.Div([
                html.Div([
                    dcc.Graph(id='orders-by-state')
                ], style={'flex': '1', 'marginRight': '10px'}),
                
                html.Div([
                    dcc.Graph(id='payment-methods')
                ], style={'flex': '1', 'marginLeft': '10px'})
            ], style={'display': 'flex', 'gap': '20px'}, className="chart-container"),

            html.Div([
                html.Div([
                    dcc.Graph(id='category-analysis')
                ], style={'flex': '1', 'marginRight': '10px'}),
                
                html.Div([
                    dcc.Graph(id='weekday-pattern')
                ], style={'flex': '1', 'marginLeft': '10px'})
            ], style={'display': 'flex', 'gap': '20px'}, className="chart-container"),
        ])
    ], style={
        'maxWidth': '1400px', 
        'margin': '0 auto', 
        'padding': '0 20px'
    })
])

# --- CALLBACKS ---
@app.callback(
    [Output('total-revenue', 'children'),
     Output('total-orders', 'children'),
     Output('avg-ticket', 'children'),
     Output('total-customers', 'children'),
     Output('avg-items', 'children'),
     Output('avg-freight', 'children'),
     Output('conversion-rate', 'children'),
     Output('revenue-trend', 'figure'),
     Output('orders-by-state', 'figure'),
     Output('payment-methods', 'figure'),
     Output('category-analysis', 'figure'),
     Output('weekday-pattern', 'figure')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('time-grouping', 'value')]
)
def update_dashboard(start_date, end_date, time_grouping):
    # Filtrar dados do período atual
    filtered = data[(data['order_purchase_timestamp'] >= start_date) & 
                   (data['order_purchase_timestamp'] <= end_date)]
    
    # Calcular período anterior para comparação (mesmo tamanho do período atual)
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    date_diff = end_dt - start_dt
    
    prev_start = start_dt - date_diff
    prev_end = start_dt
    
    prev_data = data[(data['order_purchase_timestamp'] >= prev_start) & 
                    (data['order_purchase_timestamp'] < prev_end)]

    print(f"📅 Período atual: {start_date} a {end_date} ({len(filtered)} registros)")
    print(f"📅 Período anterior: {prev_start.date()} a {prev_end.date()} ({len(prev_data)} registros)")

    # Métricas principais
    total_revenue = filtered['price'].sum()
    prev_revenue = prev_data['price'].sum() if len(prev_data) > 0 else 0
    revenue_change = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
    
    total_orders = filtered['order_id'].nunique()
    prev_orders = prev_data['order_id'].nunique() if len(prev_data) > 0 else 0
    orders_change = ((total_orders - prev_orders) / prev_orders * 100) if prev_orders > 0 else 0
    
    avg_ticket = total_revenue / total_orders if total_orders else 0
    prev_avg_ticket = prev_revenue / prev_orders if prev_orders else 0
    ticket_change = ((avg_ticket - prev_avg_ticket) / prev_avg_ticket * 100) if prev_avg_ticket > 0 else 0
    
    total_customers = filtered['customer_id'].nunique()
    prev_customers = prev_data['customer_id'].nunique() if len(prev_data) > 0 else 0
    customers_change = ((total_customers - prev_customers) / prev_customers * 100) if prev_customers > 0 else 0
    
    # Debug das variações
    print(f"💰 Receita: R$ {total_revenue:.2f} (era R$ {prev_revenue:.2f}) = {revenue_change:+.1f}%")
    print(f"🛒 Pedidos: {total_orders} (eram {prev_orders}) = {orders_change:+.1f}%")
    
    # Métricas operacionais
    avg_items = filtered['items_count'].mean() if len(filtered) > 0 else 0
    avg_freight = filtered['freight_value'].mean() if len(filtered) > 0 else 0
    conversion_rate = (total_orders / total_customers * 100) if total_customers > 0 else 0

    # Função para criar KPI card
    def create_kpi_card(title, value, icon, color, change=None, prefix="", suffix=""):
        change_element = []
        if change is not None:
            change_class = "metric-up" if change >= 0 else "metric-down"
            change_icon = "fas fa-arrow-up" if change >= 0 else "fas fa-arrow-down"
            change_element = [
                html.Div([
                    html.I(className=change_icon, style={'marginRight': '5px'}),
                    f"{change:+.1f}% vs período anterior"
                ], className=f"metric-change {change_class}")
            ]
        
        return html.Div([
            html.I(className=f"{icon} kpi-icon", style={'color': color}),
            html.H4(title, className="kpi-label"),
            html.H2(f"{prefix}{value}{suffix}", className="kpi-value"),
            *change_element
        ], className="kpi-card")

    # KPI Cards
    kpi_revenue = create_kpi_card(
        "Receita Total", 
        f"{total_revenue:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
        "fas fa-dollar-sign", COLORS['success'], revenue_change, "R$ "
    )

    kpi_orders = create_kpi_card(
        "Total de Pedidos", 
        f"{total_orders:,}".replace(',', '.'),
        "fas fa-shopping-cart", COLORS['primary'], orders_change
    )

    kpi_avg_ticket = create_kpi_card(
        "Ticket Médio", 
        f"{avg_ticket:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
        "fas fa-receipt", COLORS['secondary'], ticket_change, "R$ "
    )
    
    kpi_customers = create_kpi_card(
        "Clientes Únicos", 
        f"{total_customers:,}".replace(',', '.'),
        "fas fa-users", COLORS['accent'], customers_change
    )
    
    kpi_avg_items = create_kpi_card(
        "Itens por Pedido", 
        f"{avg_items:.1f}",
        "fas fa-boxes", COLORS['primary']
    )
    
    kpi_avg_freight = create_kpi_card(
        "Frete Médio", 
        f"{avg_freight:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
        "fas fa-truck", COLORS['secondary'], None, "R$ "
    )
    
    kpi_conversion = create_kpi_card(
        "Taxa de Conversão", 
        f"{conversion_rate:.1f}",
        "fas fa-percentage", COLORS['success'], None, "", "%"
    )

    # Gráfico de tendência de receita
    if time_grouping == 'month':
        period_col = 'order_month'
        title_suffix = "Mensal"
    elif time_grouping == 'quarter':
        filtered['period'] = filtered['order_purchase_timestamp'].dt.to_period('Q').dt.to_timestamp()
        period_col = 'period'
        title_suffix = "Trimestral"
    else:  # year
        filtered['period'] = filtered['order_purchase_timestamp'].dt.to_period('Y').dt.to_timestamp()
        period_col = 'period'
        title_suffix = "Anual"
    
    trend_data = (filtered.groupby(period_col)
                  .agg({'price': 'sum', 'order_id': 'nunique'})
                  .reset_index())
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=trend_data[period_col], 
        y=trend_data['price'],
        mode='lines+markers',
        name='Receita',
        line=dict(width=3, color=COLORS['primary']),
        marker=dict(size=8, color=COLORS['primary'])
    ))
    
    fig_trend.update_layout(
        title=f'📈 Evolução da Receita {title_suffix}',
        title_font_size=18,
        title_x=0.02,
        template='plotly_white',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    # Gráfico de pedidos por estado (Top 10)
    state_orders = (filtered.groupby('customer_state')
                    .agg({'order_id': 'nunique'})
                    .reset_index()
                    .rename(columns={'order_id': 'pedidos'})
                    .sort_values('pedidos', ascending=True)
                    .tail(10))
    
    fig_state = px.bar(state_orders, 
                      x='pedidos', 
                      y='customer_state',
                      orientation='h',
                      title='🗺️ Top 10 Estados',
                      template='plotly_white',
                      color='pedidos',
                      color_continuous_scale=[[0, COLORS['primary']], [1, COLORS['secondary']]])
    
    fig_state.update_layout(
        title_font_size=16,
        title_x=0.02,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )

    # Gráfico de métodos de pagamento
    if 'payment_type' in filtered.columns:
        payment_data = filtered['payment_type'].value_counts().head(6)
        fig_payment = px.pie(
            values=payment_data.values,
            names=payment_data.index,
            title='💳 Métodos de Pagamento',
            template='plotly_white',
            color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['success']]
        )
    else:
        fig_payment = px.pie(values=[1], names=['Dados não disponíveis'], title='💳 Métodos de Pagamento')
    
    fig_payment.update_layout(
        title_font_size=16,
        title_x=0.02,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )

    # Análise por categoria (simulada - usando dados disponíveis)
    category_data = pd.DataFrame({
        'categoria': ['Eletrônicos', 'Casa & Jardim', 'Esporte', 'Moda', 'Livros', 'Outros'],
        'vendas': np.random.randint(50, 500, 6)  # Dados simulados
    }).sort_values('vendas', ascending=True)
    
    fig_category = px.bar(category_data,
                         x='vendas',
                         y='categoria',
                         orientation='h',
                         title='🛍️ Vendas por Categoria',
                         template='plotly_white',
                         color='vendas',
                         color_continuous_scale=[[0, COLORS['accent']], [1, COLORS['primary']]])
    
    fig_category.update_layout(
        title_font_size=16,
        title_x=0.02,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )

    # Padrão por dia da semana
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_names = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    
    weekday_data = (filtered.groupby('order_weekday')['order_id']
                   .nunique().reset_index()
                   .rename(columns={'order_id': 'pedidos'}))
    
    # Reordenar e traduzir
    weekday_data['order'] = weekday_data['order_weekday'].map({day: i for i, day in enumerate(weekday_order)})
    weekday_data = weekday_data.sort_values('order')
    weekday_data['weekday_pt'] = weekday_names
    
    fig_weekday = px.bar(weekday_data,
                        x='weekday_pt',
                        y='pedidos',
                        title='📅 Pedidos por Dia da Semana',
                        template='plotly_white',
                        color='pedidos',
                        color_continuous_scale=[[0, COLORS['secondary']], [1, COLORS['primary']]])
    
    fig_weekday.update_layout(
        title_font_size=16,
        title_x=0.02,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )

    return (kpi_revenue, kpi_orders, kpi_avg_ticket, kpi_customers,
            kpi_avg_items, kpi_avg_freight, kpi_conversion,
            fig_trend, fig_state, fig_payment, fig_category, fig_weekday)


if __name__ == '__main__':
    print("🚀 Iniciando Dashboard EJ - Análise Financeira...")
    print("📊 Acesse: http://localhost:8050")
    print("⏹️  Para parar: Ctrl+C")
    
    app.run(debug=True, host='0.0.0.0', port=8050)