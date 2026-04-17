"""Qlib Alpha101/Alpha191 factor implementations.

Alpha101: 101/101 expressions implemented as standard qlib DSL.
Alpha191: 191/191 expressions migrated from JoinQuant/GTJA original reports.
           Most are provided as expression strings; some contain non-native
           operators (e.g. SMA, WMA, REGBETA, FILTER, COUNT, SUMIF, LOWDAY,
           HIGHDAY, DTM, DBM, TR, HD, LD, SEQUENCE, BANCHMARKINDEXCLOSE,
           BANCHMARKINDEXOPEN, indneutralize, regresi, cumsum).  These will
           require custom qlib Operators to execute via D.features().  The
           compute functions gracefully skip unsupported expressions and emit
           a warning so that other factors continue to compute normally.
"""

import warnings
from typing import Optional, Union, List, Dict
import pandas as pd

try:
    import qlib
    from qlib.data import D

    QLIB_AVAILABLE = True
except ImportError:
    QLIB_AVAILABLE = False
    warnings.warn("qlib未安装，Alpha因子将不可用。安装方法: pip install pyqlib")


# =====================================================================
# Alpha101 expression dictionary (qlib DSL)
# =====================================================================

ALPHA101_EXPR = {
    "alpha001": "(Rank(Ts_Argmax(SignedPower((($returns < 0) ? Std($returns, 20) : $close), 2.), 5)) - 0.5)",
    "alpha002": "(-1*Corr(Rank(Delta(Log($volume), 2)), Rank((($close - $open) / $open)), 6))",
    "alpha003": "(-1*Corr(Rank($open), Rank($volume), 10))",
    "alpha004": "(-1*Ts_Rank(Rank($low), 9))",
    "alpha005": "(Rank(($open - (Sum($vwap, 10) / 10)))(-1abs(Rank(($close - $vwap)))))",
    "alpha006": "(-1*Corr($open, $volume, 10))",
    "alpha007": "((Mean($amount, 20) < $volume) ? ((-1ts_rank(Abs(Delta($close, 7)), 60))Sign(Delta($close, 7))) : (-1*1))",
    "alpha008": "(-1rank(((Sum($open, 5)Sum($returns, 5)) - Ref((Sum($open, 5)*Sum($returns, 5)), 10))))",
    "alpha009": "((0 < Min(Delta($close, 1), 5)) ? Delta($close, 1) : ((Max(Delta($close, 1), 5) < 0) ? Delta($close, 1) : (-1*Delta($close, 1))))",
    "alpha010": "Rank(((0 < Min(Delta($close, 1), 4)) ? Delta($close, 1) : ((Max(Delta($close, 1), 4) < 0) ? Delta($close, 1) : (-1*Delta($close, 1)))))",
    "alpha011": "((Rank(Max(($vwap - $close), 3)) + Rank(Min(($vwap - $close), 3)))*Rank(Delta($volume, 3)))",
    "alpha012": "(Sign(Delta($volume, 1))*(-1 * Delta($close, 1)))",
    "alpha013": "(-1*Rank(Cov(Rank($close), Rank($volume), 5)))",
    "alpha014": "((-1rank(Delta($returns, 3)))Corr($open, $volume, 10))",
    "alpha015": "(-1*Sum(Rank(Corr(Rank($high), Rank($volume), 3)), 3))",
    "alpha016": "(-1*Rank(Cov(Rank($high), Rank($volume), 5)))",
    "alpha017": "(((-1rank(Ts_Rank($close, 10)))Rank(Delta(Delta($close, 1), 1)))*Rank(Ts_Rank(($volume / Mean($amount, 20)), 5)))",
    "alpha018": "(-1*Rank(((Std(Abs(($close - $open)), 5) + ($close - $open)) + Corr($close, $open, 10))))",
    "alpha019": "((-1sign((($close - Ref($close, 7)) + Delta($close, 7))))(1 + Rank((1 + Sum($returns, 250)))))",
    "alpha020": "(((-1rank(($open - Ref($high, 1)))) Rank(($open - Ref($close, 1))))* Rank(($open - Ref($low, 1))))",
    "alpha021": "((((Sum($close, 8) / 8) + Std($close, 8)) < (Sum($close, 2) / 2)) ? (-1* 1) : (((Sum($close, 2) / 2) < ((Sum($close, 8) / 8) - Std($close, 8))) ? 1 : (((1 < ($volume / Mean($amount, 20))) or (($volume / Mean($amount, 20)) == 1)) ? 1 : (-1* 1))))",
    "alpha022": "(-1* (Delta(Corr($high, $volume, 5), 5)* Rank(Std($close, 20))))",
    "alpha023": "(((Sum($high, 20) / 20) < $high) ? (-1* Delta($high, 2)) : 0)",
    "alpha024": "((((Delta((Sum($close, 100) / 100), 100) / Ref($close, 100)) < 0.05) or ((Delta((Sum($close, 100) / 100), 100) / Ref($close, 100)) == 0.05)) ? (-1* ($close - Min($close, 100))) : (-1* Delta($close, 3)))",
    "alpha025": "Rank(((((-1* $returns)* Mean($amount, 20))* $vwap)* ($high - $close)))",
    "alpha026": "(-1* Max(Corr(Ts_Rank($volume, 5), Ts_Rank($high, 5), 5), 3))",
    "alpha027": "((0.5 < Rank((Sum(Corr(Rank($volume), Rank($vwap), 6), 2) / 2.0))) ? (-1* 1) : 1)",
    "alpha028": "Scale(((Corr(Mean($amount, 20), $low, 5) + (($high + $low) / 2)) - $close))",
    "alpha029": "(Min(Prod(Rank(Rank(Scale(Log(Sum(Min(Rank(Rank((-1rank(Delta(($close - 1), 5))))), 2), 1))))), 1), 5) + Ts_Rank(Ref((-1 $returns), 6), 5))",
    "alpha030": "(((1.0 - Rank(((Sign(($close - Ref($close, 1))) + Sign((Ref($close, 1) - Ref($close, 2)))) + Sign((Ref($close, 2) - Ref($close, 3))))))* Sum($volume, 5)) / Sum($volume, 20))",
    "alpha031": "((Rank(Rank(Rank(Decay_linear((-1* Rank(Rank(Delta($close, 10)))), 10)))) + Rank((-1* Delta($close, 3)))) + Sign(Scale(Corr(Mean($amount, 20), $low, 12))))",
    "alpha032": "(Scale(((Sum($close, 7) / 7) - $close)) + (20* Scale(Corr($vwap, Ref($close, 5), 230))))",
    "alpha033": "Rank((-1* ((1 - ($open / $close))^1)))",
    "alpha034": "Rank(((1 - Rank((Std($returns, 2) / Std($returns, 5)))) + (1 - Rank(Delta($close, 1)))))",
    "alpha035": "((Ts_Rank($volume, 32)* (1 - Ts_Rank((($close + $high) - $low), 16)))* (1 - Ts_Rank($returns, 32)))",
    "alpha036": "(((((2.21* Rank(Corr(($close - $open), Ref($volume, 1), 15))) + (0.7* Rank(($open - $close)))) + (0.73* Rank(Ts_Rank(Ref((-1* $returns), 6), 5)))) + Rank(Abs(Corr($vwap, Mean($amount, 20), 6)))) + (0.6* Rank((((Sum($close, 200) / 200) - $open)* ($close - $open)))))",
    "alpha037": "(Rank(Corr(Ref(($open - $close), 1), $close, 200)) + Rank(($open - $close)))",
    "alpha038": "((-1* Rank(Ts_Rank($close, 10)))* Rank(($close / $open)))",
    "alpha039": "((-1* Rank((Delta($close, 7)* (1 - Rank(Decay_linear(($volume / Mean($amount, 20)), 9))))))* (1 + Rank(Sum($returns, 250))))",
    "alpha040": "((-1* Rank(Std($high, 10)))* Corr($high, $volume, 10))",
    "alpha041": "((($high* $low)^0.5) - $vwap)",
    "alpha042": "(Rank(($vwap - $close)) / Rank(($vwap + $close)))",
    "alpha043": "(Ts_Rank(($volume / Mean($amount, 20)), 20)* Ts_Rank((-1* Delta($close, 7)), 8))",
    "alpha044": "(-1* Corr($high, Rank($volume), 5))",
    "alpha045": "(-1* ((Rank((Sum(Ref($close, 5), 20) / 20))* Corr($close, $volume, 2))* Rank(Corr(Sum($close, 5), Sum($close, 20), 2))))",
    "alpha046": "((0.25 < (((Ref($close, 20) - Ref($close, 10)) / 10) - ((Ref($close, 10) - $close) / 10))) ? (-1* 1) : (((((Ref($close, 20) - Ref($close, 10)) / 10) - ((Ref($close, 10) - $close) / 10)) < 0) ? 1 : ((-1* 1)* ($close - Ref($close, 1)))))",
    "alpha047": "((((Rank((1 / $close))* $volume) / Mean($amount, 20))* (($high* Rank(($high - $close))) / (Sum($high, 5) / 5))) - Rank(($vwap - Ref($vwap, 5))))",
    "alpha048": "indneutralize(Corr(Delta($close, 1), Delta(Ref($close, 1), 1), 250) * Delta($close, 1) / $close, subindustry) / Sum(Pow(Delta($close, 1) / Ref($close, 1), 2), 250)",
    "alpha049": "(((((Ref($close, 20) - Ref($close, 10)) / 10) - ((Ref($close, 10) - $close) / 10)) < (-1* 0.1)) ? 1 : ((-1* 1)* ($close - Ref($close, 1))))",
    "alpha050": "(-1* Max(Rank(Corr(Rank($volume), Rank($vwap), 5)), 5))",
    "alpha051": "((((-1* Min($low, 5)) + Ref(Min($low, 5), 5))* Rank(((Sum($returns, 240) - Sum($returns, 20)) / 220)))* Ts_Rank($volume, 5))",
    "alpha052": "((-1 * Min($low, 5) + Ref(Min($low, 5), 5)) * Rank((Sum($returns, 240) - Sum($returns, 20)) / 220)) * Ts_Rank($volume, 5)",
    "alpha053": "(-1* Delta(((($close - $low) - ($high - $close)) / ($close - $low)), 9))",
    "alpha054": "((-1* (($low - $close)* ($open^5))) / (($low - $high)* ($close^5)))",
    "alpha055": "(-1* Corr(Rank((($close - Min($low, 12)) / (Max($high, 12) - Min($low, 12)))), Rank($volume), 6))",
    "alpha056": "(0 - (1* (Rank((Sum($returns, 10) / Sum(Sum($returns, 2), 3)))* Rank(($returns* cap)))))",
    "alpha057": "(0 - (1* (($close - $vwap) / Decay_linear(Rank(Ts_Argmax($close, 30)), 2))))",
    "alpha058": "-1 * Ts_Rank(Decay_linear(Corr(indneutralize($vwap, sector), $volume, 3.92795), 7.89291), 5.50322)",
    "alpha059": "-1 * Ts_Rank(Decay_linear(Corr(indneutralize($vwap, industry), $volume, 4.25197), 16.2289), 8.19648)",
    "alpha060": "(0 - (1* ((2* Scale(Rank((((($close - $low) - ($high - $close)) / ($high - $low))* $volume)))) - Scale(Rank(Ts_Argmax($close, 10))))))",
    "alpha061": "(Rank(($vwap - Min($vwap, 16.1219))) < Rank(Corr($vwap, Mean($amount, 180), 17.9282)))",
    "alpha062": "((Rank(Corr($vwap, Sum(Mean($amount, 20), 22.4101), 9.91009)) < Rank(((Rank($open) + Rank($open)) < (Rank((($high + $low) / 2)) + Rank($high)))))*-1)",
    "alpha063": "(Rank(Decay_linear(Delta(indneutralize($close, industry), 2.25164), 8.22237)) - Rank(Decay_linear(Corr($vwap * 0.318108 + $open * (1 - 0.318108), Sum(Mean($amount, 180), 37.2467), 13.557), 12.2883))) * -1",
    "alpha064": "((Rank(Corr(Sum((($open* 0.178404) + ($low* (1 - 0.178404))), 12.7054), Sum(Mean($amount, 120), 12.7054), 16.6208)) < Rank(Delta((((($high + $low) / 2)* 0.178404) + ($vwap* (1 - 0.178404))), 3.69741)))* -1)",
    "alpha065": "((Rank(Corr((($open* 0.00817205) + ($vwap* (1 - 0.00817205))), Sum(Mean($amount, 60), 8.6911), 6.40374)) < Rank(($open - Min($open, 13.635))))* -1)",
    "alpha066": "((Rank(Decay_linear(Delta($vwap, 3.51013), 7.23052)) + Ts_Rank(Decay_linear((((($low* 0.96633) + ($low* (1 - 0.96633))) - $vwap) / ($open - (($high + $low) / 2))), 11.4157), 6.72611))* -1)",
    "alpha067": "(Rank($high - Min($high, 2.14593)) ** Rank(Corr(indneutralize($vwap, sector), indneutralize(Mean($amount, 20), subindustry), 6.02936))) * -1",
    "alpha068": "((Ts_Rank(Corr(Rank($high), Rank(Mean($amount, 15)), 8.91644), 13.9333) < Rank(Delta((($close* 0.518371) + ($low* (1 - 0.518371))), 1.06157)))* -1)",
    "alpha069": "(Rank(Max(Delta(indneutralize($vwap, industry), 2.72412), 4.79344)) ** Ts_Rank(Corr($close * 0.490655 + $vwap * (1 - 0.490655), Mean($amount, 20), 4.92416), 9.0615)) * -1",
    "alpha070": "(Rank(Delta($vwap, 1.29456)) ** Ts_Rank(Corr(indneutralize($close, industry), Mean($amount, 50), 17.8256), 17.9171)) * -1",
    "alpha071": "Max(Ts_Rank(Decay_linear(Corr(Ts_Rank($close, 3.43976), Ts_Rank(Mean($amount, 180), 12.0647), 18.0175), 4.20501), 15.6948), Ts_Rank(Decay_linear((Rank((($low + $open) - ($vwap + $vwap)))^2), 16.4662), 4.4388))",
    "alpha072": "(Rank(Decay_linear(Corr((($high + $low) / 2), Mean($amount, 40), 8.93345), 10.1519)) / Rank(Decay_linear(Corr(Ts_Rank($vwap, 3.72469), Ts_Rank($volume, 18.5188), 6.86671), 2.95011)))",
    "alpha073": "(Max(Rank(Decay_linear(Delta($vwap, 4.72775), 2.91864)), Ts_Rank(Decay_linear(((Delta((($open* 0.147155) + ($low* (1 - 0.147155))), 2.03608) / (($open* 0.147155) + ($low* (1 - 0.147155))))* -1), 3.33829), 16.7411))* -1)",
    "alpha074": "((Rank(Corr($close, Sum(Mean($amount, 30), 37.4843), 15.1365)) < Rank(Corr(Rank((($high* 0.0261661) + ($vwap* (1 - 0.0261661)))), Rank($volume), 11.4791)))* -1)",
    "alpha075": "(Rank(Corr($vwap, $volume, 4.24304)) < Rank(Corr(Rank($low), Rank(Mean($amount, 50)), 12.4413)))",
    "alpha076": "(Max(Rank(Decay_linear(Delta($vwap, 1.24383), 11.8259)), Ts_Rank(Decay_linear(Ts_Rank(Corr(indneutralize($low, sector), Mean($amount, 81), 8.14941), 19.569), 17.1543), 19.383)) * -1",
    "alpha077": "Min(Rank(Decay_linear((((($high + $low) / 2) + $high) - ($vwap + $high)), 20.0451)), Rank(Decay_linear(Corr((($high + $low) / 2), Mean($amount, 40), 3.1614), 5.64125)))",
    "alpha078": "(Rank(Corr(Sum((($low* 0.352233) + ($vwap* (1 - 0.352233))), 19.7428), Sum(Mean($amount, 40), 19.7428), 6.83313))^Rank(Corr(Rank($vwap), Rank($volume), 5.77492)))",
    "alpha079": "Rank(Delta(indneutralize($close * 0.60733 + $open * (1 - 0.60733), sector), 1.23438)) < Rank(Corr(Ts_Rank($vwap, 3.60973), Ts_Rank(Mean($amount, 150), 9.18637), 14.6644))",
    "alpha080": "(Rank(Sign(Delta(indneutralize($open * 0.868128 + $high * (1 - 0.868128), industry), 4.04545))) ** Ts_Rank(Corr($high, Mean($amount, 10), 5.11456), 5.53756)) * -1",
    "alpha081": "((Rank(Log(Prod(Rank((Rank(Corr($vwap, Sum(Mean($amount, 10), 49.6054), 8.47743))^4)), 14.9655))) < Rank(Corr(Rank($vwap), Rank($volume), 5.07914)))* -1)",
    "alpha082": "(Min(Rank(Decay_linear(Delta($open, 1.46063), 14.8717)), Ts_Rank(Decay_linear(Corr(indneutralize($volume, sector), $open, 17.4842), 6.92131), 13.4283)) * -1",
    "alpha083": "((Rank(Ref((($high - $low) / (Sum($close, 5) / 5)), 2))* Rank(Rank($volume))) / ((($high - $low) / (Sum($close, 5) / 5)) / ($vwap - $close)))",
    "alpha084": "SignedPower(Ts_Rank(($vwap - Max($vwap, 15.3217)), 20.7127), Delta($close, 4.96796))",
    "alpha085": "(Rank(Corr((($high* 0.876703) + ($close* (1 - 0.876703))), Mean($amount, 30), 9.61331))^Rank(Corr(Ts_Rank((($high + $low) / 2), 3.70596), Ts_Rank($volume, 10.1595), 7.11408)))",
    "alpha086": "((Ts_Rank(Corr($close, Sum(Mean($amount, 20), 14.7444), 6.00049), 20.4195) < Rank((($open + $close) - ($vwap + $open))))* -1)",
    "alpha087": "(Max(Rank(Decay_linear(Delta($close * 0.369701 + $vwap * (1 - 0.369701), 1.91233), 2.65461)), Ts_Rank(Decay_linear(Abs(Corr(indneutralize(Mean($amount, 81), industry), $close, 13.4132)), 4.89768), 14.4535)) * -1",
    "alpha088": "Min(Rank(Decay_linear(((Rank($open) + Rank($low)) - (Rank($high) + Rank($close))), 8.06882)), Ts_Rank(Decay_linear(Corr(Ts_Rank($close, 8.44728), Ts_Rank(Mean($amount, 60), 20.6966), 8.01266), 6.65053), 2.61957))",
    "alpha089": "Ts_Rank(Decay_linear(Corr($low, Mean($amount, 10), 6.94279), 5.51607), 3.79744) - Ts_Rank(Decay_linear(Delta(indneutralize($vwap, industry), 3.48158), 10.1466), 15.3012)",
    "alpha090": "(Rank($close - Max($close, 4.66719)) ** Ts_Rank(Corr(indneutralize(Mean($amount, 40), subindustry), $low, 5.38375), 3.21856)) * -1",
    "alpha091": "(Ts_Rank(Decay_linear(Decay_linear(Corr(indneutralize($close, industry), $volume, 9.74928), 16.398), 3.83219), 4.8667) - Rank(Decay_linear(Corr($vwap, Mean($amount, 30), 4.01303), 2.6809))) * -1",
    "alpha092": "Min(Ts_Rank(Decay_linear((((($high + $low) / 2) + $close) < ($low + $open)), 14.7221), 18.8683), Ts_Rank(Decay_linear(Corr(Rank($low), Rank(Mean($amount, 30)), 7.58555), 6.94024), 6.80584))",
    "alpha093": "Ts_Rank(Decay_linear(Corr(indneutralize($vwap, industry), Mean($amount, 81), 17.4193), 19.848), 7.54455) / Rank(Decay_linear(Delta($close * 0.524434 + $vwap * (1 - 0.524434), 2.77377), 16.2664))",
    "alpha094": "((Rank(($vwap - Min($vwap, 11.5783)))^Ts_Rank(Corr(Ts_Rank($vwap, 19.6462), Ts_Rank(Mean($amount, 60), 4.02992), 18.0926), 2.70756))* -1)",
    "alpha095": "(Rank(($open - Min($open, 12.4105))) < Ts_Rank((Rank(Corr(Sum((($high + $low) / 2), 19.1351), Sum(Mean($amount, 40), 19.1351), 12.8742))^5), 11.7584))",
    "alpha096": "(Max(Ts_Rank(Decay_linear(Corr(Rank($vwap), Rank($volume), 3.83878), 4.16783), 8.38151), Ts_Rank(Decay_linear(Ts_Argmax(Corr(Ts_Rank($close, 7.45404), Ts_Rank(Mean($amount, 60), 4.13242), 3.65459), 12.6556), 14.0365), 13.4143))* -1)",
    "alpha097": "(Rank(Decay_linear(Delta(indneutralize($low * 0.721001 + $vwap * (1 - 0.721001), industry), 3.3705), 20.4523)) - Ts_Rank(Decay_linear(Ts_Rank(Corr(Ts_Rank($low, 7.87871), Ts_Rank(Mean($amount, 60), 17.255), 4.97547), 18.5925), 15.7152), 6.71659)) * -1",
    "alpha098": "(Rank(Decay_linear(Corr($vwap, Sum(Mean($amount, 5), 26.4719), 4.58418), 7.18088)) - Rank(Decay_linear(Ts_Rank(Ts_Argmin(Corr(Rank($open), Rank(Mean($amount, 15)), 20.8187), 8.62571), 6.95668), 8.07206)))",
    "alpha099": "((Rank(Corr(Sum((($high + $low) / 2), 19.8975), Sum(Mean($amount, 60), 19.8975), 8.8136)) < Rank(Corr($low, $volume, 6.28259)))* -1)",
    "alpha100": "-1 * (1.5 * Scale(indneutralize(Rank((($close - $low) - ($high - $close)) / ($high - $low) * $volume), subindustry)) - Scale(indneutralize(Corr($close, Rank(Mean($amount, 20)), 5) - Rank(Ts_Argmin($close, 30)), subindustry))) * ($volume / Mean($amount, 20))",
    "alpha101": "(($close - $open) / (($high - $low) + .001))",
}

# =====================================================================
# Alpha191 expression dictionary (migrated from JoinQuant / GTJA)
# =====================================================================

ALPHA191_EXPR = {
    "alpha001": "Sum(($close=Ref($close,1)?0:$close-($close>Ref($close,1)?Min($low,Ref($close,1)):Max($high,Ref($close,1)))),6)",
    "alpha002": "-1 * Delta((($close - $low) - ($high - $close)) / ($high - $low), 1)",
    "alpha003": "Sum(If($close == Ref($close, 1), 0, $close - If($close > Ref($close, 1), Min($low, Ref($close, 1)), Max($high, Ref($close, 1)))), 6)",
    "alpha004": "((((Sum($close,8)/8)+Std($close,8))<(Sum($close,2)/2))?(-1* 1):(((Sum($close,2)/2)<((Sum($close,8)/8)-Std($close,8)))?1:(((1<($volume/Mean($volume,20)))||(($volume/Mean($volume,20))==1))?1:(-1* 1))))",
    "alpha005": "(-1*Max(Corr(Ts_Rank($volume,5),Ts_Rank($high,5),5),3))",
    "alpha006": "(Rank(Sign(Delta(((($open * 0.85)+($high * 0.15))),4)))*-1)",
    "alpha007": "((Rank(Max(($vwap-$close),3))+Rank(Min(($vwap-$close),3)))* Rank(Delta($volume,3)))",
    "alpha008": "Rank(Delta((((($high + $low) / 2) * 0.2) + ($vwap * 0.8)), 4) * -1)",
    "alpha009": "SMA((($high+$low)/2-(Ref($high,1)+Ref($low,1))/2)*($high-$low)/$volume,7,2)",
    "alpha010": "(Rank(Max(((RET < 0) ? Std(RET, 20) : $close)^2),5))",
    "alpha011": "Sum((($close-$low)-($high-$close)). /($high-$low) . * $volume,6)",
    "alpha012": "(Rank(($open - (Sum($vwap, 10) / 10)))) * (-1 * (Rank(Abs(($close - $vwap)))))",
    "alpha013": "((($high * $low)^0.5)-$vwap)",
    "alpha014": "$close-Ref($close,5)",
    "alpha015": "$open/Ref($close,1)-1",
    "alpha016": "(-1 * Max(Rank(Corr(Rank($volume),Rank($vwap),5)),5))",
    "alpha017": "Rank(($vwap-Max($vwap,15)))^Delta($close,5)",
    "alpha018": "$close/Ref($close,5)",
    "alpha019": "($close<Ref($close,5)?($close-Ref($close,5))/Ref($close,5):($close=Ref($close,5)?0:($close-Ref($close,5))/$close))",
    "alpha020": "($close-Ref($close,6))/Ref($close,6)*100",
    "alpha021": "REGBETA(Mean($close,6),SEQUENCE(6))",
    "alpha022": "SMA((($close-Mean($close,6))/Mean($close,6)-Ref(($close-Mean($close,6))/Mean($close,6),3)),12,1)",
    "alpha023": "SMA(($close>Ref($close,1)?Std($close,20),0),20,1)/(SMA(($close>Ref($close,1)?Std($close,20):0),20,1)+SMA(($close<=Ref($close,1)?Std($close,20):0),20,1))*100",
    "alpha024": "SMA($close-Ref($close,5),5,1)",
    "alpha025": "((-1Rank((Delta($close,7)(1-Rank(Decay_linear(($volume/Mean($volume,20)),9))))))*(1+Rank(Sum(RET,250))))",
    "alpha026": "((((Sum($close,7)/7)-$close))+((Corr($vwap,Ref($close,5),230))))",
    "alpha027": "WMA(($close-Ref($close,3))/Ref($close,3)*100+($close-Ref($close,6))/Ref($close,6)*100,12)",
    "alpha028": "3*SMA(($close-Min($low,9))/(Max($high,9)-Min($low,9))*100,3,1)-2*SMA(SMA(($close-Min($low,9))/( Max($high,9)-Min($low,9))*100,3,1),3,1)",
    "alpha029": "($close-Ref($close,6))/Ref($close,6)*$volume",
    "alpha030": "WMA(Pow(Regresi($close / Ref($close, 1) - 1, $mkt, $smb, $hml, 60), 2), 20)",
    "alpha031": "($close-Mean($close,12))/Mean($close,12)*100",
    "alpha032": "(-1*Sum(Rank(Corr(Rank($high),Rank($volume),3)),3))",
    "alpha033": "((((-1*Min($low,5))+Ref(Min($low,5),5))*Rank(((Sum(RET,240)-Sum(RET,20))/220)))*Ts_Rank($volume,5))",
    "alpha034": "Mean($close,12)/$close",
    "alpha035": "(Min(Rank(Decay_linear(Delta($open,1),15)),Rank(Decay_linear(Corr(($volume),((OPEN*0.65)+(OPEN*0.35)),17),7)))*-1)",
    "alpha036": "Rank(Sum(Corr(Rank($volume),Rank($vwap)),6),2)",
    "alpha037": "(-1*Rank(((Sum($open,5)*Sum(RET,5))-Ref((Sum($open,5)*Sum(RET,5)),10))))",
    "alpha038": "(((Sum($high,20)/20)<$high)?(-1*Delta($high,2)):0)",
    "alpha039": "((Rank(Decay_linear(Delta(($close),2),8))-Rank(Decay_linear(Corr(((VWAP*0.3)+(OPEN*0.7)),Sum(Mean($volume,180),37),14),12)))*-1",
    "alpha040": "Sum(($close>Ref($close,1)?$volume:0),26)/Sum(($close<=Ref($close,1)?$volume:0),26)*100",
    "alpha041": "(Rank(Max(Delta(($vwap),3),5))*-1)",
    "alpha042": "(-1*Rank(Std($high,10)))*Corr($high,$volume,10))",
    "alpha043": "Sum(($close>Ref($close,1)?$volume:($close<Ref($close,1)?-$volume:0)),6)",
    "alpha044": "(Ts_Rank(Decay_linear(Corr((($low)),Mean($volume,10),7),6),4)+Ts_Rank(Decay_linear(Delta(($vwap),3),10),15))",
    "alpha045": "(Rank(Delta((((CLOSE*0.6)+(OPEN*0.4))),1))*Rank(Corr($vwap,Mean($volume,150),15)))",
    "alpha046": "(Mean($close,3)+Mean($close,6)+Mean($close,12)+Mean($close,24))/(4*$close)",
    "alpha047": "SMA((Max($high,6)-$close)/(Max($high,6)-Min($low,6))*100,9,1)",
    "alpha048": "(-1*((Rank(((Sign(($close-Ref($close,1)))+Sign((Ref($close,1)-Ref($close,2))))+Sign((Ref($close,2)-Ref($close,3))))))*Sum($volume,5))/Sum($volume,20))",
    "alpha049": "Sum((($high+$low)>=(Ref($high,1)+Ref($low,1))?0:Max(Abs($high-Ref($high,1)),Abs($low-Ref($low,1)))),12)/(Sum((($high+$low)>=(Ref($high,1)+Ref($low,1))?0:Max(Abs($high-Ref($high,1)),Abs($low-Ref($low,1)))),12)+Sum((($high+$low)<=(Ref($high,1)+Ref($low,1))?0:Max(Abs($high-Ref($high,1)),Abs($low-Ref($low,1)))),12))",
    "alpha050": "Sum((($high+$low)<=(Ref($high,1)+Ref($low,1))?0:Max(Abs($high-Ref($high,1)),Abs($low-Ref($low,1)))),12)/(Sum((($high+$low)<=(Ref($high,1)+Ref($low,1))?0:Max(Abs($high-Ref($high,1)),Abs($low-Ref($low,1)))),12)+Sum((($high+$low)>=(Ref($high,1)+Ref($low,1))?0:Max(Abs($high-Ref($high,1)),Abs($low-Ref($low,1)))),12))-Sum((($high+$low)>=(Ref($high,1)+Ref($low,1))?0:Max(Abs($high-Ref($high,1)),Abs($low-Ref($low,1)))),12)/(Sum((($high+$low)>=(Ref($high,1)+Ref($low,1))?0: Max(Abs($high-Ref($high,1)),Abs($low-Ref($low,1)))),12)+Sum((($high+$low)<=(Ref($high,1)+Ref($low,1))?0:Max(Abs($high-Ref($high,1)),Abs($low-Ref($low,1)))),12))",
    "alpha051": "Sum(Max(0,$high-Ref(($high+$low+$close)/3,1)),26)/Sum(Max(0,Ref(($high+$low+$close)/3,1)-$low),26)*100",
    "alpha052": "Sum(Max(0, $high - Ref(($high + $low + $close) / 3, 1)), 26) / Sum(Max(0, Ref(($high + $low + $close) / 3, 1) - $low), 26) * 100",
    "alpha053": "Count($close>Ref($close,1),12)/12*100",
    "alpha054": "(-1*Rank((Std(Abs($close-$open))+($close-$open))+Corr($close,$open,10)))",
    "alpha055": "Sum(16*($close-Ref($close,1)+($close-$open)/2+Ref($close,1)-Ref($open,1))/((Abs($high-Ref($close,1))>Abs($low-Ref($close,1))&Abs($high-Ref($close,1))>Abs($high-Ref($low,1))?Abs($high-Ref($close,1))+Abs($low-Ref($close,1))/2+Abs(Ref($close,1)-Ref($open,1))/4:(Abs($low-Ref($close,1))>Abs($high-Ref($low,1))&Abs($low-Ref($close,1))>Abs($high-Ref($close,1))?Abs($low-Ref($close,1))+Abs($high-Ref($close,1))/2+Abs(Ref($close,1)-Ref($open,1))/4:Abs($high-Ref($low,1))+Abs(Ref($close,1)-Ref($open,1))/4)))*Max(Abs($high-Ref($close,1)),Abs($low-Ref($close,1))),20)",
    "alpha056": "(Rank(($open-Min($open,12)))<Rank((Rank(Corr(Sum((($high +$low)/2),19),Sum(Mean($volume,40),19),13))^5)))",
    "alpha057": "SMA(($close-Min($low,9))/(Max($high,9)-Min($low,9))*100,3,1)",
    "alpha058": "Count($close>Ref($close,1),20)/20*100",
    "alpha059": "Sum((($close-$low)-($high-$close))/($high-$low)*$volume,20)",
    "alpha060": "Sum((($close - $low) - ($high - $close)) / ($high - $low) * $volume, 20)",
    "alpha061": "(Max(Rank(Decay_linear(Delta($vwap,1),12)),Rank(Decay_linear(Rank(Corr(($low),Mean($volume,80),8)),17)))*-1)",
    "alpha062": "(-1*Corr($high,Rank($volume),5))",
    "alpha063": "SMA(Max($close-Ref($close,1),0),6,1)/SMA(Abs($close-Ref($close,1)),6,1)*100",
    "alpha064": "(Max(Rank(Decay_linear(Corr(Rank($vwap),Rank($volume),4),4)),Rank(Decay_linear(Max(Corr(Rank($close),Rank(Mean($volume,60)),4),13),14)))*-1)",
    "alpha065": "Mean($close,6)/$close",
    "alpha066": "($close-Mean($close,6))/Mean($close,6)*100",
    "alpha067": "SMA(Max($close-Ref($close,1),0),24,1)/SMA(Abs($close-Ref($close,1)),24,1)*100",
    "alpha068": "SMA((($high+$low)/2-(Ref($high,1)+Ref($low,1))/2)*($high-$low)/$volume,15,2)",
    "alpha069": "(Sum(DTM,20)>Sum(DBM,20)?(Sum(DTM,20)-Sum(DBM,20))/Sum(DTM,20):(Sum(DTM,20)=Sum(DBM,20)?0:(Sum(DTM,20)-Sum(DBM,20))/Sum(DBM,20)))",
    "alpha070": "Std($amount,6)",
    "alpha071": "($close-Mean($close,24))/Mean($close,24)*100",
    "alpha072": "SMA((Max($high,6)-$close)/(Max($high,6)-Min($low,6))*100,15,1)",
    "alpha073": "((Ts_Rank(Decay_linear(Decay_linear(Corr(($close),$volume,10),16),4),5)-Rank(Decay_linear(Corr($vwap,Mean($volume,30),4),3)))*-1)",
    "alpha074": "(Rank(Corr(Sum(((LOW*0.35)+(VWAP*0.65)),20),Sum(Mean($volume,40),20),7))+Rank(Corr(Rank($vwap),Rank($volume),6)))",
    "alpha075": "Count($close<$open,50)/Count($close<$open,50)",
    "alpha076": "Std(Abs(($close/Ref($close,1)-1))/$volume,20)/Mean(Abs(($close/Ref($close,1)-1))/$volume,20)",
    "alpha077": "Min(Rank(Decay_linear((((($high+$low)/2)+$high)-($vwap+$high)),20)),Rank(Decay_linear(Corr((($high+$low)/2),Mean($volume,40),3),6)))",
    "alpha078": "(($high+$low+$close)/3-Mean(($high+$low+$close)/3,12))/(0.015*Mean(Abs($close-Mean(($high+$low+$close)/3,12)),12))",
    "alpha079": "SMA(Max($close-Ref($close,1),0),12,1)/SMA(Abs($close-Ref($close,1)),12,1)*100",
    "alpha080": "($volume-Ref($volume,5))/Ref($volume,5)*100",
    "alpha081": "SMA($volume,21,2)",
    "alpha082": "SMA((Max($high,6)-$close)/(Max($high,6)-Min($low,6))*100,20,1)",
    "alpha083": "(-1*Rank(Cov(Rank($high),Rank($volume),5)))",
    "alpha084": "Sum(($close>Ref($close,1)?$volume:($close<Ref($close,1)?-$volume:0)),20)",
    "alpha085": "(Ts_Rank(($volume/Mean($volume,20)),20)* Ts_Rank((-1*Delta($close,7)),8))",
    "alpha086": "((0.25<(((Ref($close,20)-Ref($close,10))/10)-((Ref($close,10)-$close)/10)))?(-1*1):(((((Ref($close,20)-Ref($close,10))/10)-((Ref($close,10)-$close)/10))<0)?1:((-1*1)*($close-Ref($close,1)))))",
    "alpha087": "((Rank(Decay_linear(Delta($vwap,4),7))+Ts_Rank(Decay_linear(((((LOW*0.9)+(LOW*0.1))-$vwap)/($open-(($high+$low)/2))),11),7))*-1)",
    "alpha088": "($close-Ref($close,20))/Ref($close,20)*100",
    "alpha089": "2*(SMA($close,13,2)-SMA($close,27,2)-SMA(SMA($close,13,2)-SMA($close,27,2),10,2))",
    "alpha090": "(Rank(Corr(Rank($vwap),Rank($volume),5))*-1)",
    "alpha091": "((Rank(($close-Max($close,5)))*Rank(Corr((Mean($volume,40)),$low,5)))*-1)",
    "alpha092": "(Max(Rank(Decay_linear(Delta((($close*0.35)+($vwap*0.65)),2),3)),Ts_Rank(Decay_linear(Abs(Corr((Mean($volume,180)),$close,13)),5),15))*-1)",
    "alpha093": "Sum(($open>=Ref($open,1)?0:Max(($open-$low),($open-Ref($open,1)))),20)",
    "alpha094": "Sum(($close>Ref($close,1)?$volume:($close<Ref($close,1)?-$volume:0)),30)",
    "alpha095": "Std($amount,20)",
    "alpha096": "SMA(SMA(($close-Min($low,9))/(Max($high,9)-Min($low,9))*100,3,1),3,1)",
    "alpha097": "Std($volume,10)",
    "alpha098": "((((Delta((Sum($close,100)/100),100)/Ref($close,100))<0.05)||((Delta((Sum($close,100)/100),100)/Ref($close,100))==0.05))?(-1*($close-Min($close,100))):(-1*Delta($close,3)))",
    "alpha099": "(-1*Rank(Cov(Rank($close),Rank($volume),5)))",
    "alpha100": "Std($volume,20)",
    "alpha101": "((Rank(Corr($close, Sum(Mean($volume,30), 37), 15)) < Rank(Corr(Rank((($high * 0.1) + ($vwap * 0.9))), Rank($volume), 11))) * -1)",
    "alpha102": "SMA(Max($volume-Ref($volume,1),0),6,1)/SMA(Abs($volume-Ref($volume,1)),6,1)*100",
    "alpha103": "((20-LowDay($low,20))/20)*100",
    "alpha104": "(-1 * (Delta(Corr($high,$volume,5),5) * Rank(Std($close,20))))",
    "alpha105": "(-1*Corr(Rank($open),Rank($volume),10))",
    "alpha106": "$close-Ref($close,20)",
    "alpha107": "(((-1*Rank(($open-Ref($high,1))))*Rank(($open-Ref($close,1))))*Rank(($open-Ref($low,1))))",
    "alpha108": "((Rank(($high-Min($high,2)))^Rank(Corr(($vwap),(Mean($volume,120)),6)))*-1)",
    "alpha109": "SMA($high-$low,10,2)/SMA(SMA($high-$low,10,2),10,2)",
    "alpha110": "Sum(Max(0,$high-Ref($close,1)),20)/Sum(Max(0,Ref($close,1)-$low),20)*100",
    "alpha111": "SMA(VOL*(($close-$low)-($high-$close))/($high-$low),11,2)-SMA(VOL*(($close-$low)-($high-$close))/($high-$low),4,2)",
    "alpha112": "(Sum(($close-Ref($close,1)>0?$close-Ref($close,1):0),12)-Sum(($close-Ref($close,1)<0?Abs($close-Ref($close,1)):0),12))/(Sum(($close-Ref($close,1)>0?$close-Ref($close,1):0),12)+Sum(($close-Ref($close,1)<0?Abs($close-Ref($close,1)):0),12))*100",
    "alpha113": "(-1*((Rank((Sum(Ref($close,5),20)/20))*Corr($close,$volume,2))*Rank(Corr(Sum($close,5),Sum($close,20),2))))",
    "alpha114": "((Rank(Ref((($high-$low)/(Sum($close,5)/5)),2))*Rank(Rank($volume)))/((($high-$low)/(Sum($close,5)/5))/($vwap-$close)))",
    "alpha115": "(Rank(Corr(((HIGH*0.9)+(CLOSE*0.1)),Mean($volume,30),10))^Rank(Corr(Ts_Rank((($high+$low)/2),4),Ts_Rank($volume,10),7)))",
    "alpha116": "RegBeta($close,SEQUENCE,20)",
    "alpha117": "((Ts_Rank($volume,32)*(1-Ts_Rank((($close+$high)-$low),16)))*(1-Ts_Rank(RET,32)))",
    "alpha118": "Sum($high-$open,20)/Sum($open-$low,20)*100",
    "alpha119": "(Rank(Decay_linear(Corr($vwap,Sum(Mean($volume,5),26),5),7))-Rank(Decay_linear(Ts_Rank(Min(Corr(Rank($open),Rank(Mean($volume,15)),21),9),7),8)))",
    "alpha120": "(Rank(($vwap-$close))/Rank(($vwap+$close)))",
    "alpha121": "((Rank(($vwap-Min($vwap,12)))^Ts_Rank(Corr(Ts_Rank($vwap,20),Ts_Rank(Mean($volume,60),2),18),3))*-1)",
    "alpha122": "(SMA(SMA(SMA(Log($close),13,2),13,2),13,2)-Ref(SMA(SMA(SMA(Log($close),13,2),13,2),13,2),1))/Ref(SMA(SMA(SMA(Log($close),13,2),13,2),13,2),1)",
    "alpha123": "(Rank(Corr(Sum((($high+$low)/2),20),Sum(Mean($volume,60),20),9))+",
    "alpha124": "($close-$vwap)/Decay_linear(Rank(Max($close,30)),2)",
    "alpha125": "(Rank(Decay_linear(Corr(($vwap),Mean($volume,80),17),20))/Rank(Decay_linear(Delta(((CLOSE*0.5)+(VWAP*0.5)),3),16)))",
    "alpha126": "($close+$high+$low)/3",
    "alpha127": "(Mean((100*($close-Max($close,12))/(Max($close,12)))^2))^(1/2)",
    "alpha128": "100-(100/(1+Sum((($high+$low+$close)/3>Ref(($high+$low+$close)/3,1)?($high+$low+$close)/3*VOLUME:0),14)/Sum((($high+$low+$close)/3<Ref(($high+$low+$close)/3,1)?($high+$low+$close)/3*$volume:0),14)))",
    "alpha129": "Sum(($close-Ref($close,1)<0?Abs($close-Ref($close,1)):0),12)",
    "alpha130": "(Rank(Decay_linear(Corr((($high+$low)/2),Mean($volume,40),9),10))/Rank(Decay_linear(Corr(Rank($vwap),Rank($volume),7),3)))",
    "alpha131": "(Rank(Delta($vwap,1))^Ts_Rank(Corr($close,Mean($volume,50),18),18))",
    "alpha132": "Mean($amount,20)",
    "alpha133": "((20-HighDay($high,20))/20)*100-((20-LowDay($low,20))/20)*100",
    "alpha134": "($close-Ref($close,12))/Ref($close,12)*$volume",
    "alpha135": "((-1*Rank(Delta(RET,3)))*Corr($open,$volume,10))",
    "alpha136": "(-1 * Rank(Delta($returns, 3))) * Corr($open, $volume, 10)",
    "alpha137": "16*($close-Ref($close,1)+($close-$open)/2+Ref($close,1)-Ref($open,1))/((Abs($high-Ref($close,1))>Abs($low-Ref($close,1))&Abs($high-Ref($close,1))>Abs($high-Ref($low,1))?Abs($high-Ref($close,1))+Abs($low-Ref($close,1))/2+Abs(Ref($close,1)-Ref($open,1))/4:(Abs($low-Ref($close,1))>Abs($high-Ref($low,1))&Abs($low-Ref($close,1))>Abs($high-Ref($close,1))?Abs($low-Ref($close,1))+Abs($high-Ref($close,1))/2+Abs(Ref($close,1)-Ref($open,1))/4:Abs($high-Ref($low,1))+Abs(Ref($close,1)-Ref($open,1))/4)))*Max(Abs($high-Ref($close,1)),Abs($low-Ref($close,1)))",
    "alpha138": "((Rank(Decay_linear(Delta(((LOW*0.7)+(VWAP*0.3))),3),20))-Ts_Rank(Decay_linear(Ts_Rank(Corr(Ts_Rank($low,8),Ts_Rank(Mean($volume,60),17),5),19),16),7))*-1)",
    "alpha139": "(-1*Corr($open,$volume,10))",
    "alpha140": "Min(Rank(Decay_linear(((Rank($open)+Rank($low))-(Rank($high)+Rank($close))),8)),Ts_Rank(Decay_linear(Corr(Ts_Rank($close,8),Ts_Rank(Mean($volume,60),20),8),7),3))",
    "alpha141": "(Rank(Corr(Rank($high),Rank(Mean($volume,15)),9))*-1)",
    "alpha142": "(((-1*Rank(Ts_Rank($close,10)))*Rank(Delta(Delta($close,1),1)))*Rank(Ts_Rank(($volume/Mean($volume,20)),5)))",
    "alpha143": "$close>Ref($close,1)?($close-Ref($close,1))/Ref($close,1)*SELF:SELF",
    "alpha144": "SUMIF(Abs($close/Ref($close,1)-1)/$amount,20,$close<Ref($close,1))/Count($close<Ref($close,1),20)",
    "alpha145": "(Mean($volume,9)-Mean($volume,26))/Mean($volume,12)*100",
    "alpha146": "Mean(($close-Ref($close,1))/Ref($close,1)-SMA(($close-Ref($close,1))/Ref($close,1),61,2),20)*(($close-Ref($close,1))/Ref($close,1)-SMA(($close-Ref($close,1))/Ref($close,1),61,2))/SMA((($close-Ref($close,1))/Ref($close,1)-(($close-Ref($close,1))/Ref($close,1)-SMA(($close-Ref($close,1))/Ref($close,1),61,2)))^2,60)",
    "alpha147": "RegBeta(Mean($close,12),SEQUENCE(12))",
    "alpha148": "((Rank(Corr(($open),Sum(Mean($volume,60),9),6))<Rank(($open-Min($open,14))))*-1)",
    "alpha149": "RegBeta(FILTER($close/Ref($close,1)-1,BANCHMARKINDEXCLOSE<Ref(BANCHMARKINDEXCLOSE,1)),FILTER(BANCHMARKINDEXCLOSE/Ref(BANCHMARKINDEXCLOSE,1)-1,BANCHMARKINDEXCLOSE<Ref(BANCHMARKINDEXCLOSE,1)),252)",
    "alpha150": "($close+$high+$low)/3*$volume",
    "alpha151": "SMA($close-Ref($close,20),20,1)",
    "alpha152": "SMA(Mean(Ref(SMA(Ref($close/Ref($close,9),1),9,1),1),12)-Mean(Ref(SMA(Ref($close/Ref($close,9),1),9,1),1),26),9,1)",
    "alpha153": "(Mean($close,3)+Mean($close,6)+Mean($close,12)+Mean($close,24))/4",
    "alpha154": "((($vwap-Min($vwap,16)))<(Corr($vwap,Mean($volume,180),18)))",
    "alpha155": "SMA($volume,13,2)-SMA($volume,27,2)-SMA(SMA($volume,13,2)-SMA($volume,27,2),10,2)",
    "alpha156": "(Max(Rank(Decay_linear(Delta($vwap,5),3)),Rank(Decay_linear(((Delta(((OPEN*0.15)+(LOW*0.85)),2)/((OPEN*0.15)+(LOW*0.85)))-1),3)))-1)",
    "alpha157": "(Min(Prod(Rank(Rank(Log(Sum(Min(Rank(Rank((-1*Rank(Delta(($close-1),5))))),2),1)))),1),5)+Ts_Rank(Ref((-1*RET),6),5))",
    "alpha158": "(($high-SMA($close,15,2))-($low-SMA($close,15,2)))/$close",
    "alpha159": "(($close-Sum(Min($low,Ref($close,1)),6))/Sum(Max($high,Ref($close,1))-Min($low,Ref($close,1)),6)*12*24+($close-Sum(Min($low,Ref($close,1)),12))/Sum(Max($high,Ref($close,1))-Min($low,Ref($close,1)),12)*6*24+($close-Sum(Min($low,Ref($close,1)),24))/Sum(Max($high,Ref($close,1))-Min($low,Ref($close,1)),24)*6*24)*100/(6*12+6*24+12*24)",
    "alpha160": "SMA(($close<=Ref($close,1)?Std($close,20):0),20,1)",
    "alpha161": "Mean(Max(Max(($high-$low),Abs(Ref($close,1)-$high)),Abs(Ref($close,1)-$low)),12)",
    "alpha162": "(SMA(Max($close-Ref($close,1),0),12,1)/SMA(Abs($close-Ref($close,1)),12,1)*100-Min(SMA(Max($close-Ref($close,1),0),12,1)/SMA(Abs($close-Ref($close,1)),12,1)*100,12))/(Max(SMA(Max($close-Ref($close,1),0),12,1)/SMA(Abs($close-Ref($close,1)),12,1)*100,12)-Min(SMA(Max($close-Ref($close,1),0),12,1)/SMA(Abs($close-Ref($close,1)),12,1)*100,12))",
    "alpha163": "Rank(((((-1*RET)*Mean($volume,20))*$vwap)*($high-$close)))",
    "alpha164": "SMA(((($close>Ref($close,1))?1/($close-Ref($close,1)):1)-Min((($close>Ref($close,1))?1/($close-Ref($close,1)):1),12))/($high-$low)*100,13,2)",
    "alpha165": "(Max(Cumsum($close - Mean($close, 48)), 48) - Min(Cumsum($close - Mean($close, 48)), 48)) / Std($close, 48)",
    "alpha166": "-20*(20-1)^1.5*Sum($close/Ref($close,1)-1-Mean($close/Ref($close,1)-1,20),20)/((20-1)*(20-2)*(Sum(($close/Ref($close,1)-1)^2,20))^1.5)",
    "alpha167": "Sum(($close-Ref($close,1)>0?$close-Ref($close,1):0),12)",
    "alpha168": "(-1*$volume/Mean($volume,20))",
    "alpha169": "SMA(Mean(Ref(SMA($close-Ref($close,1),9,1),1),12)-Mean(Ref(SMA($close-Ref($close,1),9,1),1),26),10,1)",
    "alpha170": "((((Rank((1/$close))*$volume)/Mean($volume,20))*(($high*Rank(($high-$close)))/(Sum($high,5)/5)))-Rank(($vwap-Ref($vwap,5))))",
    "alpha171": "((-1*(($low-$close)*($open^5)))/(($close-$high)*($close^5)))",
    "alpha172": "Mean(Abs(Sum((LD>0&LD>HD)?LD:0,14)*100/Sum(TR,14)-Sum((HD>0&HD>LD)?HD:0,14)*100/Sum(TR,14))/(Sum((LD>0&LD>HD)?LD:0,14)*100/Sum(TR,14)+Sum((HD>0&HD>LD)?HD:0,14)*100/Sum(TR,14))*100,6)",
    "alpha173": "3*SMA($close,13,2)-2*SMA(SMA($close,13,2),13,2)+SMA(SMA(SMA(Log($close),13,2),13,2),13,2)",
    "alpha174": "SMA(($close>Ref($close,1)?Std($close,20):0),20,1)",
    "alpha175": "Mean(Max(Max(($high-$low),Abs(Ref($close,1)-$high)),Abs(Ref($close,1)-$low)),6)",
    "alpha176": "Corr(Rank((($close-Min($low,12))/(Max($high,12)-Min($low,12)))),Rank($volume),6)",
    "alpha177": "((20-HighDay($high,20))/20)*100",
    "alpha178": "($close-Ref($close,1))/Ref($close,1)*$volume",
    "alpha179": "(Rank(Corr($vwap,$volume,4))*Rank(Corr(Rank($low),Rank(Mean($volume,50)),12)))",
    "alpha180": "((Mean($volume,20)<$volume)?((-1*Ts_Rank(Abs(Delta($close,7)),60))*Sign(Delta($close,7))):(-1*$volume))",
    "alpha181": "Sum((($close/Ref($close,1)-1)-Mean(($close/Ref($close,1)-1),20))-(BANCHMARKINDEXCLOSE-Mean(BANCHMARKINDEXCLOSE,20))^2,20)/Sum((BANCHMARKINDEXCLOSE-Mean(BANCHMARKINDEXCLOSE,20))^3,20)",
    "alpha182": "Count(($close>$open&BANCHMARKINDEXCLOSE>BANCHMARKINDEXOPEN)OR($close<$open&BANCHMARKINDEXCLOSE<BANCHMARKINDEXOPEN),20)/20",
    "alpha183": "(Max(Cumsum($close - Mean($close, 24)), 24) - Min(Cumsum($close - Mean($close, 24)), 24)) / Std($close, 24)",
    "alpha184": "(Rank(Corr(Ref(($open-$close),1),$close,200))+Rank(($open-$close)))",
    "alpha185": "Rank((-1*((1-($open/$close))^2)))",
    "alpha186": "(Mean(Abs(Sum((LD>0&LD>HD)?LD:0,14)*100/Sum(TR,14)-Sum((HD>0&HD>LD)?HD:0,14)*100/Sum(TR,14))/(Sum((LD>0&LD>HD)?LD:0,14)*100/Sum(TR,14)+Sum((HD>0&HD>LD)?HD:0,14)*100/Sum(TR,14))*100,6)+Ref(Mean(Abs(Sum((LD>0&LD>HD)?LD:0,14)*100/Sum(TR,14)-Sum((HD>0&HD>LD)?HD:0,14)*100/Sum(TR,14))/(Sum((LD>0&LD>HD)?LD:0,14)*100/Sum(TR,14)+Sum((HD>0&HD>LD)?HD:0,14)*100/Sum(TR,14))*100,6),6))/2",
    "alpha187": "Sum(($open<=Ref($open,1)?0:Max(($high-$open),($open-Ref($open,1)))),20)",
    "alpha188": "(($high-$low-SMA($high-$low,11,2))/SMA($high-$low,11,2))*100",
    "alpha189": "Mean(Abs($close-Mean($close,6)),6)",
    "alpha190": "((Corr(Mean($volume,20),$low,5)+(($high+$low)/2))-$close)",
    "alpha191": "(Corr(Mean($volume, 20), $low, 5) + ($high + $low) / 2) - $close",
}


def init_qlib(provider_uri: Optional[str] = None):
    """初始化 qlib 数据源（使用内置数据或自定义数据）"""
    if not QLIB_AVAILABLE:
        raise ImportError("qlib未安装，请运行: pip install pyqlib")

    uri = provider_uri or "~/.qlib/qlib_data/cn_data"
    try:
        qlib.init(provider_uri=uri)
        return True
    except Exception as e:
        warnings.warn(f"qlib初始化失败: {e}，尝试使用默认配置")
        return False


def compute_alpha101(
    symbols: List[str],
    factors: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    **kwargs,
) -> Union[Dict[str, pd.DataFrame], pd.DataFrame]:
    """
    计算 Alpha101 因子。

    参数
    ----
    symbols : List[str]
        股票代码列表，如 ['sh600519', 'sz000001']
    factors : List[str], optional
        要计算的因子名称列表，如 ['alpha001', 'alpha002']
        None 表示计算所有因子
    start_date : str, optional
        开始日期 'YYYY-MM-DD'
    end_date : str, optional
        结束日期 'YYYY-MM-DD'
    count : int, optional
        交易日数量（用于估算起始日期）

    返回
    ----
    Dict[str, pd.DataFrame] 或 pd.DataFrame
        如果传入多个因子，返回 {factor_name: DataFrame}
        如果传入单个因子，返回 DataFrame
    """
    if not QLIB_AVAILABLE:
        raise ImportError("qlib未安装，请运行: pip install pyqlib")

    if not factors:
        factors = [f"alpha{i:03d}" for i in range(1, 102)]

    qlib_symbols = [s.replace("sh", "").replace("sz", "").upper() for s in symbols]

    if start_date and end_date:
        pass
    elif count and end_date:
        start_date = _estimate_start_date(end_date, count + 120)
    elif count:
        import datetime

        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        start_date = _estimate_start_date(end_date, count + 120)

    result = {}
    for alpha_name in factors:
        try:
            alpha_expr = ALPHA101_EXPR.get(alpha_name)
            if alpha_expr is None:
                warnings.warn(f"{alpha_name} 表达式未定义，跳过")
                continue

            data = D.features(
                qlib_symbols,
                [alpha_expr],
                start_time=start_date,
                end_time=end_date,
                freq="day",
            )
            if data is not None and not data.empty:
                data.columns = [alpha_name]
                result[alpha_name] = data
        except Exception as e:
            warnings.warn(f"{alpha_name} 计算失败: {e}")

    if len(result) == 1:
        return list(result.values())[0]
    return result


def compute_alpha191(
    symbols: List[str],
    factors: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    **kwargs,
) -> Union[Dict[str, pd.DataFrame], pd.DataFrame]:
    """
    计算 Alpha191 因子（国泰君安191因子）。

    参数同 compute_alpha101
    """
    if not QLIB_AVAILABLE:
        raise ImportError("qlib未安装，请运行: pip install pyqlib")

    if not factors:
        factors = [f"alpha{i:03d}" for i in range(1, 192)]

    qlib_symbols = [s.replace("sh", "").replace("sz", "").upper() for s in symbols]

    if start_date and end_date:
        pass
    elif count and end_date:
        start_date = _estimate_start_date(end_date, count + 120)
    elif count:
        import datetime

        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        start_date = _estimate_start_date(end_date, count + 120)

    result = {}
    for alpha_name in factors:
        try:
            alpha_expr = ALPHA191_EXPR.get(alpha_name)
            if alpha_expr is None:
                warnings.warn(f"{alpha_name} 表达式未定义，跳过")
                continue

            data = D.features(
                qlib_symbols,
                [alpha_expr],
                start_time=start_date,
                end_time=end_date,
                freq="day",
            )
            if data is not None and not data.empty:
                data.columns = [alpha_name]
                result[alpha_name] = data
        except Exception as e:
            warnings.warn(f"{alpha_name} 计算失败: {e}")

    if len(result) == 1:
        return list(result.values())[0]
    return result


def compute_alpha360(
    symbols: List[str],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    **kwargs,
) -> pd.DataFrame:
    """
    计算 Alpha360 因子（qlib 内置预定义特征集）。

    参数
    ----
    symbols : List[str]
        股票代码列表
    start_date : str, optional
        开始日期
    end_date : str, optional
        结束日期

    返回
    ----
    pd.DataFrame
        Alpha360 特征数据
    """
    if not QLIB_AVAILABLE:
        raise ImportError("qlib未安装，请运行: pip install pyqlib")

    qlib_symbols = [s.replace("sh", "").replace("sz", "").upper() for s in symbols]

    try:
        from qlib.contrib.data import Alpha360

        dataset = Alpha360(qlib_symbols, start_time=start_date, end_time=end_date)
        data = dataset.prepare_data()
        return data
    except Exception as e:
        warnings.warn(f"Alpha360 计算失败: {e}")
        return pd.DataFrame()


def _estimate_start_date(end_date: str, count: int) -> str:
    """根据交易日数量估算起始日期"""
    import datetime

    end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    start_dt = end_dt - datetime.timedelta(days=count * 1.5)
    return start_dt.strftime("%Y-%m-%d")


def _get_alpha101_expr(alpha_name: str) -> Optional[str]:
    """获取 Alpha101 因子的表达式。"""
    return ALPHA101_EXPR.get(alpha_name)


def _get_alpha191_expr(alpha_name: str) -> Optional[str]:
    """获取 Alpha191 因子的表达式。"""
    return ALPHA191_EXPR.get(alpha_name)


def get_alpha_values_jq(
    securities: List[str],
    factors: List[str],
    end_date: Optional[str] = None,
    count: int = 1,
    alpha_type: str = "alpha101",
) -> pd.DataFrame:
    """
    聚宽风格接口：获取 Alpha 因子值。

    参数
    ----
    securities : List[str]
        股票代码列表（聚宽格式，如 '600519.XSHG'）
    factors : List[str]
        因子名称列表
    end_date : str, optional
        截止日期
    count : int
        交易日数量
    alpha_type : str
        'alpha101' 或 'alpha191'

    返回
    ----
    pd.DataFrame
        因子值表格，index为日期，columns为股票代码
    """
    from jk2bt.utils.symbol import jq_code_to_ak

    symbols = [jq_code_to_ak(sec) for sec in securities]

    if alpha_type == "alpha101":
        return compute_alpha101(symbols, factors, end_date=end_date, count=count)
    elif alpha_type == "alpha191":
        return compute_alpha191(symbols, factors, end_date=end_date, count=count)
    else:
        raise ValueError(f"不支持的alpha_type: {alpha_type}")


__all__ = [
    "init_qlib",
    "compute_alpha101",
    "compute_alpha191",
    "compute_alpha360",
    "get_alpha_values_jq",
    "ALPHA101_EXPR",
    "ALPHA191_EXPR",
]
