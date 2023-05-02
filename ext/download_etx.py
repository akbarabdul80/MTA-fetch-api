import wget


def download_file_pdf(title: str, url: str):
    def bar_custom(current, total, width=80):
        print("Downloading " + title + ": %d%% [%d / %d] bytes" % (current / total * 100, current, total))

    wget.download(url=url,
                  out="download/" + title + ".pdf",
                  bar=bar_custom)

