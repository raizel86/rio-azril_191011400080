
def turun(z, zmin, zmak):
    return (zmak-z)/(zmak-zmin)

def naik(z, zmin, zmak):
    return(z-zmin)/(zmak-zmin)

class Permintaan():
    minimal = 2049
    maksimal = 7493
    median = 4861

    def down(self, z):
        if z >= self.median:
            return 0
        elif z <= self.minimal:
            return 1
        else :
            return turun(z, self.minimal, self.median)
    
    def up(self, z):
        if z >= self.maksimal:
            return 1
        elif z <= self.median:
            return 0
        else :
            return naik(z, self.median  , self.maksimal)
    
    def consistent(self, z):
        if z >= self.maksimal or z <= self.minimal:
            return 0
        elif self.minimal < z < self.median:
            return naik(z, self.minimal, self.median)
        elif self.median < z < self.maksimal:
            return turun (z, self.median, self.maksimal)
        else :
            return 1

class Persediaan():
    minimal = 550
    maksimal = 1285

    def sedikit(self, z):
        if z >= self.maksimal:
            return 0
        elif z <= self.minimal:
            return 1
        else :
            return turun(z, self.minimal, self.maksimal)
    
    def banyak(self, z):
        if z >= self.maksimal:
            return 1
        elif z <= self.minimal:
            return 0
        else :
            return naik(z, self.minimal, self.maksimal)

class Produksi():
    minimal = 3719
    maksimal = 6769
    permintaan = 0
    persediaan = 0

    def _kurang(self, s):
        return self.maksimal - s*(self.maksimal - self.minimal)

    def _tambah(self, s):
        return s*(self.maksimal - self.minimal) + self.minimal

    def _inferensi(self, pmt=Permintaan(), psd=Persediaan()):
        result = []
        #1
        q1 = min(pmt.down(self.permintaan), psd.banyak(self.persediaan))
        w1 = self._kurang(q1)
        result.append((q1, w1))
        #2
        q2 = min(pmt.down(self.permintaan), psd.sedikit(self.persediaan))
        w2 = self._kurang(q2)
        result.append((q2, w2))
        #3
        q3 = min(pmt.up(self.permintaan), psd.banyak(self.persediaan))
        w3 = self._tambah(q3)
        result.append((q3, w3))
        #4
        q4 = min(pmt.up(self.permintaan), psd.sedikit(self.persediaan))
        w4 = self._kurang(q4)
        result.append((q4, w4))
        #5
        q5 = min(pmt.consistent(self.permintaan), psd.sedikit(self.persediaan))
        w5 = self._tambah(q5)
        result.append((q5, w5))
        #6
        q6 = min(pmt.consistent(self.permintaan), psd.sedikit(self.persediaan))
        w6 = self._kurang(q6)
        result.append((q6, w6))
        return result

    def defuzifikasi(self, data_inferensi=[]):
        data_inferensi = data_inferensi if data_inferensi else self._inferensi()
        res_q_w = 0
        res_q = 0
        for data in data_inferensi:
            res_q_w += data[0] * data[1]
            res_q += data[0]
        return res_q_w/res_q


