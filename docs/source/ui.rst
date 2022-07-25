User Interface
================



Generating UI
--------------

Generating the UI is handled by the *generate_ui* module.

The UI is sorted into several tabs. Each tab groups multiple SPN's together, usually by similar type. (DIG I/P, PWM O/P, VOLTAGE...)

Each Tab contains a number of labels, buttons, dropdown menus, and text boxes.

This module contains functions that handle the creation of widgets, and their placement within the UI.

.. autoclass:: UserInterface.generate_ui.generate_ui
    :members:


Updating UI
-------------

Once the UI is generated and the components initialized, a thread handles any updates and changes made to the widgets listed.

.. autoclass:: UserInterface.update_ui.update_ui
    :members:



UI Callbacks
------------

These functions are meant to be callbacks that are ran when the corresponding widget is activated.

.. autoclass:: UserInterface.ui_callbacks.ui_callbacks
    :members:
