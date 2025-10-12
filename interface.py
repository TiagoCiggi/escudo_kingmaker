import tkinter as tk
from tkinter import ttk
from clima import Mes, calcular_clima

def iniciar_interface():
    def simular():
        mes_nome = combo_meses.get()
        nivel = entry_nivel.get()

        try:
            mes = next(m for m in Mes if m.value == mes_nome)
            nivel = int(nivel)
            resultado = calcular_clima(mes, nivel)
            texto_resultado.config(state='normal')
            texto_resultado.delete("1.0", tk.END)
            texto_resultado.insert(tk.END, resultado)
            texto_resultado.config(state='disabled')
        except Exception as e:
            texto_resultado.config(state='normal')
            texto_resultado.delete("1.0", tk.END)
            texto_resultado.insert(tk.END, f"⚠️ Erro: {e}")
            texto_resultado.config(state='disabled')

    root = tk.Tk()
    root.title("🌦️ Simulador Climático")
    root.geometry("600x500")

    ttk.Label(root, text="Escolha o mês:").pack(pady=5)
    combo_meses = ttk.Combobox(root, values=[mes.value for mes in Mes])
    combo_meses.pack()

    ttk.Label(root, text="Nível do grupo:").pack(pady=5)
    entry_nivel = ttk.Entry(root)
    entry_nivel.pack()

    ttk.Button(root, text="Simular Clima", command=simular).pack(pady=10)

    texto_resultado = tk.Text(root, height=20, wrap='word', state='disabled')
    texto_resultado.pack(padx=10, pady=10, fill='both', expand=True)

    root.mainloop()
