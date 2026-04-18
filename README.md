# ✈️ Air Combat - Jogo 2D em Python

## 📌 Descrição
Air Combat é um jogo 2D desenvolvido em Python utilizando Pygame, onde o jogador controla um avião e enfrenta inimigos em diferentes cenários com níveis progressivos de dificuldade.

O jogo conta com sistema de fases, seleção de avião, tiros, colisões, pontuação e ranking com banco de dados SQLite.

---

## 🎮 Funcionalidades

### 🧭 Menu Principal
- Player 1
- 2 Players (Cooperativo - planejado)
- 2 Players (Competitivo - planejado)
- Score (ranking)
- Exit

---

### ✈️ Seleção de Avião
Antes de iniciar o jogo, o jogador pode escolher entre 3 tipos de avião:

| Avião        | Velocidade | Tiro        | Característica    |
|-------------|-----------|------------|----------------------|
| Raptor delta     | Alta      | Lento       | Mobilidade alta  |
| Falcon One  | Média     | Médio       | Equilibrado           |
|

---

### 🌍 Sistema de Fases

O jogo possui 3 fases com dificuldade progressiva:

#### 🏙️ Fase 1 - Deserto
- Inimigos mais lentos
- Menor quantidade de tiros

#### 🏜️ Fase 2 - Deserto
- Inimigos mais rápidos
- Maior frequência de ataques

#### 🌊 Fase 3 - Mar
- Inimigos 
- Alta dificuldade

---

### 🔫 Sistema de Combate
- Tiros do jogador
- Tiros dos inimigos
- Colisão entre objetos
- Sistema de vida

---

### 💥 Sistema de Pontuação
- Pontos ao destruir inimigos
- Inimigos que escapam não contam pontos

---

### 🏆 Ranking (SQLite)
- Armazena os 5 melhores scores
- Persistência de dados
- Exibição em tela de Score
---
🧱 Estrutura do Projeto

```Jogo_Teste/
├── asset/              # Imagens (.png) e Áudios (.mp3)
├── code/               # Código-fonte do projeto
│   ├── __init__.py     # Inicializador do pacote Python
│   ├── Bullet.py       # Lógica dos projéteis
│   ├── Button.py       # Automatiza produção de botões
│   ├── Collision.py    # Detecta as colisões
│   ├── Const.py        # Constantes (Velocidade, Pontos, etc.)
│   ├── database.db     # Banco de dados (gerado automaticamente)
│   ├── Enemy.py        # Define comportamento e adversários
│   ├── Entity.py       # Classe base para objetos do jogo
│   ├── EntityFactory.py# Fábrica de entidades
│   ├── EntityMediator.py# Torre de controle do jogo
│   ├── Game.py         # Orquestra tudo o que acontece
│   ├── Game_State.py   # Enumerador de estados
│   ├── Level.py        # Gestão de fases e progresso
│   ├── Level_Config.py # Manual de instruções (Fases)
│   ├── Menu.py         # Recepção do jogo
│   ├── Plane_config.py # Catálogo das naves
│   ├── Player.py       # Lógica e estados do jogador
│   └── Score_Screen.py # Interface do Ranking
└── Main.py             # Ponto de entrada do jogo