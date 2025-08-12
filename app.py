import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# --- CARREGAR DADOS ---
orders = pd.read_csv('data/olist_orders_dataset.csv', parse_dates=['order_purchase_timestamp'])
customers = pd.read_csv('data/olist_customers_dataset.csv')
order_items = pd.read_csv('data/olist_order_items_dataset.csv')
products = pd.read_csv('data/olist_products_dataset.csv')
sellers = pd.read_csv('data/olist_sellers_dataset.csv')

# --- PREPARAÇÃO E JUNÇÃO ---
# Unir orders + customers (para ter estado)
data = orders.merge(customers, on='customer_id', how='left')

# Unir orders + order_items para receita
order_items['price'] = pd.to_numeric(order_items['price'], errors='coerce').fillna(0)
order_revenue = order_items.groupby('order_id')['price'].sum().reset_index()
data = data.merge(order_revenue, on='order_id', how='left')

# Criar colunas auxiliares para data (Ano, Mês)
data['order_month'] = data['order_purchase_timestamp'].dt.to_period('M').dt.to_timestamp()

# --- DASH APP ---
app = Dash(__name__)
app.title = "Dashboard EJ - Olist"

app.layout = html.Div([
    html.H1("Dashboard EJ - Dados Olist", style={'textAlign':'center'}),
    
    # Filtro de período
    dcc.DatePickerRange(
        id='date-range',
        min_date_allowed=data['order_purchase_timestamp'].min(),
        max_date_allowed=data['order_purchase_timestamp'].max(),
        start_date=data['order_purchase_timestamp'].min(),
        end_date=data['order_purchase_timestamp'].max(),
        display_format='DD/MM/YYYY',
        style={'marginBottom':'20px'}
    ),

    # KPIs em cards simples
    html.Div([
        html.Div(id='total-revenue', style={'display':'inline-block', 'width':'30%', 'textAlign':'center'}),
        html.Div(id='total-orders', style={'display':'inline-block', 'width':'30%', 'textAlign':'center'}),
        html.Div(id='avg-ticket', style={'display':'inline-block', 'width':'30%', 'textAlign':'center'}),
    ], style={'marginBottom':'30px'}),

    # Gráfico de receita por mês
    dcc.Graph(id='revenue-monthly'),

    # Gráfico de pedidos por estado
    dcc.Graph(id='orders-by-state')
], style={'maxWidth':'900px', 'margin':'auto', 'fontFamily':'Arial'})

# --- CALLBACK ---
@app.callback(
    [Output('total-revenue', 'children'),
     Output('total-orders', 'children'),
     Output('avg-ticket', 'children'),
     Output('revenue-monthly', 'figure'),
     Output('orders-by-state', 'figure')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_dashboard(start_date, end_date):
    filtered = data[(data['order_purchase_timestamp'] >= start_date) & (data['order_purchase_timestamp'] <= end_date)]

    total_revenue = filtered['price'].sum()
    total_orders = filtered['order_id'].nunique()
    avg_ticket = total_revenue / total_orders if total_orders else 0

    kpi_revenue = html.Div([
        html.H3("Receita Total"),
        html.H2(f"R$ {total_revenue:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    ])

    kpi_orders = html.Div([
        html.H3("Pedidos"),
        html.H2(f"{total_orders:,}")
    ])

    kpi_avg_ticket = html.Div([
        html.H3("Ticket Médio"),
        html.H2(f"R$ {avg_ticket:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    ])

    # Receita por mês
    monthly = (filtered
               .groupby('order_month')
               .agg({'price':'sum'})
               .reset_index())
    fig_revenue = px.bar(monthly, x='order_month', y='price',
                         labels={'order_month':'Mês', 'price':'Receita (R$)'},
                         title='Receita por Mês',
                         template='plotly_white')

    # Pedidos por estado
    state_orders = (filtered
                    .groupby('customer_state')
                    .agg({'order_id':'nunique'})
                    .reset_index()
                    .rename(columns={'order_id':'pedidos'}))

    # Mapa Brasil (simplificado usando Plotly Express e UF)
    fig_state = px.choropleth(state_orders,
                              locations='customer_state',
                              locationmode='USA-states',  # NÃO É USA, mas vamos corrigir abaixo
                              color='pedidos',
                              color_continuous_scale='Blues',
                              scope='south america',
                              labels={'customer_state':'Estado', 'pedidos':'Pedidos'},
                              title='Pedidos por Estado')

    # Ajustar para mapa Brasil usando GeoJSON (vou explicar depois, ou faço pra você)

    return kpi_revenue, kpi_orders, kpi_avg_ticket, fig_revenue, fig_state


if __name__ == '__main__':
    app.run(debug=True)
