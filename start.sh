#!/bin/bash
# Script de inicialização do Dashboard EJ

echo "🚀 Iniciando Dashboard Empresa Junior..."
echo ""

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências se necessário
if [ ! -f "venv/.installed" ]; then
    echo "📥 Instalando dependências..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Verificar se os dados existem
if [ ! -d "fake_data" ]; then
    echo "❌ Pasta 'fake_data' não encontrada!"
    echo "   Certifique-se de que os dados da EJ estão na pasta fake_data/"
    exit 1
fi

# Executar o dashboard
echo "✅ Tudo pronto! Iniciando dashboard..."
echo ""
python app.py