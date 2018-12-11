import os
import random

from datetime import datetime
from pylatex.utils import italic, bold
from pylatex import *

import numpy as np
import matplotlib.pyplot as plt

CONTROL = 0
WEALTH = 1
desire_string = {0: "control",
                 1: "wealth"}

def generate(name, data, saveloc = 'generated/wealth_vs_control'):
    geometry_options = {}
    doc = Document(geometry_options=geometry_options, page_numbers=False)

    desire_str = desire_string[data["desire"]]

    header = PageStyle("header")
    with header.create(Head("R")):
        header.append(bold(str(random.randint(100, 999))))
        header.append(italic("Prepared for {}".format(name)))
        header.append(LineBreak())
        header.append(italic(datetime.now().strftime("%B %d, %Y")))
    doc.preamble.append(header)
    doc.change_document_style("header")

    # brief overview of conflicting interests
    add_summary(doc, data)

    # how consistent are your decisions with goals
    n_wealth = np.count_nonzero(data['answers'])
    n_total = len(data['answers'])
    n_control = n_total - n_wealth

    if (n_total == n_control and data['desire'] == CONTROL) or (n_total == n_wealth and data['desire'] == WEALTH):
        with doc.create(Section("Consistency")):
            doc.append('Congratulations, your decisions are completely consistent and aligned with your motivations! You\'re on the right path towards achieving ' + desire_str + '. Be careful though. Rarely, are decisions as clear cut as presented in this module. In addition, there are a vast number of potential dilemmas outside of those discussed here. We are currently working on building out more sections.')
        doc.generate_pdf(saveloc)
        return

    add_consistency(doc, data, n_control, n_wealth, n_total, desire_str)

    add_breakdown(doc, data, data['desire'], data['answers'], data['inconsistent'])

    with doc.create(Section("References")):
        doc.append("[1] Wasserman, Noam. \"Rich Versus King: The Entrepreneur's Dilemma.\"")
        doc.append(italic(" Academy of Management Proceedings"))
        doc.append("vol. 2006, no. 1, 2006, doi:10.5465/ambpp.2006.22896807")
        doc.append(NewLine())
        doc.append("[2] Wadhwa V, Aggarwal R, Holly K, Salkever A. 2009. The anatomy of an entrepreneur: Family background and motivation. ")
        doc.append(italic("Kauffman Foundation Reserah Paper "))
        doc.append("(July)")
        doc.append(NewLine())
        doc.append("[3] Wasserman, Noam. The Founder's Dilemmas: ")
        doc.append(italic("Anticipating and Avoiding the Pitfalls That Can Sink a Startup. "))
        doc.append("Princeton University Pr, 2013.")

    doc.generate_pdf('generated/wealth_vs_control')



# Section information
def add_summary(doc, data):
    with doc.create(Section("Overview")):
        doc.append("""Wealth and control are the two most common motivators for entrepreneurs. Yet, there is an inverse correlation between achieving each.[1] Owning a valuable startup is an unusual outcome that few can achieve. More commonly, founders must make choices that achieve one goal at the expense of the other.""")
    with doc.create(Section('Preferred Outcome')):
        doc.append('Understanding your desired outcome helps to make consistent, effective decisions. ')
        if data["desire"] == WEALTH:
            doc.append('You are primarily motivated by wealth. According to data from the Kauffman Foundation\'s study of 549 founders, 75% of respondents were also motivated to build wealth. 64% were motivated by owning their own business.[2] Unfortunately, in order to achieve wealth you must sacrifice control. Attracting the resources required for success means giving up assets.')
        else:
            doc.append('You are primarily motivated by a desire to control your venture. According to data from the Kauffman Foundation\'s study of 549 founders, 64% of respondents also sought after control. In contrast, 75% were motivated by money.[2] To achieve your goal of control, you must maintain assets that could otherwise be used for hiring strong talent or attracting cofounders. Control may cost financial growth.')

def add_consistency(doc, data, n_control, n_wealth, n_total, desire_str):
    with doc.create(Section('Consistency')):
        doc.append('Founders that attempt to achieve both wealth and control are more likely to fail at both. Similarly, you should avoid making decisions that alternate between wealth and control. Consistent decisions give you the best chance of achieving {}. '.format(desire_str))

        doc.append('You made control oriented decisions {} / {} times and and decisions in favor of wealth {} / {} times. '.format(n_control, n_total, n_wealth, n_total))
        if n_control > n_wealth is not desire_str == "wealth":
            doc.append('On average, your decisions align with your overall goal. ')
        else:
            doc.append('On average, you are making decisions that prevent you from achieving your goal. It is worth reconsidering your decisions or your desired outcome.')

def add_breakdown(doc, data, desire, answers, inconsistent):
    N = 5
    split = [answers[0:4], answers[4:7], answers[7:10], answers[10:12], answers[12:14]][::-1]
    wealth = [sum(a) for a in split]
    control = [len(a) - sum(a) for a in split]
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

    with doc.create(Section('Breakdown')):
        doc.append('The questions fall into 5 primary categories: cofounders, hires, investors, successors, and other factors. The figure below shows the alignment of your decisions in each category.')

        with doc.create(Figure(position='h!')) as plot:
            plot.add_plot(width=NoEscape(r'1\textwidth'), dpi=300)
        add_inconsistent(doc, data, inconsistent)

def add_inconsistent(doc, data, inc):
    for i in range(len(inc)):
        if inc[i] != 0: inc[i] = i
    inconsistent = [inc[0:4], inc[4:7], inc[7:10], inc[10:12], inc[12:14]]
    intro = "Choose cofounders wisely. Founding together is a relationship comparable to marriage. Partners have the potential to bring success or make failure inevitable. "
    section(doc, data, inconsistent[0], 'Cofounders', intro)

    intro = "Like you, the best hires will often seek wealth or control but can introduce vital ideas and resources. "
    section(doc, data, inconsistent[1], 'Hires', intro)

    intro = "Not all money is good money. Who you take capital from is just as import as you hire and who you cofound with. "
    section(doc, data, inconsistent[2], 'Investors', intro)

    intro = "As the company grows and changes over time, the CEO must often change as well. How and when this happen are decisions to consider early. "
    section(doc, data, inconsistent[3], 'Successors', intro)

    section(doc, data, inconsistent[4], 'Other Factors', None)

def section(doc, data, inconsistent, name, intro):
    with doc.create(Subsection(name)):
        if intro != None:
            doc.append(intro)

        num = np.count_nonzero(inconsistent)
        desire = desire_string[data['desire']]
        if num == 0:
            doc.append("All your decisions in this section aligned with your goal!")
            return
        elif num == 1:
            doc.append("You made {} decision that will make it harder to achieve {}.".format(num, desire))
        else:
            doc.append("You made {} decisions that will make it harder to achieve {}.".format(num, desire))

        for q in inconsistent:
            if q != 0:
                add_question(doc, data['desire'], data['questions'][q])
                if data['desire'] == CONTROL:
                    doc.append("Why you should reconsider: " + w_exp[q])
                if data['desire'] == WEALTH:
                    doc.append("Why you should reconsider: " + c_exp[q])
                doc.append(VerticalSpace("3mm"))

w_exp = ["only 16.1% of high-potential startups are solo-founded. Adding cofounders can provide crucial knowledge, network connections, and financial capital.",
         "close relationships often skew equity splits and introduce potential misalignment. What makes sense socially doesn't always make sense for the business.",
         "cofounders with complementary skills can make better decisions than solo-founders.",
         "distributing equity attracts better talent and motivates cofounders to work towards shared success.",
         "searching broader networks can bring in intellectual capital to bolster your chances at a wealthy outcome.",
         "delegating decisions allows you to scale rapidly and sustain explosive growth",
         "expensive employees are well worth the money if they have a large impact on the succesful outcome of your venture",
         "money often comes with access to networks and wisdom that you may otherwise lack.",
         "experienced angels and venture capitalists have more expertise to guide the business towards a succesful outcome.",
         "if you refuse to suceede control, you will inevitably lose the best investors that demand decision making power.",
         "the success of your company often rests on the quality of your board. Consider giving up control to acquire a better board.",
         "likely there is a CEO more qualified than yourself. A professional CEO provides lots of financial value.",
         "consider picking up a role that is more closely aligned with your skills. Being open to succession means others can help provide value to the venture.",
         "it might be in your best interest to scale quickly. Fast growth builds financial value.",
         "seeking outside help lets you fill in personal weekness."]

c_exp = ["16.1% of high-potential startups are solo-founded. Solo-founding allows you to own more equity and own important decisions.",
         "You may be able to negotiate for more control if you are negotiating with friends and family.",
         "Although sharing the decision process can lead to better results, you may be forced into decisions that you don't agree with.",
         "Share equity and you risk losing control.",
         "Hiring people you know well means there is less risk of decisions that differ radically from yours",
         "Delegating allows you to scale but at the cost of control",
         "Junior employees generally have less desire and skill to control decision making like their experienced counterparts.",
         "Outside capital comes with conditions like board seats and increases your chances of getting replaced or forced out.",
         "Friends and family care about you're success over the business and won't force a succession of power.",
         "The best investors have more bargaining power and will want to control the direction of the venture.",
         "Holding onto the CEO title puts you in a position to make more decisions.",
         "Refusing to accept a non-CEO role makes it harder to remove and replace you smoothly.",
         "With gradual growth you have more time to be involved in more decisions. Explosive growth and this influence is unsustainable.",
         "The more skills you can provide, the less you need to rely on others who want to control the company as well."]

def add_question(doc, desire, attributes):
    with doc.create(Center()) as centered:
        with centered.create(MiniPage(width=r"0.85\textwidth")) as page:
            page.append(SmallText(attributes['title']))
            wealth = "- " + attributes['choices'][WEALTH]
            control = "- " + attributes['choices'][CONTROL]
            if desire == WEALTH:
                wealth = bold(wealth + " (your choice)")
            if desire == CONTROL:
                control = bold(control + " (your choice)")

            for a in random.sample([wealth, control], 2):
                page.append(NewLine())
                page.append(SmallText(a))

