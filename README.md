# 🚚 Frete IA Pro - Inteligência Artificial para Logística

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)

Aplicação SaaS (Software as a Service) desenvolvida para resolver um dos maiores problemas de pequenas e médias transportadoras: **a precificação incorreta de fretes**. 

O sistema cruza dados automáticos de roteirização, tabela oficial do governo (ANTT) e utiliza **Machine Learning** para sugerir a margem de lucro ideal, maximizando as chances de fechamento da carga.

🌐 **Acesse a aplicação ao vivo:** [https://frete-ia-app.onrender.com/]

---

## 🎯 O Problema vs. A Solução

**O Problema:** Muitas transportadoras calculam fretes de cabeça ou em planilhas defasadas. Isso resulta em orçamentos abaixo da Tabela Mínima da ANTT (gerando multas) ou muito acima do mercado (perdendo o cliente para a concorrência).

**A Solução:** Uma API inteligente que avalia a carga, traça a rota, calcula custos preditivos (diesel, manutenção, pedágio e seguro) e passa os dados por um modelo de regressão treinado para entender o comportamento do mercado, sugerindo o preço "na mosca".

---

## ✨ Principais Funcionalidades

- **Cotação Spot (Multi-Transportadora):** Motor de leilão reverso que simula todas as transportadoras da base de uma só vez e exibe um ranking automático com a opção de maior lucro/menor custo.
- **Roteirização e Custos Preditivos:** Integração para cálculo de distância e estimativa inteligente de Pedágios (por eixo/UF), Variação de Diesel regional e Seguro *Ad Valorem* da carga.
- **Compliance ANTT:** Cálculo obrigatório do Piso Mínimo da ANTT atualizado, garantindo proteção contra multas fiscais.
- **Machine Learning e Risco:** Modelo preditivo que avalia o risco da rota (ex: RJ vs SP) e o custo técnico para sugerir a melhor margem de venda e a % de probabilidade de fechamento.
- **CRM e Dashboard Financeiro:** Painel completo com histórico de cotações, geração de PDF para o cliente, cadastro de regras de descontos (Clientes VIP) e acompanhamento de faturamento/lucro estimado.
- **Proteção de Acesso:** Sistema de segurança HTTP Basic Auth embutido para proteger a plataforma contra acessos não autorizados.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python + FastAPI
- **Banco de Dados:** PostgreSQL (Hospedado no Neon.tech) + SQLAlchemy (ORM)
- **Inteligência Artificial:** Pandas, NumPy e Scikit-Learn
- **Geração de Relatórios:** ReportLab (Exportação em PDF)
- **Integrações (APIs):** OpenRouteService (Distâncias)
- **Frontend:** HTML5, JavaScript Vanilla (Fetch API) e Tailwind CSS
- **Deploy:** Render (CI/CD Automático)

---

## 🚀 Como rodar o projeto localmente

1. Clone o repositório:
```bash
git clone https://github.com/vsfrancisco/frete-ia.git
cd frete-ia
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o Banco de Dados:
- Crie um arquivo `.env` na raiz do projeto contendo a sua URI do PostgreSQL (Neon.tech).
- Exemplo: `DATABASE_URL=postgresql://usuario:senha@host/banco`

5. Inicie o servidor:
```bash
uvicorn app.main:app --reload
```
Acesse `http://localhost:8000` no seu navegador usando as credenciais master cadastradas no código.