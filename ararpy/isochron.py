# ===============================================================================
# Copyright 2015 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= enthought library imports =======================

# ============= standard library imports ========================
from numpy import array
# ============= local library imports  ==========================
from uncertainties import ufloat
from ararpy.arar import age_equation


def extract_isochron_xy(analyses):
    ans = [(ai.get_interference_corrected_value('Ar39'),
            ai.get_interference_corrected_value('Ar36'),
            ai.get_interference_corrected_value('Ar40'))
           for ai in analyses]
    a39, a36, a40 = array(ans).T
    # print 'a40',a40
    # print 'a39',a39
    # print 'a36',a36
    try:
        xx = a39 / a40
        yy = a36 / a40
    except ZeroDivisionError:
        return

    return xx, yy

def calculate_isochron(analyses, reg='NewYork'):
    ref = analyses[0]
    ans = [(ai.get_interference_corrected_value('Ar39'),
            ai.get_interference_corrected_value('Ar36'),
            ai.get_interference_corrected_value('Ar40'))
           for ai in analyses]

    a39, a36, a40 = array(ans).T
    try:
        xx = a39 / a40
        yy = a36 / a40
    except ZeroDivisionError:
        return

    xs, xerrs = zip(*[(xi.nominal_value, xi.std_dev) for xi in xx])
    ys, yerrs = zip(*[(yi.nominal_value, yi.std_dev) for yi in yy])

    xds, xdes = zip(*[(xi.nominal_value, xi.std_dev) for xi in a40])
    yns, ynes = zip(*[(xi.nominal_value, xi.std_dev) for xi in a36])
    xns, xnes = zip(*[(xi.nominal_value, xi.std_dev) for xi in a39])

    regx = isochron_regressor(ys, yerrs, xs, xerrs,
                              xds, xdes, yns, ynes, xns, xnes)

    reg = isochron_regressor(xs, xerrs, ys, yerrs,
                             xds, xdes, xns, xnes, yns, ynes,
                             reg)

    xint = ufloat(regx.get_intercept(), regx.get_intercept_error())
    # xint = ufloat(reg.x_intercept, reg.x_intercept_error)
    try:
        r = xint ** -1
    except ZeroDivisionError:
        r = 0

    age = ufloat(0, 0)
    if r > 0:
        age = age_equation((ref.j.nominal_value, 0), r, arar_constants=ref.arar_constants)
    return age, reg, (xs, ys, xerrs, yerrs)


def isochron_regressor(xs, xes, ys, yes,
                       xds, xdes, xns, xnes, yns, ynes,
                       reg='Reed'):
    if reg.lower() in ('newyork', 'new_york'):
        from pychron.core.regression.new_york_regressor import NewYorkRegressor as klass
    else:
        from pychron.core.regression.new_york_regressor import ReedYorkRegressor as klass
    reg = klass(xs=xs, ys=ys,
                xserr=xes, yserr=yes,
                xds=xds, xdes=xdes,
                xns=xns, xnes=xnes,
                yns=yns, ynes=ynes)
    reg.calculate()
    return reg
# ============= EOF =============================================



