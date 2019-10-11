from datetime import datetime, timedelta


def donationCounter():
    """
    Generator of donationCount
    :return:
    """
    donationCount = 0
    while True:
        yield f'{donationCount:03}'
        donationCount += 1

class Donation:
    def __init__(self):
        self._donor = None
        self._din = str()
        self._donationDate = str()
        self._donationSite = str()
        self.products = []
        self.donationCounterGen = donationCounter();


    def createDonation(self, donor, dinPrefix, donationDate, donationSite):
        self._donor = donor
        #donationDate = datetime.now().strftime()   strftime('%Y%02m0%2d', donationDate)
        self._din = f'{dinPrefix[0]}{donationDate}{next(self.donationCounterGen)}'
        self._donationDate = donationDate
        self._donationSite = donationSite

    def getExpireDate(self, daysToExpire):
        donationDate = datetime.strptime(self._donationDate, '%m %b %Y')
        return donationDate + timedelta(float(daysToExpire))


    def reprJSON(self):
        dictionary =self.donor
        return dict()