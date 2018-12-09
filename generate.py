import os

from datetime import datetime
from pylatex.utils import italic, bold
from pylatex import *

import numpy as np
import matplotlib.pyplot as plt

WEALTH = 0
CONTROL = 1
desire_string = {0: "wealth",
                 1: "control"}

def generate(name, data, saveloc = 'generated/wealth_vs_control'):
    geometry_options = {}
    doc = Document(geometry_options=geometry_options)

    desire_str = desire_string[data["desire"]]

    header = PageStyle("header")
    with header.create(Head("R")):
        header.append("Prepared for {}".format(name))
        header.append(LineBreak())
        header.append(datetime.now().strftime("%B %d, %Y"))
    doc.preamble.append(header)
    doc.change_document_style("header")

    # brief overview of conflicting interests
    add_summary(doc, data)

    # how consistent are your decisions with goals
    n_control = np.count_nonzero(data['answers'])
    n_total = len(data['answers'])
    n_wealth = n_total - n_control

    if (n_total == n_control and data['desire'] == CONTROL) or (n_total == n_wealth and data['desire'] == WEALTH):
        doc.append('Congratulations, your decisions are completely consistent and aligned with your motivations! You\'re on the right path towards achieving ' + desire_str + '. Be careful though. Rarely, are decisions as clear cut as presented in this module. In addition, there are a vast number of potential dilemmas outside of those discussed here. We are currently working on building out more sections.')
        doc.generate_pdf(saveloc)
        return

    add_consistency(doc, n_control, n_wealth, n_total, desire_str)

    add_breakdown(doc, data['desire'], data['answers'])


    doc.generate_pdf('generated/wealth_vs_control')

def add_summary(doc, data):
    with doc.create(Section("Wealth v. Control Overview")):
        doc.append("""Wealth and Control are the two most common motivators for entrepreneurs. Although controlling a valuable startup is extremely attractive, the number of people who are able to do this is few and far between. Not everyone can be Bill Gates. Few achieve this entrepreneurial ideal. More commonly, founders must make choices that lean towards one goal at the expense of the other.""")
    with doc.create(Section('Preferred Outcome')):
        doc.append('Having self-understanding concerning your desired outcome helps you consistently make decisions in alignment with your long-term goals. ')
        if data["desire"] == WEALTH:
            doc.append('Based on your answer to the final question you are primarily motivated by wealth. According to data from the Kauffman Foundation\'s study of 549 founders, 75% of respondents were also motivated to build wealth. 64% were motivated by owning their own business. Unfortunately, in order to achieve wealth you must sacrifice control. Attracting the resources required for success means giving up assets.')
        else:
            doc.append('Based on your answer to the final question you are primarily motivated by a desire to control your venture. According to data from the Kauffman Foundation\'s study of 549 founders, 64% of respondents also sought after control. In contrast, 75% were motivated by money. To achieve your goal of control, you must maintain assets that could otherwise be used for hiring strong talent or attracting cofounders. Control comes with the sacrifice of wealth.')

def add_consistency(doc, n_control, n_wealth, n_total, desire_str):
    with doc.create(Section('Consistency')):
        doc.append('Founders that attempt to achieve both wealth and control are more likely to fail at both. Similarly, you should avoid making decisions that alternate between wealth and control. Consistency is crucial. Consistent decisions give you the best chance of achieving {}. '.format(desire_str))

        doc.append('Based on your answers, you choose to make decision in favor of control {} / {} times and and decisions in favor of wealth {} / {} times. '.format(n_control, n_total, n_wealth, n_total))
        if n_control > n_wealth is not data["desire"] == WEALTH:
            doc.append('On average, your decisions align with your overall goal. ')
        else:
            doc.append('On average, you are making decisions that prevent you from achieving your goal. It is worth reconsidering your decisions or your desired outcome.')

def add_breakdown(doc, desire, answers):
    N = 5
    split = [answers[0:4], answers[4:7], answers[7:10], answers[10:12], answers[12:13]][::-1]
    control = [sum(a) for a in split]
    wealth = [len(a) - sum(a) for a in split]
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    if desire == WEALTH:
        left = control
        right = wealth
    else:
        left = wealth
        right = control

    plt.figure(figsize=(9, 3))
    p1 = plt.barh(ind, left, color='#BB2222')
    p2 = plt.barh(ind, right, left=left, color='#999999')

    plt.title('Decision Breakdown')
    plt.yticks(ind, reversed(('Cofounders', 'Hires', 'Investors', 'Successors', 'Other Factors')))
    plt.xticks(np.arange(5))

    if desire == WEALTH:
        plt.legend((p1[0], p2[0]), ('Control (Inconsistent)', 'Wealth (Consistent)'))
    else:
        plt.legend((p1[0], p2[0]), ('Wealth (Inconsistent)', 'Control (Consistent)'))

    # setion breakdown
    with doc.create(Section('Breakdown')):
        doc.append('The questions fall into 5 primary categories: Cofounders, Hires, Investors, Successors, and Other Factors. The figure below shows the alignment of your decisions in each category.')

        with doc.create(Figure(position='h!')) as plot:
            plot.add_plot(width=NoEscape(r'1\textwidth'), dpi=300)
            plot.add_caption('')

