import tkinter as tk
from tkinter import ttk
from clima import Mes, calcular_clima
from encontros import nomes_zonas, teste

def iniciar_interface():
    def simular_clima():
        mes_nome = combo_meses.get()
        nivel = entry_nivel.get()

        try:
            mes = next(m for m in Mes if m.value == mes_nome)
            nivel = int(nivel)
            resultado = calcular_clima(mes, nivel)

            texto_resultado.config(state='normal')
            texto_resultado.delete("1.0", tk.END)
            texto_resultado.insert(tk.END, f"🌦️ Clima para {mes_nome} (Nível {nivel}):\n{resultado}")
            texto_resultado.config(state='disabled')
        except Exception as e:
            texto_resultado.config(state='normal')
            texto_resultado.delete("1.0", tk.END)
            texto_resultado.insert(tk.END, f"⚠️ Erro: {e}")
            texto_resultado.config(state='disabled')

    def simular_encontro():
        zona_nome = combo_zonas.get()

        try:
            resultado_encontro = teste(zona_nome)
            texto_resultado.config(state='normal')
            texto_resultado.delete("1.0", tk.END)
            texto_resultado.insert(tk.END, f"🎲 Encontro na zona {zona_nome}:\n{resultado_encontro}")
            texto_resultado.config(state='disabled')
        except Exception as e:
            texto_resultado.config(state='normal')
            texto_resultado.delete("1.0", tk.END)
            texto_resultado.insert(tk.END, f"⚠️ Erro: {e}")
            texto_resultado.config(state='disabled')

    root = tk.Tk()
    root.title("Escudo Kingmaker 🛡️")
    root.geometry("600x500")

    ttk.Label(root, text="Escolha a zona:").pack(pady=5)
    combo_zonas = ttk.Combobox(root, values=nomes_zonas)
    combo_zonas.pack()

    ttk.Label(root, text="Escolha o mês:").pack(pady=5)
    combo_meses = ttk.Combobox(root, values=[mes.value for mes in Mes])
    combo_meses.pack()

    ttk.Label(root, text="Nível do grupo:").pack(pady=5)
    entry_nivel = ttk.Entry(root)
    entry_nivel.pack()

    ttk.Button(root, text="Simular Clima", command=simular_clima).pack(pady=10)
    ttk.Button(root, text="Simular Encontro", command=simular_encontro).pack(pady=10)

    texto_resultado = tk.Text(root, height=20, wrap='word', state='disabled')
    texto_resultado.pack(padx=10, pady=10, fill='both', expand=True)

    root.mainloop()
