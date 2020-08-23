import numpy as np
from PIL import Image
import time
from functools import reduce        # untuk faktor bilangan
#from matplotlib import pyplot as plt


#OBE
def r_ij(m, baris_i, baris_j, r):
    return m[baris_i] + r*m[baris_j]

def tukar(m, baris_i, baris_j):
    m[baris_i] = m[baris_i] + m[baris_j]
    m[baris_j] = m[baris_i] - m[baris_j]
    m[baris_i] = m[baris_i] - m[baris_j]
##########################

#barisan logistic map
def log(x0, banyak):
    x = x0
    for i in range(1000):
        x = 3.9 * x * (1 - x)     # 3.9 bisa diganti bil. pada [3.7, 4]
    
    barisan = np.zeros(banyak, dtype=np.uint8)
    for i in range(banyak):
        x = 3.9 * x * (1 - x)     # 3.9 bisa diganti bil. pada [3.7, 4]
        barisan[i] = x*1000%256
    return barisan
###########################

def kunci(n, x0):
    # matriks segitiga atas
    banyak = n * (n - 1)/2
    barisan = log(x0, banyak + n - 1)
    

    msa = np.eye(n)
    
    indeks = 0
    for i in range(n):
        for j in range(i+1,n):
            msa[i,j] = barisan[indeks]
            indeks += 1
    
    #print 'kunci sebaran logistik'
    #print msa
    #print '@'*30
    for baris_i in range(1,n):
        msa[baris_i] = r_ij(msa, baris_i, 0, barisan[indeks])%256
        indeks += 1
        #print msa
        #print '-'*10
    #print '='*20
    #print msa
    augmented = np.zeros((n,2*n))
    augmented[:,:n]=msa
    
    augmented[:,n:]=np.eye(n)
    
    #OBE untuk dapatkan invers
    # mengenolkan segitiga bawah
    for kolom in range(n):
        for baris in range(kolom+1,n):
            augmented[baris] = r_ij(augmented, baris, kolom, -augmented[baris, kolom])%256
    
    # mengenolkan segitiga atas
    for kolom in range(1,n):
        for baris in range(kolom):
            augmented[baris] = r_ij(augmented, baris, kolom, -augmented[baris, kolom])%256
    
    mbalik = augmented[:,n:]

    return msa, mbalik


def enkripsi(gb, ukuran, x0):
    print "="*50
    print "Encryption process begin."
    waktu_mulai = time.time()
    gbku = Image.open(gb)
    mgb = np.array(gbku)
    
    kunciku, balikku = kunci(ukuran, x0)
    #print 'kunciku'
    #print kunciku
    #print '#'*30
    mgb_reshape = mgb.reshape((ukuran, mgb.size/ukuran))
    
    m_kali = np.dot(kunciku, mgb_reshape)%256
    #print 'm_kali'
    #print m_kali
    #print '$'*50
    m_cipher = m_kali.reshape(mgb.shape).astype(np.uint8)
    #print 'm_cipher'
    #print m_cipher
    
    chiper = Image.fromarray(m_cipher)
    chiper.save('enkripsi.png')
    print "-----------------------------------------------------------------"
    print 'Your encrypted image is called "enkripsi.png" in the same folder.'
    print 'The encryption time is ', time.time() - waktu_mulai, ' seconds.'
    password2 = str(x0)
    pjgx0 = len(password2)
    password2 = password2[2:pjgx0 - 1]
    print 'Please remember your two-layer password:'
    print 'Password 1:', ukuran
    print 'Password 2:', password2
    print "-----------------------------------------------------------------"

def dekripsi(gb, ukuran, x0):
    print "Decryption process begin."
    waktu_mulai = time.time()
    gbku = Image.open(gb)
    mgb = np.array(gbku)
    
    kunciku, balikku = kunci(ukuran, x0)
    
    mgb_reshape = mgb.reshape((ukuran, mgb.size/ukuran))
    
    m_kali = np.dot(balikku, mgb_reshape)%256
    m_dechiper = m_kali.reshape(mgb.shape).astype(np.uint8)
    
    dechiper = Image.fromarray(m_dechiper)
    dechiper.save('dekripsi.png')
    print 'Your decrypted image is called "dekripsi.png" in the same folder.'
    print 'The decryption time is ', time.time() - waktu_mulai, ' seconds.'

def cek_sama(gb_asli, gb_dekripsi):
    gba = Image.open(gb_asli)
    gbd = Image.open(gb_dekripsi)
    
    mgba = np.array(gba)
    mgbd = np.array(gbd)
    
    if (mgba==mgbd).all():
        return "Kedua gambar sama"
    else:
        return "Kedua gambar beda"



def factors(n):    
    fkt = set(reduce(list.__add__, 
                ([i, n//i] for i in range(2, int(n**0.5) + 1) if n % i == 0)))
    fkt_list = sorted(fkt)
    return [ i for i in fkt_list if i < 1000 ] # ambil nilai yang kurang dari 1000

##########################################################



print "============================================================================"
print "Digital Image Encryption Algorithm Trough Unimodular Matrix and Logistic Map"
print "============================================================================"
jawaban = raw_input("Please select, you want to encrypt (e) or decrypt (d):")
if jawaban == "e" or jawaban == "E":
    print "-------------------------"
    print "You will encrypt an image"
    print "-------------------------"
    print
    gb = raw_input("Now, insert your image with its extension (example: image.png):")
    gbku = Image.open(gb)
    mgb = np.array(gbku)
    ukuran = mgb.size
    faktor = factors(ukuran)
    
    #print ukuran
    print
    print "----------------------------------------------------------------------------"
    print faktor
    print "----------------------------------------------------------------------------"
    
    password1 = input("Please choose one of the numbers in the set above as Password 1:")
    #print password1
    while password1 not in faktor:
        print "Your choice are ", password1
        print "Not in the given list."
        print "-"*50, "\nThe list of numbers are:"
        print faktor
        password1 = input("Please choose again the right one:")
    print "Your Password 1 is: ", password1, "\n"
    pw2 = raw_input("Enter Password 2 in the form of a number, maximum 14 digits (example: 22021985)\nPassword 2:")
    print "Your Password 2 is: ", pw2
    password2 = float("0." + pw2 + "1")

    #proses enkripsi dimulai
    enkripsi(gb, password1, password2)
else:
    print "*"*80
    print "Dekripsi Gambar digital dengan memanfaatkan matriks unimodular dan fungsi chaos logistic map"
    print "-"*50
    print

    gb = raw_input("Now, insert your encrypted image with its extension (example: image.png):")
    gbku = Image.open(gb)
    mgb = np.array(gbku)
    ukuran = mgb.size
    faktor = sorted(factors(ukuran))

    #print ukuran
    print "----------------------------------------------------------------------------"
    print faktor
    print "----------------------------------------------------------------------------"
    
    password1 = input("Please choose one of the numbers in the set above as Password 1:")
    #print password1
    while password1 not in faktor:
        print "Your choice are ", password1
        print "Not in the given list."
        print "-"*50, "\nThe list of numbers are:"
        print faktor
        password1 = input("Please choose again the right one:")
    print "Your Password 1 is: ", password1, "\n"
    pw2 = raw_input("Enter Password 2 in the form of a number, maximum 14 digits (example: 22021985)\nPassword 2:")
    print "Your Password 2 is: ", pw2
    password2 = float("0." + pw2 + "1")

    #proses dekripsi dimulai
    dekripsi(gb, password1, password2)


