import tempfile
import docx2txt


class doc_loading:

    def __init__(self, path):
        self.path = path

    def text(self):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".docx"
        ) as temp_file:

            temp_file.write(self.path.getvalue())

            temp_path = temp_file.name

        data = docx2txt.process(temp_path)

        text = data.strip()

        return text

# load = loading("/home/ahmad/workshop/AI-powered-resume-analyzer/component/Ahmad resume .docx")
# load.text()

    