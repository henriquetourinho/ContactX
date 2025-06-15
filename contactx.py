# /*********************************************************************************
# * Projeto:   ContactX
# * Autor:     Carlos Henrique Tourinho Santana
# * Versão:    1.0
# * Data:      14 de junho de 2025
# GitHub: https://github.com/henriquetourinho
# *
# * Descrição:
# * ContactX é uma aplicação de desktop completa para gerenciamento de contatos,
# * desenvolvida em Python com uma interface gráfica (GUI) moderna e intuitiva
# * construída com a biblioteca Tkinter. O projeto foi projetado para ser uma
# * solução de agenda pessoal robusta, segura e totalmente offline, armazenando
# * todas as informações localmente em um banco de dados SQLite. O design foca
# * em um fluxo de trabalho otimizado e uma experiência de usuário agradável,
# * com um tema visual sério e minimalista.
# *
# * Funcionalidades Principais:
# * - Interface Gráfica Completa: Gerencie todos os seus contatos através de
# * uma interface visual, sem a necessidade de usar o terminal.
# * - Armazenamento Local: Todos os dados são salvos em um arquivo de banco de
# * dados SQLite (`agenda.db`) na mesma pasta do programa, garantindo
# * privacidade e controle total sobre suas informações.
# * - Campos Detalhados: Salve informações abrangentes, incluindo múltiplos
# * emails, redes sociais (GitHub, Discord, etc.), chave PGP e foto de perfil.
# * - Gerenciamento de Fotos: Faça o upload de uma foto de perfil para cada
# * contato para fácil identificação visual.
# * - Fluxo de Trabalho Inteligente: Um único botão "Salvar" que sabe quando
# * criar um novo contato ou atualizar um existente.
# * - Menu Superior e Atalhos: Navegação facilitada com um menu clássico
# * ("Arquivo", "Ajuda") e atalhos de teclado como Ctrl+S (Salvar) e
# * Ctrl+N (Novo Contato).
# *
# * Notas de Uso e Dependências:
# * - Este programa requer a biblioteca `Pillow` para a funcionalidade de
# * upload de fotos. Instale-a em sistemas Debian/Ubuntu com o comando:
# * `sudo apt install python3-pil python3-pil.imagetk`
# * - Seus contatos são salvos no arquivo `agenda.db`. Faça backup deste
# * arquivo para não perder suas informações. Apagá-lo fará com que o
# * programa crie um novo banco de dados vazio.
# *********************************************************************************/

import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import sqlite3
import webbrowser
import os
from PIL import Image, ImageTk, ImageDraw

class ContactXApp:
    # --- Paleta de Cores e Configs ---
    COR_FUNDO = "#1c1c1c"
    COR_FUNDO_BLOCO = "#2a2a2a"
    COR_OURO = "#d4af37"
    COR_TEXTO = "#f0f0f0"
    COR_FUNDO_ENTRY = "#333333"
    COR_BORDA = "#555555"
    COR_HEADER = "#2a2a2a"
    TAMANHO_FOTO = (150, 150)

    def __init__(self, root):
        self.root = root
        self.root.title("ContactX")
        self.root.geometry("1100x750")
        self.root.configure(bg=self.COR_FUNDO)
        self.root.resizable(False, False)

        self.caminho_foto_atual = None
        self.selected_item_id = None
        
        self.gerar_placeholder()

        self.configurar_estilos()
        self.criar_menu() # <<< NOVO: Cria o menu superior
        self.conectar_db()
        self.criar_widgets()
        
        self.limpar_campos()
        self.popular_lista()
        
        # <<< NOVO: Configura os atalhos de teclado
        self.root.bind("<Control-s>", lambda event: self.salvar_contato())
        self.root.bind("<Control-n>", lambda event: self.limpar_campos())


    def gerar_placeholder(self):
        if not os.path.exists("placeholder.png"):
            img = Image.new('RGB', self.TAMANHO_FOTO, color=self.COR_FUNDO_BLOCO)
            d = ImageDraw.Draw(img)
            d.text((45, 65), "Sem Foto", fill=self.COR_BORDA)
            img.save("placeholder.png")

    def conectar_db(self):
        self.conn = sqlite3.connect('agenda.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, telefone TEXT,
                emails TEXT, telegram TEXT, github TEXT, discord TEXT, reddit TEXT,
                pgp_key TEXT, foto_path TEXT
            )
        """)
        self.conn.commit()

    def configurar_estilos(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        # ... (estilos idênticos à versão anterior)
        self.style.configure('.', background=self.COR_FUNDO, foreground=self.COR_TEXTO, bordercolor=self.COR_BORDA)
        self.style.configure('TFrame', background=self.COR_FUNDO)
        self.style.configure('TLabel', background=self.COR_FUNDO, foreground=self.COR_TEXTO, font=('Segoe UI', 10))
        self.style.configure('TLabelframe', background=self.COR_FUNDO_BLOCO, bordercolor=self.COR_BORDA)
        self.style.configure('TLabelframe.Label', background=self.COR_FUNDO_BLOCO, foreground=self.COR_OURO, font=('Segoe UI', 11, 'bold'))
        self.style.configure('TEntry', fieldbackground=self.COR_FUNDO_ENTRY, foreground=self.COR_TEXTO, insertcolor=self.COR_TEXTO)
        self.style.configure('Gold.TButton', background=self.COR_OURO, foreground='#000000', font=('Segoe UI', 10, 'bold'), borderwidth=0)
        self.style.map('Gold.TButton', background=[('active', '#b89a30')], relief=[('pressed', 'sunken')])
        self.style.configure('Sec.TButton', background=self.COR_BORDA, foreground=self.COR_TEXTO, font=('Segoe UI', 9), borderwidth=0)
        self.style.map('Sec.TButton', background=[('active', '#666666')])
        self.style.configure('Treeview', background=self.COR_FUNDO_ENTRY, fieldbackground=self.COR_FUNDO_ENTRY, foreground=self.COR_TEXTO, rowheight=25)
        self.style.configure('Treeview.Heading', background=self.COR_HEADER, foreground=self.COR_OURO, font=('Segoe UI', 11, 'bold'))
        self.style.map('Treeview', background=[('selected', self.COR_OURO)], foreground=[('selected', '#000000')])
        self.style.configure('Vertical.TScrollbar', background=self.COR_FUNDO, troughcolor=self.COR_FUNDO_ENTRY, bordercolor=self.COR_FUNDO, arrowcolor=self.COR_TEXTO)
        self.style.configure('TNotebook', background=self.COR_FUNDO, bordercolor=self.COR_FUNDO)
        self.style.configure('TNotebook.Tab', background=self.COR_FUNDO_BLOCO, foreground=self.COR_TEXTO, padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', self.COR_OURO), ('active', self.COR_BORDA)], foreground=[('selected', '#000000')])

    # --- NOVO MÉTODO PARA CRIAR O MENU ---
    def criar_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Novo Contato", command=self.limpar_campos, accelerator="Ctrl+N")
        file_menu.add_command(label="Salvar Contato", command=self.salvar_contato, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)

        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre...", command=self.mostrar_sobre)

    def mostrar_sobre(self):
        messagebox.showinfo(
            "Sobre o ContactX",
            "ContactX - Agenda de Contatos Segura\n\n"
            "Desenvolvido por:\n"
            "Carlos Henrique Tourinho Santana\n\n"
            "https://github.com/henriquetourinho",
            parent=self.root
        )

    def criar_widgets(self):
        # ... (O resto do método criar_widgets permanece igual)
        frame_lista = ttk.Frame(self.root); frame_lista.pack(side=tk.LEFT, fill=tk.Y, padx=(20, 10), pady=20)
        frame_formulario = ttk.Frame(self.root); frame_formulario.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=20)
        ttk.Button(frame_lista, text="Novo Contato (+)", style='Gold.TButton', command=self.limpar_campos).pack(fill=tk.X, ipady=4, pady=(0,15))
        frame_tree = ttk.Frame(frame_lista); frame_tree.pack(fill=tk.BOTH, expand=True)
        self.tree = ttk.Treeview(frame_tree, columns=('id', 'nome'), show='headings'); self.tree.heading('id', text='ID'); self.tree.heading('nome', text='Nome')
        self.tree.column('id', width=40, stretch=tk.NO, anchor=tk.CENTER); self.tree.column('nome', width=220)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview); self.tree.configure(yscroll=scrollbar.set); scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind('<<TreeviewSelect>>', self.item_selecionado)
        self.label_status = ttk.Label(frame_formulario, text="", font=('Segoe UI', 14, 'bold'), foreground=self.COR_OURO); self.label_status.pack(pady=(0,10), anchor=tk.W)
        frame_superior = ttk.Frame(frame_formulario); frame_superior.pack(fill=tk.X)
        bloco_foto = ttk.Labelframe(frame_superior, text="Foto de Perfil"); bloco_foto.pack(side=tk.LEFT, padx=(0, 20), anchor=tk.N)
        self.label_foto = ttk.Label(bloco_foto, background=self.COR_FUNDO_BLOCO); self.label_foto.pack(padx=10, pady=10)
        ttk.Button(bloco_foto, text="Selecionar Foto", style='Sec.TButton', command=self.selecionar_foto).pack(pady=(0,10), padx=10)
        bloco_nome = ttk.Frame(frame_superior); bloco_nome.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(bloco_nome, text="Nome Completo*").pack(anchor=tk.W, padx=5)
        self.entry_nome = ttk.Entry(bloco_nome, width=50, font=('Segoe UI', 12)); self.entry_nome.pack(fill=tk.X, padx=5, pady=5, ipady=2)
        ttk.Label(bloco_nome, text="Telefone Principal").pack(anchor=tk.W, padx=5)
        self.entry_telefone = ttk.Entry(bloco_nome, width=50, font=('Segoe UI', 12)); self.entry_telefone.pack(fill=tk.X, padx=5, pady=5, ipady=2)
        notebook = ttk.Notebook(frame_formulario); notebook.pack(pady=20, fill=tk.BOTH, expand=True)
        f1, f2, f3 = ttk.Frame(notebook), ttk.Frame(notebook), ttk.Frame(notebook)
        notebook.add(f1, text='  Contatos e Redes  '); notebook.add(f2, text='  Chave PGP  '); notebook.add(f3, text='  Créditos  ')
        ttk.Label(f1, text="Emails (um por linha)").pack(anchor=tk.W, padx=5, pady=(10,0))
        self.text_emails = tk.Text(f1, height=4, width=60, bg=self.COR_FUNDO_ENTRY, fg=self.COR_TEXTO, relief=tk.FLAT, insertbackground=self.COR_TEXTO, font=('Segoe UI', 10)); self.text_emails.pack(fill=tk.X, expand=True, padx=5, pady=5)
        redes_frame = ttk.Frame(f1); redes_frame.pack(fill=tk.X, expand=True, pady=10)
        campos_redes = ["Telegram", "GitHub", "Discord", "Reddit"]; self.entries_redes = {}
        for i, campo in enumerate(campos_redes):
            ttk.Label(redes_frame, text=campo).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = ttk.Entry(redes_frame, width=40); entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
            self.entries_redes[campo.lower()] = entry
        ttk.Label(f2, text="Chave PGP Pública").pack(anchor=tk.W, padx=5, pady=(10,0))
        self.text_pgp = tk.Text(f2, height=12, width=60, bg=self.COR_FUNDO_ENTRY, fg=self.COR_TEXTO, relief=tk.FLAT, insertbackground=self.COR_TEXTO, font=('Segoe UI', 10)); self.text_pgp.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        frame_creditos_interno = ttk.Frame(f3); frame_creditos_interno.pack(expand=True)
        ttk.Label(frame_creditos_interno, text="Desenvolvido por:", foreground=self.COR_BORDA, font=('Segoe UI', 12)).pack(pady=(0, 5))
        ttk.Label(frame_creditos_interno, text="Carlos Henrique Tourinho Santana", foreground=self.COR_TEXTO, font=('Segoe UI', 18, 'bold')).pack(pady=(0, 20))
        ttk.Separator(frame_creditos_interno, orient='horizontal').pack(fill='x', padx=50)
        links_frame = ttk.Frame(frame_creditos_interno); links_frame.pack(pady=20)
        link_font = font.Font(family='Segoe UI', size=11, underline=True)
        links = [("Email:", "henriquetourinho@riseup.net", "mailto:henriquetourinho@riseup.net"), ("GitHub:", "github.com/henriquetourinho", "https://github.com/henriquetourinho"), ("Página Pessoal:", "henriquetourinho.com", "https://henriquetourinho.com/"), ("Debian Wiki:", "wiki.debian.org/henriquetourinho", "https://wiki.debian.org/henriquetourinho")]
        for i, (label_text, display_text, url) in enumerate(links):
            ttk.Label(links_frame, text=label_text, font=('Segoe UI', 11, 'bold'), foreground=self.COR_OURO).grid(row=i, column=0, sticky='e', padx=10, pady=5)
            link_label = ttk.Label(links_frame, text=display_text, foreground="#6c99bb", font=link_font, cursor="hand2"); link_label.grid(row=i, column=1, sticky='w', padx=10, pady=5)
            link_label.bind("<Button-1>", lambda e, link=url: webbrowser.open_new(link))
        ttk.Separator(frame_creditos_interno, orient='horizontal').pack(fill='x', padx=50)
        ttk.Label(frame_creditos_interno, text=f"Salvador, Bahia - {self.get_current_year()}", foreground=self.COR_BORDA, font=('Segoe UI', 10)).pack(pady=20)
        frame_acoes = ttk.Frame(frame_formulario); frame_acoes.pack(fill=tk.X, pady=10)
        ttk.Button(frame_acoes, text="Salvar", style='Gold.TButton', command=self.salvar_contato).pack(side=tk.RIGHT, padx=5, ipady=8, ipadx=20)
        ttk.Button(frame_acoes, text="Deletar", style='Sec.TButton', command=self.deletar_contato).pack(side=tk.RIGHT, padx=5, ipady=5, ipadx=10)

    def get_current_year(self):
        from datetime import datetime
        return datetime.now().year

    # --- O restante da LÓGICA FUNCIONAL permanece o mesmo ---
    def salvar_contato(self):
        if self.selected_item_id is None: self._adicionar_contato()
        else: self._atualizar_contato()
    def carregar_foto(self, caminho_foto):
        try: imagem = Image.open(caminho_foto)
        except: imagem = Image.open("placeholder.png")
        imagem.thumbnail(self.TAMANHO_FOTO, Image.Resampling.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(imagem)
        self.label_foto.config(image=self.photo_image)
    def selecionar_foto(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png *.gif"), ("Todos", "*.*")])
        if caminho: self.caminho_foto_atual = caminho; self.carregar_foto(caminho)
    def coletar_dados_formulario(self):
        return {'nome': self.entry_nome.get(),'telefone': self.entry_telefone.get(),'emails': self.text_emails.get("1.0", tk.END).strip(),'telegram': self.entries_redes['telegram'].get(),'github': self.entries_redes['github'].get(),'discord': self.entries_redes['discord'].get(),'reddit': self.entries_redes['reddit'].get(),'pgp_key': self.text_pgp.get("1.0", tk.END).strip(),'foto_path': self.caminho_foto_atual}
    def _adicionar_contato(self):
        dados = self.coletar_dados_formulario()
        if not dados['nome']: messagebox.showerror("Erro", "O campo 'Nome' é obrigatório.", parent=self.root); return
        campos, placeholders = ', '.join(dados.keys()), ', '.join(['?'] * len(dados))
        self.cursor.execute(f"INSERT INTO contatos ({campos}) VALUES ({placeholders})", list(dados.values()))
        self.conn.commit()
        messagebox.showinfo("Sucesso", f"Contato '{dados['nome']}' adicionado!", parent=self.root)
        self.limpar_campos(); self.popular_lista()
    def _atualizar_contato(self):
        dados = self.coletar_dados_formulario()
        if not dados['nome']: messagebox.showerror("Erro", "O campo 'Nome' não pode ficar vazio.", parent=self.root); return
        set_clause = ', '.join([f"{key} = ?" for key in dados.keys()])
        valores = list(dados.values()) + [self.selected_item_id]
        self.cursor.execute(f"UPDATE contatos SET {set_clause} WHERE id = ?", valores)
        self.conn.commit()
        messagebox.showinfo("Sucesso", f"Contato '{dados['nome']}' atualizado!", parent=self.root)
        self.popular_lista()
    def deletar_contato(self):
        if not self.selected_item_id: messagebox.showwarning("Aviso", "Selecione um contato da lista para deletar.", parent=self.root); return
        nome = self.entry_nome.get()
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar permanentemente o contato '{nome}'?", parent=self.root):
            self.cursor.execute("DELETE FROM contatos WHERE id=?", (self.selected_item_id,))
            self.conn.commit()
            self.limpar_campos(); self.popular_lista()
    def limpar_campos(self):
        self.selected_item_id = None
        self.label_status.config(text="Criando Novo Contato")
        self.entry_nome.delete(0, tk.END); self.entry_telefone.delete(0, tk.END)
        self.text_emails.delete("1.0", tk.END); self.text_pgp.delete("1.0", tk.END)
        for entry in self.entries_redes.values(): entry.delete(0, tk.END)
        self.caminho_foto_atual = None; self.carregar_foto("placeholder.png")
        if self.tree.selection(): self.tree.selection_remove(self.tree.selection())
        self.entry_nome.focus()
    def item_selecionado(self, event=None):
        selected_items = self.tree.selection()
        if not selected_items: return
        item_id = self.tree.item(selected_items[0])['values'][0]
        self.cursor.execute("SELECT * FROM contatos WHERE id=?", (item_id,))
        dados = self.cursor.fetchone()
        if not dados: return
        self.limpar_campos(); self.selected_item_id = dados['id']
        self.label_status.config(text=f"Editando: {dados['nome']}")
        self.entry_nome.insert(0, dados['nome']); self.entry_telefone.insert(0, dados['telefone'] or '')
        self.text_emails.insert("1.0", dados['emails'] or ''); self.text_pgp.insert("1.0", dados['pgp_key'] or '')
        self.entries_redes['telegram'].insert(0, dados['telegram'] or ''); self.entries_redes['github'].insert(0, dados['github'] or '')
        self.entries_redes['discord'].insert(0, dados['discord'] or ''); self.entries_redes['reddit'].insert(0, dados['reddit'] or '')
        self.caminho_foto_atual = dados['foto_path']; self.carregar_foto(self.caminho_foto_atual or "placeholder.png")
    def popular_lista(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in self.cursor.execute("SELECT id, nome FROM contatos ORDER BY nome"):
            self.tree.insert('', tk.END, values=(row['id'], row['nome']))

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactXApp(root)
    root.mainloop()