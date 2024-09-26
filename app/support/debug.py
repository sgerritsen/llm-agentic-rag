class SimpleDirectoryReader():
    def __init__(self, documents: list):
        self.documents = documents

    def number_of_docs(self):
        all_docs = 0
        for docs in self.documents:
            for doc in docs:
                # do something with the doc
                all_docs += 1

        return all_docs

    def first_doc(self):
        return self.documents[0].text


def print_debug(message):
    debug_message = ('--------------------------------------------------------------------------------\n'
             f"{message}\n"
             '--------------------------------------------------------------------------------')
    print(debug_message)
