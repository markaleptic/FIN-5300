import datetime

class BondPricer():
    def __init__(self, name, lstCoupDt, settleDt, nxtCoupDt, n, rate, yld, face, periodicity):
        self.name           = name
        self.lastCouponDate = lstCoupDt
        self.settlementDate = settleDt
        self.nextCouponDate = nxtCoupDt
        self.periods        = n
        self.faceValue      = face
        self.coupon         = ((rate / 100) / periodicity) * face
        self.ytm            = (yld / 100)  / periodicity
        self.frequency      = periodicity
        self.remDays        = 0.00
        self.totalDays      = 0.00
        self.fracPeriod     = 0.00
        self.fullPrice      = 0.00
        self.accruedInt     = 0.00
        self.flatPrice      = 0.00

    # Component A - Fractional Period
    def setFracPeriod(self):
        self.remDays    = self.nextCouponDate - self.settlementDate
        self.totalDays  = self.nextCouponDate - self.lastCouponDate
        self.fracPeriod = self.remDays / self.totalDays
    
    # Component B - Present Value Loop
    def setPV(self):
        for i in range(0, self.periods):
            if i == self.periods - 1:
                lastCoupon = self.coupon + self.faceValue
                self.fullPrice += lastCoupon / ((1 + self.ytm) ** (i + self.fracPeriod))
            else:
                self.fullPrice += self.coupon / ((1 + self.ytm) ** (i + self.fracPeriod))

    # Component C - Bond Pricer
    def setPrice(self):
        self.accruedInt = (1 - self.fracPeriod) * self.coupon
        self.flatPrice  = self.fullPrice - self.accruedInt

    def printPretty(self):
        print('Price of %s on %s' % (self.name, self.settlementDate))
        print('Flat Price:'.ljust(20),'$','{:,.2f}'.format(self.flatPrice).rjust(10))
        print('Accrued Interest:'.ljust(20),'$','{:,.2f}'.format(self.accruedInt).rjust(12))
        print('Full Price:'.ljust(20),'$','{:,.2f}'.format(self.fullPrice).rjust(10))
        print('\n')

def main():
    # Treasury Bond from Problem Set 1
    name        = '10-Year Treasury Bond'
    lstCoupDt   = datetime.date(2017, 8, 15)
    settleDt    = datetime.date(2017, 9, 13)
    nxtCoupDt   = datetime.date(2018, 2, 15)
    periods     = 20
    coupon      = 2.25
    ytm         = 2.15849343654757
    faceValue   = 1000000.00
    periodicity = 2

    treasuryBond = BondPricer(name, lstCoupDt, settleDt, nxtCoupDt, periods, coupon, ytm, faceValue, periodicity)
    treasuryBond.setFracPeriod()
    treasuryBond.setPV()
    treasuryBond.setPrice()
    treasuryBond.printPretty()

    # Should yield
    # Flat Price    $1,008,125.00
    # Accrued       $    1,773.10
    # Full Price    $1,009,898.10


    # Corporate Bond from Problem Set 1
    name        = '10-Year AAPL Bond'
    lstCoupDt   = datetime.date(2016, 9, 17)
    settleDt    = datetime.date(2017, 9, 14)
    nxtCoupDt   = datetime.date(2017, 9, 17)
    periods     = 11
    coupon      = 2.00
    ytm         = 1.0339656
    faceValue   = 1000000.00
    periodicity = 1

    aaplBond = BondPricer(name, lstCoupDt, settleDt, nxtCoupDt, periods, coupon, ytm, faceValue, periodicity)
    aaplBond.setFracPeriod()
    aaplBond.setPV()
    aaplBond.setPrice()
    aaplBond.printPretty()

    # Should yield
    # Flat Price    $1,091,400.00
    # Accrued       $   19,835.62
    # Full Price    $1,111,235.62


main()
