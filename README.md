# Pràctica LP – mini Forth  
**GEI – Llenguatges de Programació (FIB-UPC)**  
**Q1 2025–2026**

Autor: *Víctor Moreno Villanueva*  
Nota: *10*
---

## Descripció del projecte

Aquest projecte implementa un intèrpret complet de **mini Forth**, un subconjunt del llenguatge Forth basat en pila, utilitzant:

- **ANTLR4** per generar el lexer i parser a partir de `forth.g4`
- **Python 3** per implementar el visitador i la màquina d’execució
- **doctest** per validar el comportament amb un joc de proves

L’intèrpret avalua un programa Forth passat com a `string` i l’executa sobre una pila d’enters, seguint les especificacions oficials de la pràctica.

---

## Fitxers inclosos

```
├── Makefile
├── README.md
├── forth.g4
├── forth.py
├── machine.py
├── visitor_user.py
└── test.txt
```

**Important:**  
Els fitxers generats per ANTLR (**forthLexer.py**, **forthParser.py**, **forthVisitor.py**, **forthListener.py**, *.tokens, *.interp) **NO** s’inclouen en el ZIP, tal com demana el lliurament.

---

## Dependències

- Python **3.x**
- Runtime d’ANTLR per Python:  
  `pip install antlr4-python3-runtime`
- Comanda `antlr4` instal·lada al sistema
- Llibreries estàndard de Python (cap llibreria externa no permesa)

---

## Ús del projecte

### **1) Generar els fitxers d’ANTLR**
```bash
make
```

### **2) Executar l’intèrpret**
```bash
python3 -i forth.py
>>> interpret("1 2 3 .s")
[1, 2, 3]
>>> interpret("2 3 + .")
5
```

### **3) Executar els tests**
```bash
make test
```
o
```bash
python3 -m doctest -v test.txt
```

El projecte passa **45/45 tests**.

---

## Arquitectura del codi

### **`machine.py`**
Implementa la màquina d’execució basada en pila:

- `push`, `pop`, `peek`
- `.`, `.s`
- Gestió d’errors:
  - `Error: pila buida!`
  - `Error: divisió per zero!`

### **`visitor_user.py`**
Conté el visitador principal, encarregat d’executar l’AST:

Funcionalitats implementades:
- Operacions aritmètiques (`+ - * / mod`)
- Manipulació de la pila:
  - `swap`, `2swap`
  - `dup`, `2dup`
  - `over`, `2over`
  - `rot`
  - `drop`, `2drop`
- Relacionals: `< <= > >= = <>`
- Booleans: `and or not`
- Definició de funcions: `: nom ... ;`
- Condicionals: `if ... else ... endif`
- Recursivitat amb `recurse`

### **`forth.g4`**
Gramàtica ANTLR que reconeix totes les construccions del mini Forth descrites a l’enunciat.

### **`forth.py`**
Punt d’entrada de l’intèrpret.  
Gestiona:

- Parsing
- Creació de la màquina i el visitador
- Execució
- Tota la sortida via `print` (compatible amb doctest)

---

## Jocs de proves

`test.txt` conté proves que cobreixen:

- Aritmètica
- Operacions de pila
- Relacionals i booleans
- Definició de funcions
- Condicionals
- Recursivitat (`factorial`)
- Errors:
  - pila buida
  - divisió per zero

Es poden executar amb:

```bash
python3 -m doctest -v test.txt
```
---

## Gestió d’errors

### **Pila buida**
Quan una operació requereix desapilar i la pila està buida:
```
Error: pila buida!
```

### **Divisió per zero**
```
Error: divisió per zero!
```
I es col·loca `0` a la pila per continuar.

Segons l’enunciat, la resta d’errors semàntics tenen comportament indefinit.

---

## Estat de la pràctica

-  Gramàtica completa  
-  Visitador complet  
-  Gestió d’errors implementada  
-  Recursivitat i condicionals  
-  Jocs de proves 100%  
-  Compliment de PEP8 (indentació i estil general)  
-  Makefile funcional

---


