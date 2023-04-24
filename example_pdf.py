from fpdf import FPDF

context = {"2022-02-05": 120, "2022-05-09": 60, "2023-07-06": 320}

pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.add_page()

pdf.add_font("DejaVu",'', R"dejavu-fonts-ttf-2.37\ttf\DejaVuSans-Bold.ttf", uni=True)
pdf.set_font(family="Dejavu", size=24)
pdf.cell(w=0, h=18, txt="Ewidencja czasu pracy", ln=1)
pdf.set_font_size(14)
pdf.cell(w=0, h=10, txt="Pracownik: Natalie Kić", ln=1)
pdf.cell(w=0, h=10, txt="Miesiąc: Kwiecień", ln=1)
pdf.cell(w=0, h=10, txt="Firma: Get2Talk", ln=1)


pdf.ln(10)

pdf.set_font(family="Times", size=12, style="B")
pdf.cell(w=50, h=10, txt="Data", border=1)
pdf.cell(w=50, h=10, txt="Czas pracy", border=1, ln=1)

pdf.set_font(family="Times", size=10)
for date, duration in context.items():
    pdf.cell(w=50, h=5, txt=f"{date}", border=1)
    pdf.cell(w=50, h=5, txt=f"{duration} minut", border=1, ln=1)

pdf.ln(10)

pdf.set_font(family="Dejavu", size=18)
pdf.cell(w=0, h=30, txt="Całkowity czas pracy: 8 godzin")
pdf.output("ewidencja.pdf")
