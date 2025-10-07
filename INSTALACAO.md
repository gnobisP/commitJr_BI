# 🚀 Guia de Instalação e Configuração

## 📋 Pré-requisitos

-   **Python 3.8+** instalado
-   **Git** para clonagem do repositório
-   Aproximadamente **50MB** de espaço livre

## 🛠️ Instalação Passo a Passo

### 1️⃣ **Clonar o Repositório**

```bash
git clone https://github.com/gnobisP/commitJr_BI.git
cd commitJr_BI
```

### 2️⃣ **Configurar Ambiente Virtual** (Recomendado)

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# No macOS/Linux:
source venv/bin/activate

# No Windows:
venv\Scripts\activate
```

### 3️⃣ **Instalar Dependências**

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Executando os Dashboards

### 🏢 **Dashboard Empresa Junior**

```bash
# Com ambiente virtual ativado
python app_ej.py

# Acesse: http://localhost:8051
```

### 🛒 **Dashboard E-commerce**

```bash
# Com ambiente virtual ativado
python app.py

# Acesse: http://localhost:8050
```

## 🗂️ Estrutura de Dados

### 📊 **Dados EJ** (`fake_data/`)

-   ✅ `area_projeto.csv` - Áreas de atuação
-   ✅ `empresa.csv` - Clientes empresariais
-   ✅ `pessoa.csv` - Contatos dos clientes
-   ✅ `servico.csv` - Projetos realizados
-   ✅ `despesa.csv` - Gastos operacionais
-   ✅ `tributo.csv` - Impostos por projeto

### 🛒 **Dados E-commerce** (`data/`)

-   `olist_orders_dataset.csv`
-   `olist_customers_dataset.csv`
-   `olist_order_items_dataset.csv`
-   `olist_products_dataset.csv`
-   `olist_sellers_dataset.csv`
-   `olist_order_payments_dataset.csv`

## 🔧 Solução de Problemas

### ❌ **Erro: ModuleNotFoundError**

```bash
# Verifique se o ambiente virtual está ativado
source venv/bin/activate  # macOS/Linux
# OU
venv\Scripts\activate     # Windows

# Reinstale as dependências
pip install pandas dash plotly numpy
```

### ❌ **Erro: FileNotFoundError**

-   Verifique se as pastas `fake_data/` e `data/` existem
-   Certifique-se que todos os arquivos CSV estão presentes
-   Execute o comando na pasta raiz do projeto

### ❌ **Erro: Port already in use**

```bash
# Se a porta 8051 estiver ocupada, altere no código:
# app.run(debug=True, host='0.0.0.0', port=8052)
```

## 🎨 Personalização

### 🎨 **Alterar Cores**

Modifique o dicionário `COLORS` em `app_ej.py`:

```python
COLORS = {
    'primary': '#1E40AF',    # Cor principal
    'secondary': '#7C3AED',  # Cor secundária
    'accent': '#F59E0B',     # Cor de destaque
    # ...
}
```

### 📊 **Adicionar Novos KPIs**

1. Calcule a métrica no callback principal
2. Crie um novo card com `create_kpi_card_ej()`
3. Adicione ao layout HTML

## 📱 Acesso Remoto

Para acessar de outros dispositivos na mesma rede:

```python
# Altere no final do arquivo:
app.run(debug=True, host='0.0.0.0', port=8051)

# Acesse via: http://[IP_DO_SERVIDOR]:8051
```

## 🔒 Modo Produção

Para deploy em produção:

```python
# Desative o debug
app.run(debug=False, host='0.0.0.0', port=8051)
```

## 📞 Suporte

-   🐛 **Bugs**: [GitHub Issues](https://github.com/gnobisP/commitJr_BI/issues)
-   📧 **Email**: suporte@empresajunior.com
-   📖 **Documentação**: [Wiki do Projeto](https://github.com/gnobisP/commitJr_BI/wiki)
