.. _Dice Stats:

Dice Stats
==========

Introduction
------------

If you're a new to this library you may want to look at the :ref:`Tutorial`.

If you've gone through that then the :ref:`Terminology` section
would help understand the inner mechanics of the Dice class, but
otherwise this document explains the public interface.

Public library
--------------

.. automodule:: dice_stats
   :members:
   :private-members:
   :inherited-members:


.. _Terminology:

Terminology
-----------

.. _ds-t-Chances:

Chances
+++++++

These are made up of pairs of two items, a :ref:`ds-t-Chances Value`
and a :ref:`ds-t-Chances Chance`. These are contained in a mapping
where the mapping's key is the :ref:`ds-t-Chances Value`, and the value
is the :ref:`ds-t-Chances Chance`.

This swap of terminology may cause some confusion so I think it should
be noted again that the mappings value is not the :ref:`ds-t-Chances Value`.

.. _ds-t-Chances Value:

Chances Value
+++++++++++++

This is the value on the dice. For a standard d6 this would mean that
the dice has 6 values ranging from 1 to 6. And so the the
:ref:`ds-t-Chances` would have six :ref:`ds-t-Chances Value`.

.. _ds-t-Chances Chance:

Chances Chance
++++++++++++++

This is the chance of the value being an outcome. For a standard d6 this
would mean that all the chances are 1/6. And so the the
:ref:`ds-t-Chances` would have six :ref:`ds-t-Chances Chance` all with
the same value.

These are all provided as :class:`fractions.Fraction` so that there are
no floating point issues when calculating the chances. This also allows
high precision in the chances we calculate.

.. note::

   The :ref:`ds-t-Internal Chances Chance` is slightly different to
   the public one.

.. _ds-t-Total Chance:

Total Chance
++++++++++++

This is the total chance of the dice, this is important as the
:ref:`ds-t-Chances` and the :ref:`ds-t-Internal Chances` total to
different amounts, as described in the latter.
Whilst this may at first seem bizarre, some games allow dice to have an
over, or under, 100% chance. Say we have a game where you roll a d10;

 - on a 1 you miss,
 - on a 10 you hit twice, otherwise
 - you hit once.

This could be inferred as hitting 100% of the time, and missing 10%.
Making the total chance of the dice 110%.
Whilst interpreting the rules this way are entirely down to you.
It leaves the option open for you to go down this route if you want to.

This attribute is also used on some of the more high level functions.
This is as they split a dice into say two results,
ones that are successful and ones that are unsuccessful.
Having this attribute contained within the dice makes it simpler
to handle the splitting and then combining of those dice.

.. _ds-t-Internal Chances:

Internal Chances
++++++++++++++++

These are the internal chances of the dice object. These are stored in a
:class:`dict` where the :ref:`ds-t-Internal Chances Chance` total 1.
This has two major benefits:

  - Allows us to at runtime check if there's a critical error with the
    dice object and exit gracefully, rather than fail silently.

    Whilst I'm confident the code works due to tests. I also know that
    this feature helped development and debugging when I messed up
    different functions. It's an extra fail safe to know the code isn't
    completely broken.

    It may also help you if you start doing some fancy things with this
    library, as if you break the state of the :ref:`ds-t-Internal Chances`
    then you know straight away, not after hours of debugging.

  - Keeping a mutable dictionary private, and keeping the amount of
    code that touch it to a minimum helps keep the logic of the
    Dice object reasonable. Passing a dice object to a function
    shouldn't mutate the object. At every step of development I've
    kept immutability to be a core concept for the dice class.

    Given that creating dice statistics are complex enough, this can
    keep me, and hopefully you, to be at peace when making complex dice
    statistic functions. And should prevent easy to overlook issues with
    a mutable class.

.. _ds-t-Internal Chances Chance:

Internal Chances Chance
+++++++++++++++++++++++

This is slightly different to the :ref:`ds-t-Chances Chance`.
This, the internal one, totals to 1, allowing some runtime validity checks.
However the public :ref:`ds-t-Chances Chance` total to whatever
:ref:`ds-t-Total Chance` is.

For the most part, these are likely to be the same.
