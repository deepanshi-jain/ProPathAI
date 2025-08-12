from fpdf import FPDF

def export_to_pdf(qa_list, filename="mock_interview.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for idx, qa in enumerate(qa_list, 1):
        question = f"Q{idx}: {qa['question']}"
        answer = f"A: {qa['answer']}\n"
        pdf.multi_cell(0, 10, question)
        pdf.multi_cell(0, 10, answer)
        pdf.ln(5)

    pdf.output(filename)
    return filename
