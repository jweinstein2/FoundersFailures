import numpy as np
from pylatex import *
from pylatex.utils import italic, bold
import os
from datetime import datetime

def generate(name):
    geometry_options = {}
    doc = Document(geometry_options=geometry_options)

    header = PageStyle("header")
    with header.create(Head("L")):
        header.append("Prepared for {}".format(name))
        header.append(LineBreak())
        header.append(datetime.now().strftime("%B %d, %Y"))
    doc.preamble.append(header)
    doc.change_document_style("header")

    doc.append(LargeText(bold("Wealth vs. Control")))
    with doc.create(Section('Preferred Outcome')):
        doc.append('Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?')
    with doc.create(Section('Control')):
        doc.append('Some text and some')
    with doc.create(Section('Hires')):
        doc.append('Some text and some')
    with doc.create(Section('Investors')):
        doc.append('Some text and some')
    with doc.create(Section('Successors')):
        doc.append('Some text and some')
    with doc.create(Section('Gradual Factors')):
        doc.append('Some text and some')

    doc.generate_pdf('generated/name(wealth_vs_control)')

if __name__ == '__main__':
    generate("Dummy Client")

