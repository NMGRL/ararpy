# ===============================================================================
# Copyright 2014 Jake Ross
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
#============= standard library imports ========================
#============= local library imports  ==========================
from uncertainties import ufloat


class ArArConstants(object):
    abundance_40K = 0.000117
    mK = 39.0983
    mO = 15.9994

    lambda_b_v = 4.962e-10
    lambda_b_e = 9.3e-13
    lambda_e_v = 5.81e-11
    lambda_e_e = 1.6e-13

    lambda_Cl36_v = 6.308e-9
    lambda_Cl36_e = 0

    lambda_Ar37_v = 0.01975
    lambda_Ar37_e = 0

    lambda_Ar39_v = 7.068e-6
    lambda_Ar39_e = 0

    atm4036_v = 295.5
    atm4036_e = 0.5
    atm4038_v = 1575
    atm4038_e = 2

    @property
    def atm3836(self):
        return self.atm4036/self.atm4038

    @property
    def lambda_Cl36(self):
        return ufloat(self.lambda_Cl36_v, self.lambda_Cl36_e)

    @property
    def lambda_Ar37(self):
        return ufloat(self.lambda_Ar37_v, self.lambda_Ar37_e)

    @property
    def lambda_Ar39(self):
        return ufloat(self.lambda_Ar39_v, self.lambda_Ar39_e)

    @property
    def atm4036(self):
        return ufloat(self.atm4036_v, self.atm4036_e)

    @property
    def lambda_k(self):
        return self.lambda_b+self.self.lambda_e

    @property
    def lambda_e(self):
        return ufloat(self.lambda_e_v, self.lambda_e_e)

    @property
    def lambda_b(self):
        return ufloat(self.lambda_b_v, self.lambda_b_e)

#============= EOF =============================================



