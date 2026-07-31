<p align="right"><a href="README.md">English</a></p>

# EzTranslator

Tradução instantânea, num popup dinâmico, em qualquer lugar do seu PC. Aperte um atalho global de qualquer lugar e um pequeno popup abre perto do cursor — do atalho ao resultado, as mãos não saem do teclado.

<!-- TODO: adicionar um GIF/screenshot do popup em ação aqui -->

## Funcionalidades

- Fica na bandeja do sistema, inicia na hora, não atrapalha
- Atalho global (padrão **Shift+Alt+T**, personalizável) abre um popup perto do cursor
- Detecta o idioma de origem sozinho, ou você escolhe manualmente no menu
- Traduz sozinho enquanto você digita (depois de uma pausa curta) ou ao apertar Enter — sem cliques extras
- `Ctrl+S` troca origem/destino na hora com o popup já aberto (ou use o botão de troca)
- Também lê a área de transferência automaticamente, se preferir nem digitar
- Botão de copiar pra pegar o resultado
- Fecha com `Esc` ou clicando fora do popup
- Tela de Configurações: idiomas padrão, captura de atalho (clica no campo, aperta a combinação nova), iniciar com o Windows
- Totalmente efêmero — nada sobre suas traduções é logado, salvo ou guardado em histórico
- Disponível atualmente só para Windows

A tradução usa o Google Translate (via [deep-translator](https://github.com/nidhaloff/deep-translator)), gratuito, sem precisar de chave de API.

## Instalação

Pegue a última release na [página de releases](https://github.com/LuizBrunca/EzTranslator/releases/latest) — duas opções:

- **`EzTranslator-Setup-x.x.x.exe`** (recomendado): um instalador de verdade — atalho no menu Iniciar, ícone opcional na área de trabalho, desinstalação limpa.
- **`EzTranslator.exe`**: um executável único e portável, sem passo de instalação, é só executar.

> **Nota:** como nenhum dos dois é assinado digitalmente, o Windows Defender SmartScreen pode avisar na primeira execução ("O Windows protegeu seu PC"). Clique em **Mais informações** → **Executar assim mesmo**.

Pra iniciar o EzTranslator automaticamente no login, ative **Start with Windows** nas Configurações (menu da bandeja).

## Atualizando

**Se você usou o instalador:** é só rodar o novo `EzTranslator-Setup-x.x.x.exe` — ele fecha o app em execução e sobrescreve a instalação no mesmo lugar.

**Se você está na versão portátil:**

1. Feche o EzTranslator primeiro (clique direito no ícone da bandeja → **Quit**) — o Windows não deixa sobrescrever um `.exe` em execução.
2. Baixe o novo `EzTranslator.exe` na [última release](https://github.com/LuizBrunca/EzTranslator/releases/latest).
3. Substitua o arquivo antigo pelo novo, **no mesmo caminho e com o mesmo nome**.
4. Execute. Configurações, idiomas salvos e seu atalho personalizado continuam intactos — ficam em `%LOCALAPPDATA%\EzTranslator\`, separado do executável.

Se o **Start with Windows** estiver ativado, ele aponta pro caminho exato do `.exe` — sobrescrevendo no mesmo lugar, continua funcionando sem precisar fazer mais nada. Se você salvar o novo download em outro lugar (pasta ou nome diferente), desative e reative o **Start with Windows** nas Configurações pra ele apontar pro novo local.

## Desenvolvimento

Precisa do [uv](https://docs.astral.sh/uv/) e Python 3.12+.

```powershell
git clone https://github.com/LuizBrunca/EzTranslator.git
cd EzTranslator
uv sync
uv run translator-app
```

### Estrutura do projeto

```text
src/translator_app/
├── main.py              # Ponto de entrada — conecta bandeja, popup, hotkey, settings
├── tray.py               # Ícone e menu da bandeja do sistema
├── hotkey_listener.py     # Registro do atalho global (pynput)
├── single_instance.py    # Impede rodar mais de uma cópia ao mesmo tempo
├── startup.py             # Toggle de "iniciar com o Windows" no Registro
├── config.py              # Caminhos + carregar/salvar config.json
├── logger.py               # Logger com rotação de arquivo
├── ui/
│   ├── popup.py            # O popup de tradução
│   └── settings.py         # Tela de configurações
├── translator/
│   ├── engine.py            # Wrapper do GoogleTranslator
│   ├── worker.py             # Roda a tradução numa QThread separada
│   └── languages.py          # Lista curada de idiomas
└── assets/
    └── app.ico
```

### Gerando o executável

```powershell
uv run pyinstaller translator-app.spec --noconfirm
```

Gera `dist/EzTranslator.exe` (arquivo único, sem console).

## Licença

MIT — veja [LICENSE](LICENSE).
