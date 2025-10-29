# 10 bit encoder test
# hamming code 能驗證輸入是否正確及最多糾正1位元的錯誤.
import math


class Encoder:
    def __init__(self, input: str):
        self.data = list(map(int, input))
        # self.data = [0, 1, 0, 0, 0, 0, 1, 1, 0, 1]

    # 計算所需的hamming code 長度
    def cal_syndrom_width(self) -> int:
        for i in range(len(self.data)):
            if 2**i >= len(self.data) + 1 + i:
                return i

    # 產生hamming code糾錯碼

    def encoder(self) -> str:
        syndrom_width = self.cal_syndrom_width()

        for i in range(syndrom_width):
            self.data.insert(2**i - 1, f"h{i+1}")
        # self.data = ['h1', 'h2', 0, 'h3', 1, 0, 0, 'h4', 0, 0, 1, 1, 0, 1]

        correcting_bits = 0
        for i in range(len(self.data)):
            if self.data[i] == 1:
                correcting_bits ^= i + 1
        # correcting_bits = 0b1100

        # 增加偶同位元(even Parity bit)
        tmp = correcting_bits
        parity_bit = 0
        while tmp:
            parity_bit ^= tmp & 1
            tmp >>= 1
        correcting_bits = (correcting_bits << 1) + parity_bit
        # correcting_bits = 0b11000

        return "{:b}".format(correcting_bits).zfill(syndrom_width + 1)


class Decoder:
    def __init__(self, input: str, correcting_bits: str):
        self.data = list(map(int, input))
        self.corr_bits = list(map(int, correcting_bits))

    def is_correcting_bits_correct(self, corr_bits):
        corr_bits = int("".join(map(str, corr_bits)), 2)
        tmp = corr_bits & 1
        corr_bits >>= 1
        while corr_bits:
            tmp ^= corr_bits & 1
            corr_bits >>= 1

        return False if tmp else True

    def decoder(self):
        data = self.data[:]
        # check correcting_bits 是否錯誤
        if not self.is_correcting_bits_correct(self.corr_bits):
            print("糾錯碼於傳輸時損壞, 請重新傳送.")
            return
        else:
            print("糾錯碼沒錯, 開始檢查資料是否正確...")
            del self.corr_bits[-1]

        corr_bits = self.corr_bits[:]
        # corr_bits = 0b1100
        idx = 1
        while corr_bits:
            data.insert(idx - 1, corr_bits[-1])
            del corr_bits[-1]
            idx <<= 1

        # 檢查資料是否正確
        err_idx = 0
        for i in range(len(data)):
            if data[i] == 1:
                err_idx ^= i + 1

        if err_idx != 0:
            i = 0
            while 2**i < err_idx:
                i += 1
            err_idx -= i

            self.data[err_idx - 1] ^= 1

            print(f"資料不正確, 錯誤位置為: {err_idx}(從1開始數)")
        else:
            print("資料正確")
        return "".join(map(str, self.data))


input = "0100001101"

a = Encoder(input)
syndrome_bits = a.encoder()
print(f"Hamming code + Even parity bit所產生的糾錯碼 = {syndrome_bits}")

print("")

input = "0100001100"
b = Decoder(input, syndrome_bits)
correct_data = b.decoder()
print(f"解碼後所得的資料 = {correct_data}")
