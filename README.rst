Dice Stats
==========

.. image:: https://travis-ci.com/Peilonrayz/dice_stats.svg?branch=master
   :target: https://travis-ci.com/Peilonrayz/dice_stats
   :alt: Build Status

About
-----

Get statistics for rolling dice.

Installation
------------

.. code:: shell

   $ python -m pip install dice_stats

Documentation
-------------

Documentation is available `via GitHub <https://peilonrayz.github.io/dice_stats/>`_.

Testing
-------

To run all tests run ``nox``. No venv is needed; nox makes all of them for us.

.. code:: shell

   $ python -m pip install --user nox
   $ git clone https://peilonrayz.github.io/dice_stats/
   $ cd dice_stats
   dice_stats $ nox

License
-------

Dice Stats is available under the MIT license.


Change Log
----------

1.1.0
+++++

-  Change ``Dice.apply_function`` and ``apply_dice`` to allow changes to the total chance.
-  Add matmul, ``@``, as an operator to change total chance.
-  Don't change the total chance of dice multiplied together.
-  Make numpy and matplotlib optional dependencies

1.0.0
+++++

-  Released publicly