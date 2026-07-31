# LinkedIn post — EzTranslator

## Antes de postar

- **Grave um GIF curto (10-15s)** mostrando: pressionar o hotkey (Shift+Alt+T) sobre um texto qualquer → popup abrindo → tradução aparecendo. Isso importa mais que qualquer texto — posts com imagem/vídeo de produto têm muito mais alcance no LinkedIn.
- Alternativa rápida: 2-3 screenshots (tray icon → popup aberto → popup com tradução).
- Poste terça a quinta, entre 8h-10h ou 12h-13h (horários de maior engajamento no LinkedIn).
- Marque a keywords certas: Python, PySide6, open source, produtividade — ajuda o alcance orgânico.

## Versão PT-BR (foco em prática + efêmera)

> Tradução rápida, prática, e que não deixa rastro nenhum.
>
> Criei o **EzTranslator**: aperta um atalho (Shift+Alt+T) em qualquer lugar do Windows e um popup discreto abre perto do cursor, pronto pra traduzir. Sem abrir navegador, sem trocar de janela, sem cadastro — e nada do que você traduz fica salvo ou logado em lugar nenhum, nunca.
>
> Alguns detalhes que fizeram diferença pra mim:
> - Detecta o idioma de origem automaticamente
> - Traduz enquanto você digita (com um pequeno delay), sem precisar clicar em nada
> - Também pega o texto direto do que você copiou, se preferir nem digitar
> - Botão de copiar e de inverter idiomas
> - Efêmero por design: fecha e some, sem histórico, sem log, sem rastro
> - Gratuito, sem chave de API, um único .exe pra instalar
>
> É open source, feito em Python (PySide6 + PyInstaller). Link do repositório e do download nos comentários. Feedback é muito bem-vindo!
>
> #Python #OpenSource #Produtividade #DevTools #Windows

## English version (dev/open-source angle)

> Fast, practical translation that leaves no trace.
>
> Built **EzTranslator**: hit a global hotkey (Shift+Alt+T) anywhere on Windows and a small popup opens near your cursor, ready to translate. No browser tab, no window to switch to, no sign-up — and nothing you translate is ever logged or stored, anywhere.
>
> A few things I cared about while building it:
> - Auto-detects the source language
> - Translates as you type (debounced), no extra clicks
> - Also picks up whatever you've already copied, if you'd rather not type at all
> - Copy button + quick language swap
> - Ephemeral by design: closes and it's gone — no history, no logs, no trace
> - Free, no API key, single-file .exe

> Open source, built with Python (PySide6, PyInstaller), translation via Google Translate (deep-translator). Repo + download link in the comments — feedback and contributions welcome.
>
> #Python #OpenSource #DeveloperTools #Productivity #Windows

## CTA nos comentários (evita que o LinkedIn penalize o alcance de posts com link)

> Repositório e download: https://github.com/LuizBrunca/EzTranslator

## Seção "Projetos" do perfil

Um bom Project no LinkedIn segue: problema → o que foi feito → decisões técnicas → resultado. É isso que recrutadores e conexões técnicas procuram, não uma lista de features.

**Nome do projeto:** EzTranslator — Fast, Ephemeral Translation for Windows

**Descrição:**

> Cansado de abrir uma aba nova toda vez que precisava traduzir uma frase curta (email, chat, texto comentado), projetei e implementei sozinho o EzTranslator: um app que vive na bandeja do Windows e entrega tradução instantânea via atalho global, sem deixar rastro do que foi traduzido.
>
> Dois princípios guiaram o design: **prática** — atalho global, popup perto do cursor, sem abrir navegador, sem clique extra, aceitando tanto texto digitado quanto o que já está no clipboard — e **efêmera** — nenhuma tradução é logada, salva em histórico ou persistida em disco. O app existe pra resolver o momento e some.
>
> Principais decisões técnicas:
> - PySide6 para uma UI nativa e responsiva
> - QThread para rodar a tradução em background sem travar a interface
> - pynput para captura de hotkey global
> - Leitura opcional do clipboard como um dos jeitos de entrada, ao lado da digitação direta
> - PyInstaller + Inno Setup para empacotar como .exe único com instalador
> - Arquitetura 100% efêmera por design — nada é logado ou persistido além das configurações do usuário
>
> Resultado: utilitário gratuito, sem API key, sem telemetria, open source.

**Skills/tags:** Python · PySide6 · Desktop Application Development · Software Architecture · Open Source · PyInstaller

**Mídia:** o mesmo GIF/screenshot do popup em ação sugerido para o post — reaproveita.

**URL:** https://github.com/LuizBrunca/EzTranslator

**Período:** data de início do projeto até hoje (ou "em andamento" se ainda mantém ativamente).
