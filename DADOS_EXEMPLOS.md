# 📊 Exemplos de Dados e Estruturas

## 🏢 Dados da Empresa Junior

### 📋 **area_projeto.csv**

```csv
id_area,nome_area
1,Desenvolvimento Web
2,Criação de Jogos
3,Automação
```

### 🏢 **empresa.csv** (exemplo)

```csv
id_empresa,nome,cnpj,telefone,email,capital_social,endereco,area_empresa
1,Tech Solutions Ltda,12.345.678/0001-90,+55 11 9999-8888,contato@tech.com,50000,"Rua das Flores, 123",Tecnologia
2,Green Energy SA,98.765.432/0001-12,+55 21 8888-7777,info@green.com,100000,"Av. Sustentável, 456",Energia
```

### 👤 **pessoa.csv** (exemplo)

```csv
id_pessoa,nome,email,telefone
1,João Silva,joao@tech.com,+55 11 99999-0001
2,Maria Santos,maria@green.com,+55 21 88888-0002
```

### 🎯 **servico.csv** (exemplo)

```csv
id_servico,titulo,descricao,valor,data_inicio,data_fim,status,id_area,id_pessoa,id_empresa
1,Website Institucional,Desenvolvimento completo de site,5000.00,2024-01-15,2024-03-15,Concluído,1,1,1
2,Sistema de Gestão,ERP personalizado para empresa,15000.00,2024-02-01,,Em andamento,1,,2
3,Game Mobile,Jogo educativo para crianças,8000.00,2024-01-10,2024-04-10,Concluído,2,2,
```

### 💸 **despesa.csv** (exemplo)

```csv
id_despesa,descricao,valor,data,categoria
1,Licença Adobe Creative Suite,299.90,2024-01-15,Licença para produção
2,Curso de React.js,450.00,2024-02-01,Cursos
3,Manutenção servidor,120.00,2024-01-30,Manutenção
```

### 💰 **tributo.csv** (exemplo)

```csv
id_tributo,tipo,percentual,id_servico
1,ISS,5.0,1
2,COFINS,3.0,1
3,PIS,0.65,1
4,IRPJ,15.0,2
5,CSLL,9.0,2
```

## 🎯 KPIs Calculados pelo Dashboard EJ

### 📊 **Métricas Principais**

-   **Receita Total**: Soma de todos os valores dos serviços
-   **Receita Líquida**: Receita total - tributos estimados
-   **Ticket Médio**: Receita total ÷ número de projetos
-   **Taxa de Conclusão**: (Projetos concluídos ÷ total de projetos) × 100

### 📈 **Análises Visuais**

1. **Evolução da Receita**: Gráfico de linha por mês
2. **Projetos por Área**: Distribuição horizontal
3. **Status dos Projetos**: Gráfico de pizza
4. **Clientes por Área**: Análise de segmentação
5. **Carga Tributária**: Percentual médio por área
6. **Despesas por Categoria**: Ranking de gastos

## 🔗 Relacionamentos dos Dados

```
SERVIÇOS (servico.csv)
├── id_area → ÁREAS (area_projeto.csv)
├── id_pessoa → PESSOAS (pessoa.csv)
├── id_empresa → EMPRESAS (empresa.csv)
└── id_servico ← TRIBUTOS (tributo.csv)

DESPESAS (despesa.csv) [Independente]
```

## 🎨 Campos Calculados

### 💰 **Tributos por Serviço**

```python
# Agregação por serviço
total_tributos = soma(percentual) por id_servico
media_tributos = média(percentual) por id_servico
qtd_tributos = contagem por id_servico

# Valores monetários
valor_tributos_estimado = valor × (total_tributos ÷ 100)
valor_liquido = valor - valor_tributos_estimado
```

### 📅 **Campos Temporais**

```python
mes_inicio = data_inicio agrupada por mês
ano_inicio = data_inicio agrupada por ano
trimestre_inicio = data_inicio agrupada por trimestre
```

## 📊 Filtros Disponíveis

### 🗓️ **Filtro de Data**

-   **Período**: Data início até data fim
-   **Formato**: DD/MM/YYYY
-   **Padrão**: Todo o período disponível

### 🎯 **Filtro de Área**

-   **Opções**: Todas as áreas + áreas individuais
-   **Valores**: Desenvolvimento Web, Criação de Jogos, Automação
-   **Padrão**: "Todas as Áreas"

### ✅ **Filtro de Status**

-   **Opções**: Todos os status + status individuais
-   **Valores**: Concluído, Em andamento, Cancelado
-   **Padrão**: "Todos os Status"

## 🎯 Comparação: EJ vs E-commerce

| Aspecto        | Dashboard EJ        | Dashboard E-commerce |
| -------------- | ------------------- | -------------------- |
| **Foco**       | Projetos e Serviços | Vendas e Produtos    |
| **Clientes**   | Empresas B2B        | Consumidores B2C     |
| **Receita**    | Por projeto         | Por pedido           |
| **Tempo**      | Datas de projeto    | Datas de compra      |
| **Análise**    | Áreas/Status        | Estados/Categorias   |
| **Tributação** | Por serviço         | Por pagamento        |

## 💡 Dicas de Uso

### 🎯 **Para Gestores EJ**

-   Use filtros de período para análises mensais/trimestrais
-   Monitore a taxa de conclusão de projetos
-   Acompanhe a carga tributária por área
-   Analise despesas por categoria para controle de custos

### 📊 **Para Análise Financeira**

-   Compare receita bruta vs líquida
-   Identifique áreas mais rentáveis
-   Monitore padrões sazonais na receita
-   Controle despesas operacionais

### 🎨 **Para Customização**

-   Modifique cores no dicionário `COLORS`
-   Adicione novos KPIs nos callbacks
-   Personalize filtros conforme necessidade
-   Ajuste layout CSS para branding da EJ
