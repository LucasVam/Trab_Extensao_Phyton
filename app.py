import os
import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from database import init_db, adicionar_orcamento, remover_orcamento, consultar_orcamentos, obter_proximo_id

LOGO_PATH = "logo.png"

def gerar_pdf(id, descricao, valor, data, nome_cliente, telefone):
    c = canvas.Canvas(f"Orcamento_{id}.pdf", pagesize=A4)
    width, height = A4
    font_size = 18
    logo_width, logo_height = 100, 50
    logo_x = 30
    logo_y = height - 80
    via_height = height / 2

    def desenhar_via(y_offset):
        if LOGO_PATH:
            c.drawImage(LOGO_PATH, logo_x, y_offset + logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True)
        c.setFont("Helvetica", font_size)
        margem_esquerda = logo_x
        margem_direita = width - 30
        c.drawString(margem_esquerda, y_offset + logo_y - 20, f"OS Nº: {id}")
        c.drawString(margem_esquerda, y_offset + logo_y - 60, f"Nome: {nome_cliente}")
        c.drawString(margem_esquerda, y_offset + logo_y - 100, f"Telefone: {telefone}")
        c.drawString(margem_esquerda, y_offset + logo_y - 140, f"Descrição: {descricao}")
        c.drawString(margem_esquerda, y_offset + logo_y - 180, f"Valor: R$ {valor:.2f}")
        c.drawString(margem_direita - c.stringWidth(f"Data de Criação: {data.strftime('%d/%m/%Y %H:%M:%S')}") - 10, y_offset + logo_y - 20, 
                     f"Data de Criação: {data.strftime('%d/%m/%Y %H:%M:%S')}")
        c.drawString(margem_direita - c.stringWidth("Data: ______________________________") - 10, y_offset + logo_y - 320, 
                     "Data: ______________________________")
        c.drawString(margem_direita - c.stringWidth("Assinatura: _________________________") - 10, y_offset + logo_y - 280, 
                     "Assinatura: _________________________")

    desenhar_via(0)
    desenhar_via(-via_height)
    
    c.save()

def salvar_orcamento():
    descricao = entry_desc.get()
    valor = entry_valor.get()
    nome_cliente = entry_nome_cliente.get()
    telefone = entry_telefone.get()
    
    if not descricao or not valor or not nome_cliente or not telefone:
        messagebox.showerror("Erro", "Preencha todos os campos")
        return
    
    valor = valor.replace(',', '.')
    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido")
        return
    
    orcamento_id = obter_proximo_id()
    data_atual = datetime.now()
    adicionar_orcamento(descricao, valor, data_atual, nome_cliente, telefone)
    gerar_pdf(orcamento_id, descricao, valor, data_atual, nome_cliente, telefone)
    consultar_orcamentos_gui()
    messagebox.showinfo("Sucesso", f"Orçamento Nº {orcamento_id} gerado com sucesso")

def remover_orcamento_gui():
    orcamento_id = entry_remover.get()
    
    if not orcamento_id:
        messagebox.showerror("Erro", "Informe o ID do orçamento")
        return
    
    remover_orcamento(orcamento_id)
    try:
        os.remove(f"Orcamento_{orcamento_id}.pdf")
    except FileNotFoundError:
        pass
    
    consultar_orcamentos_gui()
    messagebox.showinfo("Sucesso", f"Orçamento Nº {orcamento_id} removido com sucesso")

def consultar_orcamentos_gui():
    orcamentos = consultar_orcamentos()
    orcamentos = sorted(orcamentos, key=lambda x: x[0], reverse=True)[:10]
    
    for widget in frame_checkboxes.winfo_children():
        widget.destroy()
    
    global check_vars
    check_vars = {}
    for i, orcamento in enumerate(orcamentos):
        var = tk.BooleanVar()
        check_vars[orcamento[0]] = var
        tk.Checkbutton(frame_checkboxes, text=f"OS Nº: {orcamento[0]} - Nome: {orcamento[4]} - Descrição: {orcamento[1]} - Valor: R$ {orcamento[2]:.2f}", variable=var).pack(anchor=tk.W, padx=10, pady=2)
    
def exportar_pdf_gui():
    if not check_vars:
        messagebox.showerror("Erro", "Nenhum orçamento disponível para exportar")
        return
    
    exportado = False
    orcamentos = consultar_orcamentos()
    
    for orc_id, var in check_vars.items():
        if var.get():
            orcamento = next((orc for orc in orcamentos if orc[0] == orc_id), None)
            if orcamento:
                try:
                    if isinstance(orcamento[3], datetime):
                        data_criacao = orcamento[3]
                    else:
                        data_criacao = datetime.strptime(orcamento[3], '%d/%m/%Y %H:%M:%S')
                except ValueError:
                    messagebox.showerror("Erro", f"Formato de data inválido para OS Nº {orcamento[0]}: {orcamento[3]}")
                    continue
                
                gerar_pdf(orcamento[0], orcamento[1], orcamento[2], data_criacao, orcamento[4], orcamento[5])
                exportado = True
    
    if exportado:
        messagebox.showinfo("Sucesso", "Orçamentos exportados com sucesso")
    else:
        messagebox.showerror("Erro", "Nenhum orçamento selecionado para exportar")

def on_focus_in(event):
    widget = event.widget
    if widget.get() == widget.placeholder:
        widget.delete(0, tk.END)
        widget.config(fg='black')

def on_focus_out(event):
    widget = event.widget
    if widget.get() == '':
        widget.insert(0, widget.placeholder)
        widget.config(fg='grey')

def create_entry(frame, placeholder):
    entry = tk.Entry(frame, width=50, **entry_style)
    entry.placeholder = placeholder
    entry.insert(0, placeholder)
    entry.config(fg='grey')
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    return entry

root = tk.Tk()
root.title("Gerador de Orçamentos")
root.geometry("800x750")
root.resizable(True, True)
root.configure(bg="#f0f0f0")

 
root.configure(bg="#f0f0f0")

frame_main = tk.Frame(root, padx=20, pady=20, bg="#ffffff", relief=tk.RIDGE, bd=2)
frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

label_style = {"bg": "#ffffff", "anchor": "w", "font": ("Helvetica", 12, "bold")}
entry_style = {"font": ("Helvetica", 12)}

tk.Label(frame_main, text="Nome do Cliente:", **label_style).grid(row=0, column=0, sticky=tk.W, pady=5)
entry_nome_cliente = create_entry(frame_main, "Digite o nome do cliente")
entry_nome_cliente.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_main, text="Telefone:", **label_style).grid(row=1, column=0, sticky=tk.W, pady=5)
entry_telefone = create_entry(frame_main, "Digite o telefone")
entry_telefone.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_main, text="Descrição:", **label_style).grid(row=2, column=0, sticky=tk.W, pady=5)
entry_desc = create_entry(frame_main, "Digite a descrição")
entry_desc.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_main, text="Valor:", **label_style).grid(row=3, column=0, sticky=tk.W, pady=5)
entry_valor = create_entry(frame_main, "Digite o valor (ex: 50,55)")
entry_valor.grid(row=3, column=1, padx=10, pady=5)

button_style = {"font": ("Helvetica", 12, "bold")}

tk.Button(frame_main, text="Salvar Orçamento", command=salvar_orcamento, bg="blue", fg="white", width= 15, height=2 ,**button_style).grid(row=4, column=1, pady=10, sticky=tk.E)

tk.Label(frame_main, **label_style).grid(row=5, column=0, sticky=tk.W, pady=5)
entry_remover = create_entry(frame_main, "Digite o numero da OS para remover")
entry_remover.grid(row=15, column=1, padx=10, pady=5)

tk.Button(frame_main, text="Remover Orçamento", command=remover_orcamento_gui, bg="blue", fg="white", width= 20, height=2 , **button_style).grid(row=16, column=1, pady=10, sticky=tk.E)

tk.Button(frame_main, text="Consultar Orçamentos", command=consultar_orcamentos_gui, bg="blue", fg="white", width= 20, height=2 , **button_style).grid(row=6, column=0, pady=10, sticky=tk.E)

tk.Label(frame_main, text="Marque os orçamentos que deseja exportar:", **label_style).grid(row=8, column=0, columnspan=2, pady=5)

frame_checkboxes = tk.Frame(frame_main, bg="#ffffff")
frame_checkboxes.grid(row=9, column=0, columnspan=2, pady=10)

tk.Button(frame_main, text="Exportar PDF", command=exportar_pdf_gui, bg="blue", fg="white", width= 20, height=2 , **button_style).grid(row=10, column=1, pady=10, sticky=tk.E)

init_db()
root.mainloop()
