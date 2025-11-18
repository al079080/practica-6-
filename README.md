# practica-6-al079080 
Práctica 6 – Modelado de Problemas  
Diseño básico de una zapata aislada con Python

Alumno:  Aldo Canul 
Matrícula: 79080
Materia: Programación  
Profesor: Juan A Chuc Mendez 
Repositorio: practica-6-al079080



1. Descripción general del problema

En esta práctica se desarrolla un programa en Python que resuelve un problema real de ingeniería civil:  
el diseño básico de una zapata aislada bajo carga vertical y momentos.

El objetivo es modelar el problema mediante programación, mostrando cómo se aplican matemáticas, interfaz gráfica y lógica para obtener las dimensiones mínimas de una cimentación.



 2. Marco teórico

Una **zapata aislada** es un tipo de cimentación superficial que recibe la carga de una columna y la transmite al suelo.

 Conceptos usados:

 ✔ Carga vertical (P)  
Es la fuerza que actúa hacia abajo sobre la zapata.

### ✔ Momentos Mx y My  
Son fuerzas que generan inclinación o torsión y hacen que la carga no esté centrada.

### ✔ Excentricidades  
Cuando existe un momento, la carga deja de estar al centro.  
Se calcula así:

- ex = Mx / P  
- ey = My / P  

Estas excentricidades generan presiones mayores en un lado de la zapata.

 ✔ Presión del terreno  
Para que la zapata sea segura, la presión máxima real no debe superar la presión admisible del terreno.

 ✔ Cálculo de presión máxima

La presión máxima se calcula así:


pₘₐₓ = (P / (Bx · By)) · (1 + 6·|ex| / Bx + 6·|ey| / By)

donde:  
- P = carga  
- Bx = dimensión en el eje X  
- By = dimensión en el eje Y  
- ex = excentricidad en X  
- ey = excentricidad en Y  
- p_max = presión máxima transmitida al suelo  

El objetivo es encontrar valores de Bx y By que mantengan la presión máxima dentro del límite seguro.



 3. Funcionamiento del programa

El programa utiliza una **interfaz gráfica (Tkinter)** donde el usuario ingresa:

- Carga vertical P  
- Momento Mx  
- Momento My  
- Presión admisible del terreno  

 ¿Qué hace el programa?

1. Calcula las excentricidades (ex y ey).  
2. Propone dimensiones iniciales de la zapata.  
3. Calcula la presión máxima real.  
4. Si la presión es mayor a la admisible, aumenta automáticamente Bx y By.  
5. Detiene el proceso cuando la zapata cumple con la presión admisible.  
6. Muestra los valores finales calculados en pantalla.

Resultados que muestra:
- Dimensión Bx  
- Dimensión By  
- Área de la zapata  
- ex y ey  
- Presión máxima  
- Estado del diseño (Aceptable o No aceptable)



 4. Cómo ejecutar el programa

Requisitos:  
- Python 3  
- Tkinter (incluido por defecto en Python)

 Comando para ejecutar:

Al ejecutarlo, se abrirá la ventana del programa para ingresar los datos.



 5. Archivos del repositorio
 mi_modelado -> zapata_aislada.py



 6. Conclusión

Este proyecto demuestra cómo Python puede usarse para resolver problemas reales de ingeniería civil mediante programación, guiando al usuario de forma automática hasta obtener un diseño preliminar de una cimentación segura.


7. Nota final

El diseño generado es solo una aproximación académica.  
Para proyectos reales de construcción, se deben aplicar normas y análisis estructurales adicionales.
