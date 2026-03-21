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

**A Solução:** Uma API inteligente que avalia a carga, traça a rota, calcula custos de diesel/manutenção e passa os dados por um modelo de regressão treinado para entender o comportamento do mercado, sugerindo o preço "na mosca".

---

## ✨ Principais Funcionalidades

- **Roteirização Automática:** Integração com OSRM/Nominatim para calcular distâncias exatas (km) entre cidades e estados.
- **Compliance ANTT:** Cálculo automático do Piso Mínimo da ANTT com base em eixos do veículo e quilometragem.
- **Cálculo FTL e LTL:** Suporte para carga Lotação (caminhão fechado) e Fracionada (rateio de custos por peso cúbico e taxas operacionais).
- **Machine Learning Integrado:** Modelo preditivo (Scikit-Learn/Random Forest) que avalia o custo técnico e sugere uma margem de lucro baseada na probabilidade de fechamento.
- **Dashboard Web:** Interface responsiva, limpa e moderna construída com Tailwind CSS.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python + FastAPI
- **Banco de Dados:** PostgreSQL (Hospedado no Neon.tech) + SQLAlchemy (ORM)
- **Inteligência Artificial:** Pandas, NumPy e Scikit-Learn
- **Integrações (APIs):** OpenRouteService (Distâncias)
- **Frontend:** HTML5, JavaScript Vanilla (Fetch API) e Tailwind CSS
- **Deploy:** Render (CI/CD Automático)

---

## 🚀 Como rodar o projeto localmente

1. Clone o repositório:
```bash
git clone https://github.com/vsfrancisco/frete-ia.git
