# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 01:03:13 2022

@author: Ahnaf Sabilah Arif
"""

import streamlit as st
import pandas as pd

def main():
    st.write("##### Website ini dibuat untuk memenuhi tugas mata kuliah Komputasi Astronomi. Kode program yang telah dibuat dapat dilihat [disini](https://github.com/Ahnafsa01/Komputasi-Astronomi)")
    
    with st.expander("Perhitungan waktu sholat"):
        st.write("""
                 Dalam membuat program perhitungan waktu sholat, referensi yang saya gunakan adalah buku 
                 [*Mekanika Benda Langit*](https://github.com/Ahnafsa01/Komputasi-Astronomi/tree/main/Referensi) oleh Rinto Anugraha.
                 """)
    
    with st.expander("Database"):
        st.write("Database dibuat dengan menggunakan file excel, berikut merupakan database yang digunakan.")
        df = pd.read_excel("database.xlsx")
        st.dataframe(df)
        st.write(
              """     
          - Lintang, bujur, dan zona(UTC) didapatkan melalui google maps atau wikipedia lokasi yang digunakan.
          - Ketinggian kota didapatkan melalui data ketinggian wilayah berdasarkan badan pusat statistik. 
          - Timezone didapatkan melalui koordinat dari lokasi yang digunakan, ini akan digunakan untuk mengoreksi waktu universal menjadi waktu lokal di lokasi yang dipilih.
          - Ekstrim merupakan kolom yang digunakan untuk membedakan lokasi yang akan mengalami error saat dilakukan perhitungan waktu sholat.
           """
        )
        st.markdown("")
        st.write(
              """     
          \n Dalam mengakses database, saya menggunakan library pandas. Dengan memanfaatkan fungsi *loc* atau *iloc*.
           """
        )
    
    with st.expander("Zona ekstrim"):
        st.write("""
                 *Zona Ekstrim* merupakan sebutan untuk lokasi yang ketika dilakukan perhitungan waktu sholat, 
                 maka akan menimbulkan error pada perhitungan. Error ini dapat terjadi karena pada kenyataannya di lokasi
                 tersebut waktu siang berlansung lebih lama atau bahkan tidak ada waktu malam(keadaan benar-benar gelap).
                 Sedangkan pada program yang dibuat, jika menggunakan referensi yang sama seperti yang saya gunakana, maka
                 error ini terjadi karena nilai *ACOS* yang melewati range. Kita ketahui bahwa dalam trigonometri 
                 rangenya berkisar antara (-1 hingga 1). Pada zona ekstrim, nilai *ACOS* ini akan melewati rangenya sehingga 
                 terjadi error. Strategi untuk mengatasi ini dapat dilakukan 3 pilihan yaitu,
                 - Mengambil waktu terakhir yang masih dapat dihitung(tepat sebelum terjadi error)
                 - Menggunakan interpolasi antara dua waktu sholat yang. Waktu pertama adalah pada saat sebelum terjadi error dan waktu kedua adalah pada saat setelah terjadi error, lalu kita lakukan interpolasi untuk mendapatkan waktu sholat diantara dua waktu tersebut.
                 - Menggunakan waktu sholat lokasi lain (waktu sholatnya masih dapat dihitung) yang paling dekat dengan lokasi dimana waktu sholatnya error.   
                 """)
        st.markdown("")
        st.write(
              """     
          \n Dalam program ini saya menggunakan pilihan pertama untuk mengatasi error yang terjadi pada perhitungan waktu sholat.
           """
        )
