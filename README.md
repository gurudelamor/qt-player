# Reproductor Sinergia Doraemon
### Hecho con PySide 6 librería grafica de Python 3.

#### ↓ Colaboradores 

<h3>
<a target="_blank" href="https://github.com/a-tomy-c" title="Tomy">@a-tomy-c</a>
</h3>
<h3>
<a target="_blank" href="https://github.com/crostow" title="Mau">@crostow</a>
</h3>

------------------------------------------------------------------------------------
![Reproductor Sinergia/Doraemon](views/diagrama.png "Reproductor Sinergia/Doraemon")
<!-- ![Texto alternativo](/ruta/a/la/imagen.jpg "Título alternativo") -->
------------------------------------------------------------------------------------
![Reproductor Sinergia/Doraemon](views/inirepro.png "Reproductor Sinergia/Doraemon")
------------------------------------------------------------------------------------
![Reproductor Sinergia/Doraemon](views/inirepromax.png "Reproductor Sinergia/Doraemon")
------------------------------------------------------------------------------------
[!["Reproductor Sinergia/Doraemon"](https://img.youtube.com/vi/P1juQCHdCqg/maxresdefault.jpg "Reproductor Sinergia/Doraemon")](https://youtu.be/P1juQCHdCqg)

<!-- <a href="https://youtu.be/P1juQCHdCqg" target="_blank">
<img src="https://img.youtube.com/vi/P1juQCHdCqg/0.jpg" alt="Watch the video" width="1200" border="10" />
</a> -->


## NOTAS
### window frameless
- la ventana principal ya tiene metodos basicos
- en el archivo `tests_so` esta la prueba con el **window frameless**
- agregue hotkey "Ctrl + Q" para salir
- [ ] otros hotkeys ... 


### widget Playlist
- la interfaz y metodos de la playlist estan ahora en un paquete
- agregue los metodos que faltaban de (seleccion primero y ultimo) el de agregar lo hare luego (necesitare el dialog)
- en el archivo `tests_so` esta la prueba con el **playlist**
- [ ] agregar archivos


### widget Player
- he creado el widget player (solo tiene funciones basicas)


### Interfaz
- corte la playlist y lo coloque en un widget independiente
- cambie un label por un textedit (lbMeta)
- lo dividi en partes la interfaz


## ESTRUCTURA
la estructura actual y los archivos que ya estoy usando (ire agregando y reusando otras)
- todo lo que cambie esta en la carpeta "sin_orden" de manera temporal mientras se define la estructura.

---

por el momento la estructura esta asi, solo es temporal (puede cambiarse despues)

```
.
├── widget_body
│   └── ui_widget_body.ui
├── widget_control
│   └── ui_widget_control.ui
├── widget_player
│   └── __init__.py
├── widget_playlist
│   ├── __init__.py
│   ├── ui_widget_playlist.py
│   └── ui_widget_playlist.ui
└── window_frameless
    ├── __init__.py
    ├── ui_main_window.py
    └── ui_main_window.ui

6 directories, 9 files
```



