# H-XZ-V2: Ferramenta de Pentest com Dashboard Inteligente

## Visão Geral

**H-XZ-V2** é uma ferramenta de teste de penetração (pentest) avançada que combina scripts de segurança tradicionais com inteligência artificial. O projeto oferece um dashboard interativo hospedado no GitHub Pages para visualização de resultados, análise de vulnerabilidades e recomendações de remediação geradas por IA (Gemini ou Groq).

## Características Principais

* **Scanner de Vulnerabilidades**: Detecta portas abertas, serviços expostos e configurações inseguras.
* **Análise com IA**: Integração com Google Gemini ou Groq para análise contextual de vulnerabilidades e sugestões de correção.
* **Dashboard Interativo**: Interface web moderna para visualizar resultados de scans em tempo real.
* **Relatórios Detalhados**: Exportação de relatórios em JSON e HTML com análise de risco.
* **GitHub Pages**: Hospedagem gratuita do dashboard diretamente no GitHub.

## Arquitetura

```
H-XZ-V2/
├── index.html                 # Dashboard principal
├── assets/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── dashboard.js
│       └── api-handler.js
├── scripts/
│   ├── pentest.py            # Script principal de pentest
│   ├── ai_analyzer.py        # Análise com IA
│   └── requirements.txt
├── docs/
│   └── API.md
└── .github/
    └── workflows/
        └── deploy.yml        # CI/CD para GitHub Pages
```

## Como Usar

### 1. Instalação

```bash
git clone https://github.com/OffModzKkkkj/H-XZ-V2.git
cd H-XZ-V2
pip install -r scripts/requirements.txt
```

### 2. Configurar Chaves de API

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_aqui
# ou
GROQ_API_KEY=sua_chave_aqui
```

### 3. Executar Pentest

```bash
python scripts/pentest.py --target 192.168.1.0/24 --output results.json
```

### 4. Gerar Dashboard

```bash
python scripts/generate_dashboard.py --input results.json --output index.html
```

### 5. Acessar o Dashboard

Abra `index.html` no navegador ou acesse: `https://OffModzKkkkj.github.io/H-XZ-V2/`

## Integração com IA

### Google Gemini

```python
from ai_analyzer import GeminiAnalyzer

analyzer = GeminiAnalyzer(api_key="sua_chave")
analysis = analyzer.analyze_vulnerability({
    "type": "open_port",
    "port": 22,
    "service": "SSH"
})
print(analysis.recommendations)
```

### Groq

```python
from ai_analyzer import GroqAnalyzer

analyzer = GroqAnalyzer(api_key="sua_chave")
analysis = analyzer.analyze_vulnerability({
    "type": "weak_cipher",
    "details": "SSL 3.0 detectado"
})
print(analysis.recommendations)
```

## Recursos de Segurança

* **Validação de Entrada**: Todos os inputs são validados e sanitizados.
* **Sem Armazenamento de Dados**: Os resultados podem ser processados localmente ou no GitHub Pages sem exposição.
* **Conformidade**: Respeita as leis de pentest responsável (apenas em ambientes autorizados).

## Contribuição

Contribuições são bem-vindas! Abra uma issue ou pull request para sugestões e melhorias.

## Licença

MIT License

## Aviso Legal

Esta ferramenta é destinada apenas para fins educacionais e de teste de segurança autorizado. O uso não autorizado para acessar sistemas é ilegal. O autor não se responsabiliza pelo uso indevido.
