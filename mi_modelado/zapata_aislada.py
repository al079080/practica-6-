""" Diseño básico de zapata aislada (considerando carga axial y momentos) Archivo: zapata_aislada.py Descripción:

Calcula dimensiones de una zapata aislada para una carga axial P y momentos Mx, My

Usa una estrategia iterativa sencilla para garantizar que la presión máxima en la zapata no exceda la tensión admisible del suelo (q_allow)

Incluye una interfaz gráfica Tkinter para introducir datos y guardar un README.md


IMPORTANTE: Este script está pensado como herramienta pedagógica para la práctica. Revisa siempre las normas y códigos locales antes de usar en proyectos reales. """

import math import tkinter as tk from tkinter import ttk, messagebox, filedialog

def design_zapata(P, Mx, My, q_allow, max_iter=2000, scale_step=1.01): """ Diseño simplificado de zapata aislada. Entradas: P: carga axial vertical (kN) Mx, My: momentos alrededor de x e y (kN*m) q_allow: tensión admisible del suelo (kN/m2)

Método:
  - Se parte suponiendo zapata cuadrada Bx=By = sqrt(P/q_allow)
  - Se calcula ex = Mx/P, ey = My/P (m). Si P=0 se devuelve error.
  - Se usa una expresión aproximada para la presión máxima en una esquina bajo
    carga excéntrica:
      p_max = (P/(Bx*By)) * (1 + 6*|ex|/Bx + 6*|ey|/By)
    (esta expresión se utiliza como criterio de comprobación iterativa)
  - Si p_max > q_allow, se aumenta progresivamente Bx y By (escalado uniforme)
    hasta que se cumpla p_max <= q_allow o se alcance el número máximo de iter.

Salida: diccionario con resultados y banderas de verificación.
"""
if P <= 0:
    raise ValueError("La carga axial P debe ser mayor que 0 kN")

ex = Mx / P  # m
ey = My / P  # m

# dimensión inicial (m) - asumimos unidades: P en kN, q_allow en kN/m2 -> B en m
B = math.sqrt(P / q_allow)
Bx = B
By = B

iter_count = 0
p_max = None
while iter_count < max_iter:
    A = Bx * By
    p_uniform = P / A  # kN/m2
    p_max = p_uniform * (1 + 6 * abs(ex) / Bx + 6 * abs(ey) / By)

    # comprobación
    if p_max <= q_allow + 1e-6:
        break

    # aumentar dimensiones proporcionalmente
    Bx *= scale_step
    By *= scale_step
    iter_count += 1

# comprobación de excentricidad relativa al 'núcleo' aproximado (B/6)
kern_check_x = abs(ex) <= Bx / 6
kern_check_y = abs(ey) <= By / 6

results = {
    'P_kN': P,
    'Mx_kNm': Mx,
    'My_kNm': My,
    'ex_m': ex,
    'ey_m': ey,
    'Bx_m': Bx,
    'By_m': By,
    'Area_m2': Bx * By,
    'p_max_kN_m2': p_max,
    'q_allow_kN_m2': q_allow,
    'iterations': iter_count,
    'kern_check_x': kern_check_x,
    'kern_check_y': kern_check_y,
    'status': 'OK' if p_max <= q_allow + 1e-6 else 'NOT_OK'
}
return results

def format_results(res): lines = [] lines.append(f"Carga axial P = {res['P_kN']:.2f} kN") lines.append(f"Momento Mx = {res['Mx_kNm']:.2f} kN·m, My = {res['My_kNm']:.2f} kN·m") lines.append(f"Excentricidades: ex = {res['ex_m']:.4f} m, ey = {res['ey_m']:.4f} m") lines.append(f"Dimensiones zapata: Bx = {res['Bx_m']:.3f} m, By = {res['By_m']:.3f} m") lines.append(f"Área = {res['Area_m2']:.3f} m^2") lines.append(f"Presión máxima estimada p_max = {res['p_max_kN_m2']:.2f} kN/m^2") lines.append(f"Tensión admisible q_allow = {res['q_allow_kN_m2']:.2f} kN/m^2") lines.append(f"Comprobación núcleo: ex dentro de B/6? {res['kern_check_x']}, ey dentro de B/6? {res['kern_check_y']}") lines.append(f"Estado: {res['status']} (iteraciones = {res['iterations']})") return '\n'.join(lines)

---------- Interfaz gráfica (Tkinter) ----------

class App(tk.Tk): def init(self): super().init() self.title('Diseño de Zapata Aislada - Práctica') self.geometry('680x520') self.resizable(False, False)

frame = ttk.Frame(self, padding=10)
    frame.pack(fill='both', expand=True)

    # Entradas
    labels = ['Carga axial P (kN)', 'Momento Mx (kN·m)', 'Momento My (kN·m)', 'Tensión admisible suel. q_allow (kN/m2)']
    defaults = ['300', '20', '10', '150']
    self.vars = []
    for i, lab in enumerate(labels):
        ttk.Label(frame, text=lab).grid(row=i, column=0, sticky='w', pady=6)
        var = tk.StringVar(value=defaults[i])
        ent = ttk.Entry(frame, textvariable=var, width=20)
        ent.grid(row=i, column=1, sticky='w')
        self.vars.append(var)

    # Botones
    btn_calc = ttk.Button(frame, text='Calcular diseño', command=self.on_calculate)
    btn_calc.grid(row=5, column=0, pady=12)

    btn_save = ttk.Button(frame, text='Guardar README.md', command=self.on_save_readme)
    btn_save.grid(row=5, column=1, pady=12)

    # Resultado
    self.txt = tk.Text(frame, width=80, height=20)
    self.txt.grid(row=6, column=0, columnspan=3, pady=6)

    # Estado
    self.status = ttk.Label(frame, text='Introduce datos y presiona Calcular', foreground='blue')
    self.status.grid(row=7, column=0, columnspan=2, sticky='w')

def on_calculate(self):
    try:
        P = float(self.vars[0].get())
        Mx = float(self.vars[1].get())
        My = float(self.vars[2].get())
        q_allow = float(self.vars[3].get())
    except ValueError:
        messagebox.showerror('Error', 'Verifica que los valores introducidos sean numéricos')
        return

    try:
        res = design_zapata(P, Mx, My, q_allow)
    except Exception as e:
        messagebox.showerror('Error', str(e))
        return

    self.txt.delete('1.0', tk.END)
    self.txt.insert(tk.END, format_results(res))
    self.current_result = res
    self.status.config(text='Cálculo realizado ✔')

def on_save_readme(self):
    try:
        res = getattr(self, 'current_result', None)
        if res is None:
            messagebox.showwarning('Atención', 'Primero realiza un cálculo y luego guarda el README')
            return

        content = generate_readme_text(res)
        path = filedialog.asksaveasfilename(defaultextension='.md', filetypes=[('Markdown', '*.md')], title='Guardar README como')
        if not path:
            return
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        messagebox.showinfo('Guardado', f'README.md guardado en:\n{path}')
    except Exception as e:
        messagebox.showerror('Error', str(e))

def generate_readme_text(res): md = [] md.append('# Diseño básico de zapata aislada') md.append('') md.append('Descripción') md.append('') md.append('Este proyecto realiza un diseño simplificado de una zapata aislada considerando carga axial y momentos en dos direcciones. Se verifica que la presión máxima estimada no exceda la tensión admisible del suelo.') md.append('') md.append('Supuestos y método') md.append('') md.append('- Material homogéneo y presión de contacto linealizada bajo la zapata.') md.append('- Se parte de una zapata cuadrada y, si es necesario, se escalan las dimensiones hasta cumplir la condición de presión máxima.') md.append('- Excentricidades: ex = Mx/P, ey = My/P.') md.append('- Criterio aproximado usado para p_max (esquina):') md.append('') md.append('math') md.append('p_{max} = (P / A) \left(1 + 6 \frac{|e_x|}{B_x} + 6 \frac{|e_y|}{B_y} \right)') md.append('') md.append('') md.append('Entradas usadas (ejemplo)') md.append('') md.append(f"- P = {res['P_kN']:.2f} kN") md.append(f"- Mx = {res['Mx_kNm']:.2f} kN·m") md.append(f"- My = {res['My_kNm']:.2f} kN·m") md.append(f"- q_allow = {res['q_allow_kN_m2']:.2f} kN/m^2") md.append('') md.append('Resultados') md.append('') md.append(f"- Bx = {res['Bx_m']:.3f} m") md.append(f"- By = {res['By_m']:.3f} m") md.append(f"- Área = {res['Area_m2']:.3f} m^2") md.append(f"- Presión máxima estimada p_max = {res['p_max_kN_m2']:.2f} kN/m^2") md.append(f"- Núcleo: ex en B/6? {res['kern_check_x']}, ey en B/6? {res['kern_check_y']}") md.append('') md.append('Cómo usar') md.append('') md.append('1. Ejecuta python zapata_aislada.py (requiere Python 3 y Tkinter).') md.append('2. Introduce P, Mx, My y q_allow. Presiona Calcular diseño.') md.append('3. Revisa los resultados y guarda el README si lo deseas.') md.append('') md.append('Advertencias') md.append('') md.append('- Esta herramienta es aproximada y destinada a fines académicos. Verifica con normas locales para un diseño definitivo.') md.append('- El método de presión máxima utilizado es simplificado; para casos complejos usar análisis más riguroso o software geotécnico.') md.append('') md.append('---') md.append('Generado por: Script de ayuda para la práctica de Modelado (Ingeniería Civil)')

return '\n'.join(md)

if name == 'main': app = App() app.mainloop()
