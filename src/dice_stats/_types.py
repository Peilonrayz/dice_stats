"""Generic types used across the project."""

import fractions
import numbers
from typing import DefaultDict, Dict, Mapping, Union

TFloatNumber = numbers.Real
FloatNumber = numbers.Real
TIntNumber = numbers.Integral
IntNumber = numbers.Integral
TNumber = Union[TFloatNumber, TIntNumber]
Number = (FloatNumber, IntNumber)  # pylint: disable=invalid-name

TBaseNumber = Union[int, float]
BaseNumber = (int, float)  # pylint: disable=invalid-name

# Public
TTotalChance = fractions.Fraction
TotalChance = fractions.Fraction
TChancesChance = fractions.Fraction
ChancesChance = fractions.Fraction
TChancesValue = TNumber
ChancesValue = Number  # pylint: disable=invalid-name
TChances = Dict[TChancesValue, TChancesChance]
TChancesDD = DefaultDict[TChancesValue, TChancesChance]
TChancesMap = Mapping[TChancesValue, TChancesChance]
