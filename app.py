import streamlit as st
from streamlit_option_menu import option_menu
import hijri_converter.convert
import pandas as pd
import datetime
import calendar
from sympy import * 
from math import *
import pytz
import about
import koreksi_tanggal

st.set_page_config(layout = 'wide', initial_sidebar_state = 'collapsed', page_title = 'UtkawSholat')

with st.sidebar:
  choose = option_menu(
    menu_title = "Main Menu", 
    options = ["Home","About"], 
    icons = ['house','info-circle'], 
    menu_icon = "cast"
    )

if choose == "Home":
  st.title("WAKTU SHOLAT")

  st.write("ℹ️ - Reminder")
  st.write(
        """     
    Sesungguhnya yang pertama kali dihisab (dihitung) dari amalan seorang hamba pada hari kiamat adalah sholat. Apabila sholatnya baik, dia akan mendapatkan keberuntungan dan keselamatan. Apabila sholatnya rusak, dia akan menyesal dan merugi.
    \n[HR. at-Tirmidzi, An-Nasa'i, Al-Baihaqi] 
     """
  )
  st.markdown("")

  df = pd.read_excel("database.xlsx")
  kota_df = df["Lokasi"]
  lokasi = st.selectbox("Pilih lokasi Anda..",kota_df,21)
  wilayah = lokasi.split(",") 

  col1,col2 = st.columns([3,1])
  listTabs = ["#Masehi","#Hijriyah"]
  whitespace = 33  
  db = df.set_index("Lokasi")
  lin = db.loc[lokasi,"L"]
  buj = db.loc[lokasi,"B"]
  zone = db.loc[lokasi,"Z"]
  H = db.loc[lokasi,"H"]
  timezone = db.loc[lokasi, "timezone"]
  ekstrim = db.loc[lokasi,"ekstrim"]

  with col1:
    tabs_masehi,tabs_hijriyah = st.tabs([s.center(whitespace,"\u2001") for s in listTabs])
    with tabs_masehi:
      value = datetime.date.today()
      h = 1
      with st.expander('Pilih tanggal Anda..'):
        this_year = value.year
        this_month = value.month
        t = st.selectbox('', range(this_year + 10, this_year - 10, -1,), index = range(this_year + 10, this_year - 10, -1,).index(this_year),\
        label_visibility = 'collapsed')
        month_masehi_name = calendar.month_name[1:]
        report_month_str = st.radio('', month_masehi_name, index=calendar.month_name[1:].index(calendar.month_name[this_month]), horizontal=True,\
        label_visibility = 'collapsed')
        b = month_masehi_name.index(report_month_str) + 1
      ta = int(repr(t)[-2:])

      # index 30 hari
      dt = datetime.datetime.strptime(f"{h}/{b}/{ta}", "%d/%m/%y")
      form_hari = dt.strftime("%d %b %Y") 
      cal= calendar.Calendar()
      daf_hari = []
      for x in cal.itermonthdays2(t, b):
        if x[0] == 0:
          pass
        else:
          if x[1] == 0:
            daf_hari.append(f'{x[0]:>02d} Sen')
          elif x[1] == 1:
            daf_hari.append(f'{x[0]:>02d} Sel')
          elif x[1] == 2:
            daf_hari.append(f'{x[0]:>02d} Rab')
          elif x[1] == 3:
            daf_hari.append(f'{x[0]:>02d} Kam')
          elif x[1] == 4:
            daf_hari.append(f'{x[0]:>02d} Jum')
          elif x[1] == 5:
            daf_hari.append(f'{x[0]:>02d} Sab')
          else:
            daf_hari.append(f'{x[0]:>02d} Min')

      # display the calendar
      a = calendar.month(t, b).split()
      c = []
      for i in range(9,len(a)):
        c.append(a[i])
      tanggal = list(map(int, c))

      # menghitung jd lokal untuk 1 bulan
      d = []
      for i in tanggal:
        def cek_bulan(b,t):
          if b == 1 or b == 2:
            b = b + 12
            t = t - 1
          else:
            b = b
            t = t
          return b,t

        if t < 0:
          b1,t1 = cek_bulan(b,t)
          A = 0
          B = 0
        else:
          date_1 = datetime.date(t,b,i)
          date_2 = datetime.date(1582,10,4)
          b1,t1 = cek_bulan(b,t)
          if date_1 <= date_2:
            A = 0
            B = 0
          else:
            A = int(t1/100)
            B = 2+int(A/4)-A

        JD = int(365.25*(t1+4716))+int(30.6001*(b1+1))+i+B-1524.5
        jdlokal = JD - zone/24
        d.append(jdlokal)

      # menghitung waktu sholat untuk 1 bulan
      S = []
      TM = []
      D = []
      A = []
      M = []
      I = []
      for i in d:
        #sudut tanggal
        T = 2*pi*(i-2451545)/365.25

        #sudut deklinasi matahari
        delta = degrees(radians(0.37877) + radians(23.264) * sin(radians(57.297*T -79.547)) + radians(0.3812) \
          * sin(radians(2*57.297*T-82.682)) + radians(0.17132) * sin(radians(3*57.297*T-59.722)))

        #bujur rata2 matahari
        def L0(bujur_rata2_matahari):
          while not 0 <= bujur_rata2_matahari <= 360 :
            bujur_rata2_matahari -= 360
          return bujur_rata2_matahari 

        U = (i - 2451545)/36525
        bujur_rata2_matahari = 280.46607 + 36000.7698*U
        L0 = L0(bujur_rata2_matahari)

        #equation of time
        ET = (int(degrees(-radians(1789 + 237 * U) * sin(radians(L0)) - radians(7146 - 62 * U) * cos(radians(L0)) +\
                    radians(9934 - 14 * U) * sin(radians(2 * L0)) - radians(29 + 5 * U) * cos(radians(2 * L0)) + radians(74 + 10*U) *\
                    sin(radians(3 * L0)) + radians(320 - 4 * U) * cos(radians(3 * L0)) - radians(212) * sin(radians(4 * L0)))) + 1) / 1000

        #waktu transit
        waktu_transit = 12 + zone - buj/15 - ET/60

        def convert(waktu_desimal):
          jam = int(waktu_desimal)
          sisa_jam = waktu_desimal - jam
          menit = int(sisa_jam * 60)
          sisa_menit = sisa_jam * 60 - menit
          detik = 60 * sisa_menit
          if detik < 30:
            menit = menit
          else:
            menit = menit + 1

          if menit == 60:
            jam = jam + 1
            menit = 60%60

          if jam >= 24:
            jam = jam%24
          return jam,menit

        def HA(alt):
          hour_angle = degrees(acos((sin(radians(alt)) - sin(radians(lin)) * sin(radians(delta))) / (cos(radians(lin)) * cos(radians(delta)))))
          return hour_angle

        #Waktu Subuh
        def subuh():
          try:
            alt = -20
            waktu_subuh = waktu_transit - HA(alt) / 15
          except:
            waktu_subuh = 0
            j,m = convert(waktu_subuh)
          else:
            j,m = convert(waktu_subuh)
          return j,m

        #Waktu Terbit Matahari
        def terbit_matahari():
          try:
            alt = -0.8333 - 0.0347 * sqrt(H)
            waktu_terbit_matahari = waktu_transit - HA(alt) / 15
          except:
            waktu_terbit_matahari = 0
            j,m = convert(waktu_terbit_matahari)
          else:
            j,m = convert(waktu_terbit_matahari)
          return j,m

        #Waktu Dzuhur
        def dzuhur():
          j,m = convert(waktu_transit)
          return j,m

        #Waktu Ashar
        def ashar():
          ka = 1
          alt = degrees(acot(ka + tan(radians(abs(delta - lin)))))
          waktu_ashar = waktu_transit + HA(alt) / 15
          j,m = convert(waktu_ashar)
          return j,m

        #Waktu Maghrib
        def maghrib():
          try:
            alt = -0.8333 - 0.0347 * sqrt(H)
            waktu_maghrib = waktu_transit + HA(alt) / 15
          except:
            waktu_maghrib = 0
            j,m = convert(waktu_maghrib)
          else:
            j,m = convert(waktu_maghrib)
          return j,m

        #Waktu Isya'
        def isya():
          try:
            alt = -18
            waktu_isya = waktu_transit + HA(alt) / 15
          except:
            waktu_isya = 0
            j,m = convert(waktu_isya)
          else:
            j,m = convert(waktu_isya)
          return j,m

        js,ms = subuh()
        jt,mt = terbit_matahari()
        jd,md = dzuhur()
        ja,ma = ashar()
        jm,mm = maghrib()
        ji,mi = isya()

        S.append(f'{js:0>2d}:{ms:0>2d}')
        TM.append(f'{jt:0>2d}:{mt:0>2d}')
        D.append(f'{jd:0>2d}:{md:0>2d}')
        A.append(f'{ja:0>2d}:{ma:0>2d}')
        M.append(f'{jm:0>2d}:{mm:0>2d}')
        I.append(f'{ji:0>2d}:{mi:0>2d}')

      sholat = {f'{dt.strftime("%B")}':daf_hari,
                  'Subuh':S,
                  'Terbit':TM,
                  'Dzuhur':D,
                  'Ashar':A,
                  'Maghrib':M,
                  'Isya':I
                  }
      df = pd.DataFrame(sholat).set_index(f'{dt.strftime("%B")}')
      st.subheader(f' Jadwal Sholat {wilayah[0]} Bulan {dt.strftime("%B %Y")}')
      
      if ekstrim == False:
          st.table(df)
      else:
          korektor_subuhM ,korektor_terbitM ,korektor_maghribM ,korektor_isyaM = koreksi_tanggal.masehi(t,lin,buj,zone,H)
          df.loc[df['Subuh'] == '00:00', 'Subuh'] = korektor_subuhM
          df.loc[df['Terbit'] == '00:00', 'Terbit'] = korektor_terbitM
          df.loc[df['Maghrib'] == '00:00', 'Maghrib'] = korektor_maghribM
          df.loc[df['Isya'] == '00:00', 'Isya'] = korektor_isyaM
          st.table(df)
              
    with tabs_hijriyah:
      hijri_now = hijri_converter.Hijri.today()
      with st.expander('Pilih tanggal Anda..'):
        this_year = hijri_now.year
        this_month = hijri_now.month
        t = st.selectbox('', range(this_year + 10, this_year - 10, -1,), index = range(this_year + 10, this_year - 10, -1,).index(this_year),\
        label_visibility = 'collapsed')
        month_hijri_names = hijri_converter.locales.EnglishLocale.month_names
        report_month_str = st.radio('', month_hijri_names, index = month_hijri_names.index(month_hijri_names[this_month-1]), horizontal=True,\
        label_visibility = 'collapsed', key = 3)
        b = month_hijri_names.index(report_month_str) + 1
        hari_bulan = hijri_converter.Hijri(t,b,1)
        total_hari_hijriyah = hari_bulan.month_length()

      c = []
      for i in range(1, total_hari_hijriyah + 1):
        gregorian = hijri_converter.Hijri(t,b,i).to_gregorian()
        #tanggal = gregorian.strptime(gregorian,)
        masehi = gregorian.strftime('%d %b %Y')
        c.append(f'{i:0>2d} ({masehi})')

      list_jd_hijriyah = []
      for i in range(1, total_hari_hijriyah + 1):
        #tahun yang sudah dilewati
        t1 = int((t - 1)/30)
        ts = ((t - 1)%30)

        if ts<2:
          k = 0
        elif 2<=ts<5:
          k = 1
        elif 5<=ts<7:
          k = 2
        elif 7<=ts<10:
          k = 3
        elif 10<=ts<13:
          k = 4
        elif 13<=ts<16:
          k = 5
        elif 16<=ts<18:
          k = 6
        elif 18<=ts<21:
          k = 7
        elif 21<=ts<24:
          k = 8
        elif 24<=ts<26:
          k = 9
        elif 26<=ts<29:
          k = 10
        else:
          k = 11

        #jumlah hari yang sudah dilewati
        hariDilewati = (t1*((354*30) + 11)) + ((ts*354) + k)

        #jumlah hari dalam tahun yang berjalan
        list_hariBerjalan = [0,30,59,89,118,148,177,207,236,266,295,325,354]
        b1 = b - 1

        for berjalan,hari in enumerate(list_hariBerjalan):
          if berjalan == b1:
            hariBerjalan = hari

        hariTahunIni = hariBerjalan + i
        #hijriah ke julian day
        JD = 1948438.5 + hariDilewati + hariTahunIni
        jdlokal = JD - zone/24
        list_jd_hijriyah.append(jdlokal)

      S = []
      TM = []
      D = []
      A = []
      M = []
      I = []
      for jd in list_jd_hijriyah:
        #sudut tanggal
        T = 2*pi*(jd-2451545)/365.25

        #sudut deklinasi matahari
        delta = degrees(radians(0.37877) + radians(23.264) * sin(radians(57.297*T -79.547)) + radians(0.3812) \
              * sin(radians(2*57.297*T-82.682)) + radians(0.17132) * sin(radians(3*57.297*T-59.722)))

        #bujur rata2 matahari
        def L0(bujur_rata2_matahari):
          while not 0 <= bujur_rata2_matahari <= 360 :
            bujur_rata2_matahari -= 360
          return bujur_rata2_matahari 

        U = (jd - 2451545)/36525
        bujur_rata2_matahari = 280.46607 + 36000.7698*U
        L0 = L0(bujur_rata2_matahari)

        #equation of time
        ET = (int(degrees(-radians(1789 + 237 * U) * sin(radians(L0)) - radians(7146 - 62 * U) * cos(radians(L0)) +\
                        radians(9934 - 14 * U) * sin(radians(2 * L0)) - radians(29 + 5 * U) * cos(radians(2 * L0)) + radians(74 + 10*U) *\
                        sin(radians(3 * L0)) + radians(320 - 4 * U) * cos(radians(3 * L0)) - radians(212) * sin(radians(4 * L0)))) + 1) / 1000

        #waktu transit
        waktu_transit = 12 + zone - buj/15 - ET/60


        def convert(waktu_desimal):
          jam = int(waktu_desimal)
          sisa_jam = waktu_desimal - jam
          menit = int(sisa_jam * 60)
          sisa_menit = sisa_jam * 60 - menit
          detik = 60 * sisa_menit
          if detik < 30:
            menit = menit
          else:
            menit = menit + 1

          if menit == 60:
            jam = jam + 1
            menit = 60%60

          if jam >= 24:
            jam = jam%24
          return jam,menit

        def HA(alt):
          hour_angle = degrees(acos((sin(radians(alt)) - sin(radians(lin)) * sin(radians(delta))) / (cos(radians(lin)) * cos(radians(delta)))))
          return hour_angle

        #Waktu Subuh
        def subuh():
          try:
            alt = -20
            waktu_subuh = waktu_transit - HA(alt) / 15
          except:
            waktu_subuh = 0
            j,m = convert(waktu_subuh)
          else:
            j,m = convert(waktu_subuh)
          return j,m

        #Waktu Terbit Matahari
        def terbit_matahari():
          try:
            alt = -0.8333 - 0.0347 * sqrt(H)
            waktu_terbit_matahari = waktu_transit - HA(alt) / 15
          except:
            waktu_terbit_matahari = 0
            j,m = convert(waktu_terbit_matahari)
          else:
            j,m = convert(waktu_terbit_matahari)
          return j,m

        #Waktu Dzuhur
        def dzuhur():
          j,m = convert(waktu_transit)
          return j,m

        #Waktu Ashar
        def ashar():
          ka = 1
          alt = degrees(acot(ka + tan(radians(abs(delta - lin)))))
          waktu_ashar = waktu_transit + HA(alt) / 15
          j,m = convert(waktu_ashar)
          return j,m

        #Waktu Maghrib
        def maghrib():
          try:
            alt = -0.8333 - 0.0347 * sqrt(H)
            waktu_maghrib = waktu_transit + HA(alt) / 15
          except:
            waktu_maghrib = 0 
            j,m = convert(waktu_maghrib)
          else:
            j,m = convert(waktu_maghrib)
          return j,m

        #Waktu Isya'
        def isya():
          try:
            alt = -18
            waktu_isya = waktu_transit + HA(alt) / 15
          except:
            waktu_isya = 0
            j,m = convert(waktu_isya)
          else:
            j,m = convert(waktu_isya)
          return j,m

        js,ms = subuh()
        jt,mt = terbit_matahari()
        jd,md = dzuhur()
        ja,ma = ashar()
        jm,mm = maghrib()
        ji,mi = isya()

        S.append(f'{js:0>2d}:{ms:0>2d}')
        TM.append(f'{jt:0>2d}:{mt:0>2d}')
        D.append(f'{jd:0>2d}:{md:0>2d}')
        A.append(f'{ja:0>2d}:{ma:0>2d}')
        M.append(f'{jm:0>2d}:{mm:0>2d}')
        I.append(f'{ji:0>2d}:{mi:0>2d}')  

      sholat_hijriyah = {
          f'{hijri_now.month_name()}':c,
          'Subuh'  : S,
          'Terbit' : TM,
          'Dzuhur' : D,
          'Ashar'  : A,
          'Maghrib': M,
          'Isya'   : I
      }
      df = pd.DataFrame(sholat_hijriyah).set_index(f'{hijri_now.month_name()}')
      st.subheader(f' Jadwal Sholat {wilayah[0]} Bulan {report_month_str} {t}')
      if ekstrim ==  False:
          st.table(df)
      else:
          if b < 3:
              #korektor_subuh,korektor_terbit,korektor_maghrib,korektor_isya = koreksi_tanggal.masehi(t,lin,buj,zone,H)
              df.loc[df['Subuh'] == '00:00', 'Subuh'] = korektor_subuhM
              df.loc[df['Terbit'] == '00:00', 'Terbit'] = korektor_terbitM
              df.loc[df['Maghrib'] == '00:00', 'Maghrib'] = korektor_maghribM
              df.loc[df['Isya'] == '00:00', 'Isya'] = korektor_isyaM
              st.table(df)
          else:
              korektor_subuhH ,korektor_terbitH ,korektor_maghribH ,korektor_isyaH = koreksi_tanggal.hijriyah(t,lin,buj,zone,H)
              df.loc[df['Subuh'] == '00:00', 'Subuh'] = korektor_subuhH
              df.loc[df['Terbit'] == '00:00', 'Terbit'] = korektor_terbitH
              df.loc[df['Maghrib'] == '00:00', 'Maghrib'] = korektor_maghribH
              df.loc[df['Isya'] == '00:00', 'Isya'] = korektor_isyaH
              st.table(df)
  
  with col2:
    zona_waktu = pytz.timezone(timezone)
    waktu_lokal = datetime.datetime.now(zona_waktu)
    h = waktu_lokal.day
    b = waktu_lokal.month
    t = waktu_lokal.year
    hijri_now = hijriyah = hijri_converter.Gregorian(t,b,h).to_hijri()
    hh = hijri_now.day
    bh = hijri_now.month_name()
    th = hijri_now.year

    ta = int(repr(t)[-2:])
    dt = datetime.datetime.strptime(f"{h}/{b}/{ta}", "%d/%m/%y")
    form_hari = dt.strftime("%d %b %Y") 

    #cek nama hari
    day_name = calendar.weekday(t,b,h)
    if day_name == 0:
      nama_hari = 'Sen'
    elif day_name == 1:
      nama_hari = 'Sel'
    elif day_name == 2:
      nama_hari = 'Rab'
    elif day_name == 3:
      nama_hari = 'Kam'
    elif day_name == 4:
      nama_hari = 'Jum'
    elif day_name == 5:
      nama_hari = 'Sab'
    else:
      nama_hari = 'Min'

    def cek_bulan(b,t):
      if b == 1 or b == 2:
        b = b + 12
        t = t - 1
      else:
        b = b
        t = t
      return b,t

    if t < 0:
      b1,t1 = cek_bulan(b,t)
      A = 0
      B = 0
    else:
      date_1 = datetime.date(t,b,h)
      date_2 = datetime.date(1582,10,4)
      b1,t1 = cek_bulan(b,t)
      if date_1 <= date_2:
        A = 0
        B = 0
      else:
        A = int(t1/100)
        B = 2+int(A/4)-A

    JD = int(365.25*(t1+4716))+int(30.6001*(b1+1))+h+B-1524.5
    jdlokal = JD - zone/24

    #sudut tanggal
    T = 2*pi*(jdlokal-2451545)/365.25

    #sudut deklinasi matahari
    delta = degrees(radians(0.37877) + radians(23.264) * sin(radians(57.297*T -79.547)) + radians(0.3812) \
          * sin(radians(2*57.297*T-82.682)) + radians(0.17132) * sin(radians(3*57.297*T-59.722)))

    #bujur rata2 matahari
    def L0(bujur_rata2_matahari):
      while not 0 <= bujur_rata2_matahari <= 360 :
        bujur_rata2_matahari -= 360
      return bujur_rata2_matahari 

    U = (jdlokal - 2451545)/36525
    bujur_rata2_matahari = 280.46607 + 36000.7698*U
    L0 = L0(bujur_rata2_matahari)

    #equation of time
    ET = (int(degrees(-radians(1789 + 237 * U) * sin(radians(L0)) - radians(7146 - 62 * U) * cos(radians(L0)) +\
                    radians(9934 - 14 * U) * sin(radians(2 * L0)) - radians(29 + 5 * U) * cos(radians(2 * L0)) + radians(74 + 10*U) *\
                    sin(radians(3 * L0)) + radians(320 - 4 * U) * cos(radians(3 * L0)) - radians(212) * sin(radians(4 * L0)))) + 1) / 1000

    #waktu transit
    waktu_transit = 12 + zone - buj/15 - ET/60


    def convert(waktu_desimal):
      jam = int(waktu_desimal)
      sisa_jam = waktu_desimal - jam
      menit = int(sisa_jam * 60)
      sisa_menit = sisa_jam * 60 - menit
      detik = 60 * sisa_menit
      if detik < 30:
        menit = menit
      else:
        menit = menit + 1

      if menit == 60:
        jam = jam + 1
        menit = 60%60
      
      if jam >= 24:
        jam = jam%24
      return jam,menit

    def HA(alt):
      hour_angle = degrees(acos((sin(radians(alt)) - sin(radians(lin)) * sin(radians(delta))) / (cos(radians(lin)) * cos(radians(delta)))))
      return hour_angle

    #Waktu Subuh
    def subuh():
      try:
        alt = -20
        waktu_subuh = waktu_transit - HA(alt) / 15
      except:
        waktu_subuh = 0
        j,m = convert(waktu_subuh)
      else:
        j,m = convert(waktu_subuh)
      return j,m

    #Waktu Terbit Matahari
    def terbit_matahari():
      try:
        alt = -0.8333 - 0.0347 * sqrt(H)
        waktu_terbit_matahari = waktu_transit - HA(alt) / 15
      except:
        waktu_terbit_matahari = 0
        j,m = convert(waktu_terbit_matahari)
      else:
        j,m = convert(waktu_terbit_matahari)
      return j,m

    #Waktu Dzuhur
    def dzuhur():
      j,m = convert(waktu_transit)
      return j,m

    #Waktu Ashar
    def ashar():
      ka = 1
      alt = degrees(acot(ka + tan(radians(abs(delta - lin)))))
      waktu_ashar = waktu_transit + HA(alt) / 15
      j,m = convert(waktu_ashar)
      return j,m

    #Waktu Maghrib
    def maghrib():
      try:
        alt = -0.8333 - 0.0347 * sqrt(H)
        waktu_maghrib = waktu_transit + HA(alt) / 15
      except:
        waktu_maghrib = 0
        j,m = convert(waktu_maghrib)
      else:
        j,m = convert(waktu_maghrib)
      return j,m

    #Waktu Isya'
    def isya():
      try:
        alt = -18
        waktu_isya = waktu_transit + HA(alt) / 15
      except:
        waktu_isya = 0
        j,m = convert(waktu_isya)
      else:
        j,m = convert(waktu_isya)
      return j,m

    js,ms = subuh()
    jt,mt = terbit_matahari()
    jd,md = dzuhur()
    ja,ma = ashar()
    jm,mm = maghrib()
    ji,mi = isya()
    
    f'---'
    st.write(f'## {nama_hari}, {form_hari}')
    st.caption(f'### {hh} {bh} {th}')
    if ekstrim == False:
        st.write(f'### *`Subuh _________{js:0>2d}:{ms:0>2d}`*')
        st.write(f'### *`Terbit ________{jt:0>2d}:{mt:0>2d}`*')
        st.write(f'### *`Dzuhur ________{jd:0>2d}:{md:0>2d}`*')
        st.write(f'### *`Ashar _________{ja:0>2d}:{ma:0>2d}`*')
        st.write(f'### *`Maghrib _______{jm:0>2d}:{mm:0>2d}`*')
        st.write(f'### *`Isya __________{ji:0>2d}:{mi:0>2d}`*')
    else:
        if js == 0 and ms == 0:
            st.write(f'### *`Subuh _________{korektor_subuhM}`*')
        else:
            st.write(f'### *`Subuh _________{js:0>2d}:{ms:0>2d}`*')
        
        if jt == 0 and mt == 0:
            st.write(f'### *`Terbit ________{korektor_terbitM}`*')
        else:
            st.write(f'### *`Terbit ________{jt:0>2d}:{mt:0>2d}`*')
        
        st.write(f'### *`Dzuhur ________{jd:0>2d}:{md:0>2d}`*')
        st.write(f'### *`Ashar _________{ja:0>2d}:{ma:0>2d}`*')
        
        if jm == 0 and mm == 0:
            st.write(f'### *`Maghrib _______{korektor_maghribM}`*')
        else:
            st.write(f'### *`Maghrib _______{jm:0>2d}:{mm:0>2d}`*')
        
        if ji == 0 and mi == 0:
            st.write(f'### *`Isya __________{korektor_isyaM}`*')
        else:
            st.write(f'### *`Isya __________{ji:0>2d}:{mi:0>2d}`*')
    f'---'
    with st.expander ("parameter yang digunakan"):
        st.write(f'#### LOKASI')
        st.text_input("Lokasi saat ini", value = f"{wilayah[0]}", disabled = True)
        st.text_input("Zona Waktu", value = f"{timezone}", disabled = True)
        st.text_input("Lintang", value = f"{lin}", disabled = True)
        st.text_input("Bujur", value = f"{buj}", disabled = True)
        
        st.write(f'#### PERHITUNGAN SHOLAT')
        st.text_input("Sudut Subuh", value = "20 derajat", disabled = True)
        st.text_input("Sudut Isya", value = "18 derajat", disabled = True)
        st.text_input("KA", value = "1 (Syafi'i)", disabled = True)
        st.text_input("Koreksi Dzuhur", value = "0 menit", disabled = True)

elif choose == "About":
  st.title("KAMU NANYAK?")
  about.main()
      
