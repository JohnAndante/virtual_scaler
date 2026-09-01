# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto segue [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added
- Item de menu "Reiniciar comunicação" na bandeja, para reiniciar a leitura da porta serial sem fechar o programa.
- Arquivo `VERSION` como fonte única da versão exibida em "Sobre".
- Log em arquivo (`virtual_scaler.log`, ao lado do executável) substituindo os `print()` que se perdiam numa build `--noconsole`.
- Lint automático (`ruff`) e checagem de build no CI a cada Pull Request.

### Fixed
- `TrayIcon` recebia o módulo `scale` em vez da instância criada, deixando o ícone sem acesso real à balança.
- Botões da tela "Sobre" executavam a ação na hora de montar a janela em vez de no clique.
- `messagebox.showerror(...).run_detached()` quebrava com `AttributeError` ao tentar reportar um erro real.
- Validação de configuração aceitava valores inválidos (ex.: `"123abc"` como peso) por falta de âncora nas regexes.
- `config.ini` era resolvido em relação ao diretório de execução (`cwd`) em vez de junto ao executável.

## [0.2.0-beta] - 2024-04-09
### Added
- Reescrita completa do fluxo de configuração, usando `config.ini` em vez de parâmetros de linha de comando.
- Ícone na bandeja do sistema, com acesso a Configurações, Sobre e Fechar aplicação.
- Interface gráfica (Tkinter) para editar as configurações sem precisar mexer no arquivo `.ini` na mão.

## [0.1.0-beta] - 2024-03-27
### Added
- Primeira versão pública: balança virtual configurável via parâmetros de linha de comando (`-p`, `-b`, `-t`, `-f`).
- Envio contínuo de peso fixo ou aleatório para uma porta COM.
