import fitz


class pdf_loading:

    def __init__(self, file):
        self.file = file

    def text(self):

        resume = fitz.open(
            stream=self.file.getvalue(),
            filetype="pdf"
        )

        data = ""

        for page in resume:
            data += page.get_text()

        text = data.strip()

        return text



# load = pdf_loading("/home/ahmad/workshop/AI-powered-resume-analyzer/component/CV.pdf")
# load.text()        