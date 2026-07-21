<p align="right"><a href="README.md">English</a></p>

# EzTranslator

Um tradutor leve que roda em segundo plano no Windows. Aperte um atalho global de qualquer lugar, e um pequeno popup traduz o que estiver na sua área de transferência — sem abrir janela, sem trocar de aba do navegador.

## Funcionalidades

- Fica na bandeja do sistema, inicia na hora, não atrapalha
- Atalho global (padrão **Shift+Alt+T**, personalizável) abre um popup perto do cursor
- Lê a área de transferência automaticamente e já traduz na hora
- Detecta o idioma de origem sozinho, ou você escolhe manualmente no menu
- Botão de troca rápida pra inverter origem/destino
- Traduz sozinho enquanto você digita (depois de uma pausa curta) ou ao apertar Enter — sem cliques extras
- Botão de copiar pra pegar o resultado
- Fecha com `Esc` ou clicando fora do popup
- Tela de Configurações: idiomas padrão, captura de atalho (clica no campo, aperta a combinação nova), iniciar com o Windows
- Totalmente efêmero — nada sobre suas traduções é logado, salvo ou guardado em histórico

A tradução usa o Google Translate (via [deep-translator](https://github.com/nidhaloff/deep-translator)), gratuito, sem precisar de chave de API.

## Instalação

Baixe o `EzTranslator.exe` na [última release](https://github.com/LuizBrunca/EzTranslator/releases/latest) e execute. Sem instalador, sem configuração — é um executável único.

> **Nota:** como o executável não é assinado digitalmente, o Windows Defender SmartScreen pode avisar na primeira execução ("O Windows protegeu seu PC"). Clique em **Mais informações** → **Executar assim mesmo**.

Pra iniciar o EzTranslator automaticamente no login, ative **Start with Windows** nas Configurações (menu da bandeja).

## Atualizando

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
