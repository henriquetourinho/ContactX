# ContactX 📇🐧

**ContactX** é uma agenda de contatos com interface gráfica moderna, feita em **Python** com **Tkinter**, totalmente voltada para **usuários de Linux** que valorizam **privacidade, praticidade e personalização**.

Este é um **protótipo livre e aberto**: qualquer pessoa pode baixar, usar, modificar e contribuir!

---

## 🧠 O que o ContactX faz

- 🖼️ Interface gráfica com tema escuro e design elegante
- 📇 Cadastro completo: nome, telefone, e-mails, redes sociais e chave PGP
- 🖼️ Upload de foto de perfil por contato
- 💾 Armazenamento local via banco de dados SQLite
- ⚡ Atalhos de teclado (Ctrl+S para salvar, Ctrl+N para novo contato)
- 🔐 Não depende da nuvem — todos os dados são seus
- 🐧 Feito sob medida para desktops Linux

---

## ⚙️ Requisitos

Para rodar o ContactX, você precisa de:

- Python 3.8 ou superior
- Bibliotecas Python:
  - `tkinter` (normalmente já vem com Python)
  - `Pillow` (para fotos de perfil)
- Sistema Linux com ambiente gráfico

---

## 🧪 Instalação

### No Debian, Ubuntu e derivados:

```bash
sudo apt update
sudo apt install python3 python3-tk python3-pil python3-pil.imagetk
```

Ou com `pip`:

```bash
pip install Pillow
```

---

## ▶️ Como executar

1. Clone o repositório:

```bash
git clone https://github.com/henriquetourinho/contactx.git
cd contactx
```

2. Execute a aplicação:

```bash
python3 agenda.py
```

3. Um arquivo `agenda.db` será criado automaticamente na primeira execução, contendo seus contatos.

---

## 🔒 Sobre privacidade

ContactX é **100% offline**: seus dados ficam somente no seu computador, salvos localmente via SQLite. Nenhuma informação é enviada para a internet.

---

## 📝 Licença

Este projeto está licenciado sob a **GNU GPL v3**.  
Você é livre para **usar, modificar, redistribuir**, desde que mantenha a mesma licença.

---

## 🙋‍♂️ Desenvolvido por

**Carlos Henrique Tourinho Santana**  
📍 Salvador - Bahia  
🔗 GitHub: [github.com/henriquetourinho](https://github.com/henriquetourinho)  
🔗 Wiki: [wiki.debian.org/henriquetourinho](https://wiki.debian.org/henriquetourinho)

---

📢 **Protótipo inicial — colaborações são bem-vindas!**
