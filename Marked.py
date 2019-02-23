#!/usr/bin/env python

# Replacing Marked Feature Roadmap and Notes
# Key features:
# * [X] Monitor for changes to text file. On change, update HTML file that reloads every second unless the document is in focus (https://forum.sublimetext.com/t/best-way-to-live-preview-code/20885/6)
# * [X] Visualize word repetition
# * [X] Highlight complex words
# * [X] Highlight words to avoid
# * [X] Word count for document, and each paragraph
# * [ ] Fog index (https://en.wikipedia.org/wiki/Gunning_fog_index)
# * [ ] Flesch-Kincaid readability test (https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests)
#
# This will be key: https://stackoverflow.com/questions/46759492/syllable-count-in-python
#
# Design:
# * [X] Article down middle of page
# * [X] Left side: paragraph statistics (number of words, number of complex words, words to avoid )
# * [ ]Right side:
#   * [ ] Floating document statistics
#     * [X] Last updated
#     * [X] Word count
#     * [X] Number complex words
#     * [ ] Fog Index (color based on range)
#     * [ ] Readability (color based on range)

# Import modules
import sys
import os
from time import sleep
import datetime
import re

####
## "pec_overused" is a list of overused words from Plain English Campaign (http://www.plainenglish.co.uk/the-a-z-of-alternative-words.html)
## pec_overused    = ["an absence of", "absence of", "abundance", "accede to", "accelerate", "accentuate", "accommodation", "accompanying", "accomplish", "according to our records", "accordingly", "acknowledge", "acquaint yourself with", "acquiesce", "acquire", "additional", "adjacent", "adjustment", "admissible", "advantageous", "advise", "affix", "afford an opportunity", "afforded", "aforesaid", "aggregate", "aligned", "alleviate", "allocate", "along the lines of", "alternative", "alternatively", "ameliorate", "amendment", "anticipate", "apparent", "applicant", "application use", "appreciable", "apprise", "appropriate", "appropriate to", "approximately", "as a consequence of", "as of the date of", "as regards", "ascertain", "assemble", "assistance", "at an early date", "at its discretion", "at the moment", "at the present time", "attempt try", "attend", "attributable to", "authorise", "authority", "axiomatic", "beneficial", "bestow", "breach", "by means of", "cease", "circumvent", "clarification", "combine", "combined", "commence", "communicate", "competent", "compile", "complete", "completion", "comply with", "component", "comprises", "compulsory", "conceal", "concerning", "conclusion", "concur", "condition", "consequently", "considerable", "constitutes", "construe", "consult", "consumption", "contemplate", "contrary to", "correct", "correspond", "costs the sum of", "counter", "courteous", "cumulative", "currently", "customary", "deem to be", "defer", "deficiency", "delete", "demonstrate", "denote", "depict", "designate", "desire", "despatch", "dispatch", "despite the fact that", "determine", "detrimental", "difficulties", "diminish", "disburse", "discharge", "disclose", "disconnect", "discontinue", "discrete", "discuss", "disseminate", "documentation", "domiciled in", "dominant", "due to the fact that", "duration", "during which time", "dwelling", "eligible", "elucidate", "emphasise", "empower", "enable", "enclosed", "enclosed", "encounter", "endeavour", "enquire", "enquiry", "ensure", "entitlement", "envisage", "equivalent", "erroneous", "establish", "evaluate", "evince", "ex officio", "exceptionally", "excessive", "exclude", "excluding", "exclusively", "exempt from", "expedite", "expeditiously", "expenditure", "expire", "extant", "extremity", "facilitate", "factor", "failure to", "finalise", "following", "for the duration of ", "for the purpose of", "for the reason that", "formulate", "forthwith", "forward", "frequently", "furnish give", "further to", "furthermore", "give consideration to", "grant", "hereby", "herein", "hereinafter", "hereof", "hereto", "heretofore", "hereunder", "herewith", "hitherto", "hold in abeyance", "hope and trust", "illustrate", "immediately", "implement", "imply", "in a number of cases", "in accordance with", "in addition to", "in advance", "in case of", "in conjunction with", "in connection with", "in consequence", "in excess of", "in lieu of", "in order that", "in receipt of", "in relation to", "in respect of", "in the absence of", "in the course of", "in the event of/that", "in the majority of instances", "in the near future", "in the neighbourhood of", "in view of the fact that", "inappropriate", "inception", "incorporating", "incur", "indicate", "inform", "initially", "initiate", "insert", "instances", "intend to", "intimate", "irrespective of", "is of the opinion", "issue", "it is known that", "locality", "locate", "mandatory", "manner", "manufacture", "marginal", "material", "materialise", "may in the future", "merchandise", "mislay", "modification", "moreover", "nevertheless", "notify", "notwithstanding", "numerous", "obligatory", "obtain", "occasioned by", "on behalf of", "on numerous occasions", "on request", "on the grounds that because", "on the occasion that", "operate", "optimum", "option", "ordinarily", "otherwise", "outstanding", "owing to", "participate", "particulars", "per annum", "perform", "permissible", "permit", "personnel", "persons", "peruse", "place", "possess", "possessions", "practically", "predominant", "prescribe", "preserve", "previous", "principal", "prior to", "proceed", "procure", "profusion of", "prohibit", "projected", "prolonged", "promptly", "promulgate", "proportion", "provide", "provided that", "provisions", "proximity", "purchase", "pursuant to", "reduce", "reduction", "referred to as", "refers to", "regard to", "regarding", "regulation", "reimburse", "reiterate", "relating to about", "remain", "remainder", "remittance", "remuneration", "render", "report", "represents", "request", "require", "requirements", "reside", "residence", "restriction", "retain", "review", "revised", "scrutinise", "select", "settle", "similarly", "solely", "specified", "state", "statutory", "subject to", "submit", "subsequent to", "subsequent upon", "subsequently", "substantial", "substantially", "sufficient", "supplement", "supplementary", "supply", "terminate", "that being the case if so", "the question as to whether", "thereafter", "thereby", "therein", "thereof", "thereto", "thus", "to date", "to the extent that", "transfer", "transmit", "unavailability", "undernoted", "undersigned", "undertake", "uniform", "unilateral", "unoccupied", "until such time until", "utilisation", "utilise", "virtually", "visualise", "we have pleasure in", "whatsoever", "whensoever", "whereas", "whether or not", "with a view to", "with effect from", "with reference to", "with regard to", "with respect to", "with the minimum of delay", "your attention is drawn to", "zone"]
#
## "marked_overused" is a list of overused words from the Marked 2 app
## marked_overused = ["a total of", "absolutely", "abundantly", "actually", "all things being equal", "as a matter of fact", "as far as I am concerned", "at the end of the day", "at this moment in time", "basically", "current", "currently", "during the period from", "each and every one", "existing", "extremely", "I am of the opinion that", "I would like to say", "I would like to take this opportunity to", "in due course", "in the end", "in the final analysis", "in this connection", "in total", "in view of the fact that", "it should be understood", "last but not least", "obviously", "of course", "other things being equal", "pretty much", "quite", "really", "really quite", "regarding the", "the fact of the matter is", "the month of", "the months of", "to all intents and purposes", "to one's own mind", "very", "a large number of", "a number of", "absence of", "abundance", "accede to", "accelerate", "accentuate", "accommodation", "accompany", "accompanying", "accomplish", "accorded", "according to our records", "accordingly", "accrue", "acknowledge", "acquaint yourself with", "acquiesce", "acquire", "additional", "adjacent", "adjacent to", "adjustment", "admissible", "advantageous", "adversely impact", "advise", "affix", "afford an opportunity", "afforded", "aforementioned", "aforesaid", "aggregate", "aircraft", "aligned", "all of", "alleviate", "allocate", "along the lines of", "already existing", "alternative", "alternatively", "ameliorate", "amendment", "anticipate", "apparent", "applicant", "application", "appreciable", "apprise", "appropriate", "appropriate to", "approximately", "as a consequence of", "as a means of", "as of the date of", "as of yet", "as regards", "as to", "as yet", "ascertain", "assemble assistance", "assistance", "at an early date", "at its discretion", "at the moment", "at the present time", "at this time", "attain", "attempt", "attend", "attributable to", "authorise", "authority to", "authorize", "axiomatic", "because of the fact that", "belated", "beneficial", "benefit from", "bestow", "breach", "by means of", "by virtue of", "calculate", "cease", "circumvent", "clarification", "close proximity", "combine", "combined", "commence", "communicate", "competent", "compile", "complete", "completion", "comply with", "component", "comprise", "compulsory", "conceal", "concerning", "conclusion", "concur", "condition", "consequently", "considerable", "consolidate", "constitute", "constitutes", "construe", "consult", "consumption", "contemplate", "contrary to", "correct", "correspond", "costs the sum of", "counter", "courteous", "cumulative", "currently", "customary", "deduct", "deem to be", "defer", "deficiency", "delete", "demonstrate", "denote", "depart", "depict", "designate", "desire", "despatch", "despite the fact that", "determine", "detrimental", "difficulties", "diminish", "disburse", "discharge", "disclose", "disconnect", "discontinue", "discrete", "discuss", "dispatch", "disseminate", "documentation", "domiciled in", "dominant", "due to the fact of", "due to the fact that", "duration", "during which time", "dwelling", "each and every", "economical", "eligible", "eliminate", "elucidate", "emphasise", "employ", "empower", "enable", "enclosed", "encounter", "endeavor", "endeavour", "enquire", "enquiry", "ensure", "entitlement", "enumerate", "envisage", "equitable", "equivalent", "erroneous", "establish", "evaluate", "evidenced", "evince", "ex officio", "exceptionally", "excessive", "exclude", "excluding", "exclusively", "exempt from", "expedite", "expeditiously", "expend", "expenditure", "expiration", "expire", "extant", "extremity", "fabricate", "facilitate", "factor", "factual evidence", "failure to", "feasible", "finalise", "finalize", "first and foremost", "following", "for the duration of", "for the purpose of", "for the reason that", "forfeit", "formulate", "forthwith", "forward", "frequently", "furnish", "further to", "furthermore", "generate", "give consideration to", "grant", "henceforth", "hereby", "herein", "hereinafter", "hereof", "hereto", "heretofore", "hereunder", "herewith", "hitherto", "hold in abeyance", "honest truth", "hope and trust", "however", "if and when", "illustrate", "immediately", "impacted", "implement", "imply", "in a number of cases", "in a timely manner", "in accordance with", "in addition to", "in addition", "in advance", "in all likelihood", "in an effort to", "in between", "in case of", "in conjunction with", "in connection with", "in consequence", "in excess of", "in lieu of", "in light of the fact that", "in many cases", "in order that", "in order to", "in receipt of", "in regard to", "in relation to", "in respect of", "in some instances", "in terms of", "in the absence of", "in the course of", "in the event of", "in the event that", "in the majority of instances", "in the near future", "in the neighbourhood of", "in the process of", "in view of the fact that", "inappropriate", "inception", "incorporating", "incumbent upon", "incurred", "indicate", "indication", "inform", "initially", "initiate", "insert", "instances", "intend to", "intimate", "irrespective of", "is applicable to", "is authorized to", "is in accordance with", "is of the opinion", "is responsible for", "issue", "it is essential", "it is known that", "jeopardise", "liaise with", "locality", "locate", "magnitude", "mandatory", "manner", "manufacture", "marginal", "material", "materialise", "maximum", "may in the future", "merchandise", "methodology", "minimize", "minimum", "mislay", "modification", "modify", "monitor", "moreover", "multiple", "necessitate", "negligible", "nevertheless", "not certain", "not many", "not often", "not unless", "not unlike", "notify", "notwithstanding", "null and void", "numerous", "objective", "obligate", "obligatory", "obtain", "occasioned by", "on behalf of", "on numerous occasions", "on receipt of", "on request", "on the contrary", "on the grounds that", "on the occasion that", "on the other hand", "one particular", "operate", "optimum", "option", "ordinarily", "otherwise", "outstanding", "overall", "owing to", "owing to the fact that", "partially", "participate", "particulars", "pass away", "per annum", "percentage of", "perform", "permissible", "permit", "personnel", "persons", "pertaining to", "peruse", "place", "please find enclosed", "point in time", "portion", "possess", "possessions", "practically", "preclude", "predominant", "prescribe", "preserve", "previous", "previously", "principal", "prior to", "prioritize", "proceed", "procure", "proficiency", "profusion of", "progress something", "prohibit", "projected", "prolonged", "promptly", "promulgate", "proportion", "provide", "provided that", "provisions", "proximity", "purchase", "pursuant to", "put simply", "qualify for", "readily apparent", "reconsider", "reduce", "reduction", "refer back", "refer to", "referred to as", "regard to", "regarding", "regulation", "reimburse", "reiterate", "relating to", "relocate", "remain", "remainder", "remittance", "remuneration", "render", "represent", "request", "require", "requirement", "requirements", "reside", "residence", "restriction", "retain", "review", "revised", "satisfy", "scrutinise", "select", "settle", "shall", "should you wish", "similar to", "similarly", "solely", "solicit", "span across", "specified", "state", "statutory", "strategize", "subject to", "submit", "subsequent", "subsequent to", "subsequent upon", "subsequently", "substantial", "substantially", "successfully complete", "sufficient", "supplement", "supplementary", "supply", "take pleasure in", "tenant", "terminate", "that being the case", "the month of", "the question as to whether", "thereafter", "thereby", "therefore", "therein", "thereof", "thereto", "thus", "time period", "to date", "to the extent that", "took advantage of", "transfer", "transmit", "transpire", "ultimately", "unavailability", "undernoted", "undersigned", "undertake", "uniform", "unilateral", "unoccupied", "until such time", "until such time as", "utilisation", "utilise", "utilization", "utilize", "validate", "variation", "various different", "very", "virtually", "visualise", "ways and means", "we have pleasure in", "whatsoever", "whensoever", "whereas", "whether or not", "whilst", "with a view to", "with effect from", "with reference to", "with regard to", "with respect to", "with the exception of", "with the minimum of delay", "witnessed", "you are requested", "your attention is drawn"]
#
## "overlap" is a join of the two lists. This is the list used in this program.
overlap         = ['an absence of', 'absence of', 'abundance', 'accede to', 'accelerate', 'accentuate', 'accommodation', 'accompanying', 'accomplish', 'according to our records', 'accordingly', 'acknowledge', 'acquaint yourself with', 'acquiesce', 'acquire', 'additional', 'adjacent', 'adjustment', 'admissible', 'advantageous', 'advise', 'affix', 'afford an opportunity', 'afforded', 'aforesaid', 'aggregate', 'aligned', 'alleviate', 'allocate', 'along the lines of', 'alternative', 'alternatively', 'ameliorate', 'amendment', 'anticipate', 'apparent', 'applicant', 'application use', 'appreciable', 'apprise', 'appropriate', 'appropriate to', 'approximately', 'as a consequence of', 'as of the date of', 'as regards', 'ascertain', 'assemble', 'assistance', 'at an early date', 'at its discretion', 'at the moment', 'at the present time', 'attempt try', 'attend', 'attributable to', 'authorise', 'authority', 'axiomatic', 'beneficial', 'bestow', 'breach', 'by means of', 'cease', 'circumvent', 'clarification', 'combine', 'combined', 'commence', 'communicate', 'competent', 'compile', 'complete', 'completion', 'comply with', 'component', 'comprises', 'compulsory', 'conceal', 'concerning', 'conclusion', 'concur', 'condition', 'consequently', 'considerable', 'constitutes', 'construe', 'consult', 'consumption', 'contemplate', 'contrary to', 'correct', 'correspond', 'costs the sum of', 'counter', 'courteous', 'cumulative', 'currently', 'customary', 'deem to be', 'defer', 'deficiency', 'delete', 'demonstrate', 'denote', 'depict', 'designate', 'desire', 'despatch', 'dispatch', 'despite the fact that', 'determine', 'detrimental', 'difficulties', 'diminish', 'disburse', 'discharge', 'disclose', 'disconnect', 'discontinue', 'discrete', 'discuss', 'disseminate', 'documentation', 'domiciled in', 'dominant', 'due to the fact that', 'duration', 'during which time', 'dwelling', 'eligible', 'elucidate', 'emphasise', 'empower', 'enable', 'enclosed', 'enclosed', 'encounter', 'endeavour', 'enquire', 'enquiry', 'ensure', 'entitlement', 'envisage', 'equivalent', 'erroneous', 'establish', 'evaluate', 'evince', 'ex officio', 'exceptionally', 'excessive', 'exclude', 'excluding', 'exclusively', 'exempt from', 'expedite', 'expeditiously', 'expenditure', 'expire', 'extant', 'extremity', 'facilitate', 'factor', 'failure to', 'finalise', 'following', 'for the duration of ', 'for the purpose of', 'for the reason that', 'formulate', 'forthwith', 'forward', 'frequently', 'furnish give', 'further to', 'furthermore', 'give consideration to', 'grant', 'hereby', 'herein', 'hereinafter', 'hereof', 'hereto', 'heretofore', 'hereunder', 'herewith', 'hitherto', 'hold in abeyance', 'hope and trust', 'illustrate', 'immediately', 'implement', 'imply', 'in a number of cases', 'in accordance with', 'in addition to', 'in advance', 'in case of', 'in conjunction with', 'in connection with', 'in consequence', 'in excess of', 'in lieu of', 'in order that', 'in receipt of', 'in relation to', 'in respect of', 'in the absence of', 'in the course of', 'in the event of/that', 'in the majority of instances', 'in the near future', 'in the neighbourhood of', 'in view of the fact that', 'inappropriate', 'inception', 'incorporating', 'incur', 'indicate', 'inform', 'initially', 'initiate', 'insert', 'instances', 'intend to', 'intimate', 'irrespective of', 'is of the opinion', 'issue', 'it is known that', 'locality', 'locate', 'mandatory', 'manner', 'manufacture', 'marginal', 'material', 'materialise', 'may in the future', 'merchandise', 'mislay', 'modification', 'moreover', 'nevertheless', 'notify', 'notwithstanding', 'numerous', 'obligatory', 'obtain', 'occasioned by', 'on behalf of', 'on numerous occasions', 'on request', 'on the grounds that because', 'on the occasion that', 'operate', 'optimum', 'option', 'ordinarily', 'otherwise', 'outstanding', 'owing to', 'participate', 'particulars', 'per annum', 'perform', 'permissible', 'permit', 'personnel', 'persons', 'peruse', 'place', 'possess', 'possessions', 'practically', 'predominant', 'prescribe', 'preserve', 'previous', 'principal', 'prior to', 'proceed', 'procure', 'profusion of', 'prohibit', 'projected', 'prolonged', 'promptly', 'promulgate', 'proportion', 'provide', 'provided that', 'provisions', 'proximity', 'purchase', 'pursuant to', 'reduce', 'reduction', 'referred to as', 'refers to', 'regard to', 'regarding', 'regulation', 'reimburse', 'reiterate', 'relating to about', 'remain', 'remainder', 'remittance', 'remuneration', 'render', 'report', 'represents', 'request', 'require', 'requirements', 'reside', 'residence', 'restriction', 'retain', 'review', 'revised', 'scrutinise', 'select', 'settle', 'similarly', 'solely', 'specified', 'state', 'statutory', 'subject to', 'submit', 'subsequent to', 'subsequent upon', 'subsequently', 'substantial', 'substantially', 'sufficient', 'supplement', 'supplementary', 'supply', 'terminate', 'that being the case if so', 'the question as to whether', 'thereafter', 'thereby', 'therein', 'thereof', 'thereto', 'thus', 'to date', 'to the extent that', 'transfer', 'transmit', 'unavailability', 'undernoted', 'undersigned', 'undertake', 'uniform', 'unilateral', 'unoccupied', 'until such time until', 'utilisation', 'utilise', 'virtually', 'visualise', 'we have pleasure in', 'whatsoever', 'whensoever', 'whereas', 'whether or not', 'with a view to', 'with effect from', 'with reference to', 'with regard to', 'with respect to', 'with the minimum of delay', 'your attention is drawn to', 'zone', 'a total of', 'absolutely', 'abundantly', 'actually', 'all things being equal', 'as a matter of fact', 'as far as I am concerned', 'at the end of the day', 'at this moment in time', 'basically', 'current', 'during the period from', 'each and every one', 'existing', 'extremely', 'I am of the opinion that', 'I would like to say', 'I would like to take this opportunity to', 'in due course', 'in the end', 'in the final analysis', 'in this connection', 'in total', 'it should be understood', 'last but not least', 'obviously', 'of course', 'other things being equal', 'pretty much', 'quite', 'really', 'really quite', 'regarding the', 'the fact of the matter is', 'the month of', 'the months of', 'to all intents and purposes', "to one's own mind", 'very', 'a large number of', 'a number of', 'accompany', 'accorded', 'accrue', 'adjacent to', 'adversely impact', 'aforementioned', 'aircraft', 'all of', 'already existing', 'application', 'as a means of', 'as of yet', 'as to', 'as yet', 'assemble assistance', 'at this time', 'attain', 'attempt', 'authority to', 'authorize', 'because of the fact that', 'belated', 'benefit from', 'by virtue of', 'calculate', 'close proximity', 'comprise', 'consolidate', 'constitute', 'deduct', 'depart', 'due to the fact of', 'each and every', 'economical', 'eliminate', 'employ', 'endeavor', 'enumerate', 'equitable', 'evidenced', 'expend', 'expiration', 'fabricate', 'factual evidence', 'feasible', 'finalize', 'first and foremost', 'for the duration of', 'forfeit', 'furnish', 'generate', 'henceforth', 'honest truth', 'however', 'if and when', 'impacted', 'in a timely manner', 'in addition', 'in all likelihood', 'in an effort to', 'in between', 'in light of the fact that', 'in many cases', 'in order to', 'in regard to', 'in some instances', 'in terms of', 'in the event of', 'in the event that', 'in the process of', 'incumbent upon', 'incurred', 'indication', 'is applicable to', 'is authorized to', 'is in accordance with', 'is responsible for', 'it is essential', 'jeopardise', 'liaise with', 'magnitude', 'maximum', 'methodology', 'minimize', 'minimum', 'modify', 'monitor', 'multiple', 'necessitate', 'negligible', 'not certain', 'not many', 'not often', 'not unless', 'not unlike', 'null and void', 'objective', 'obligate', 'on receipt of', 'on the contrary', 'on the grounds that', 'on the other hand', 'one particular', 'overall', 'owing to the fact that', 'partially', 'pass away', 'percentage of', 'pertaining to', 'please find enclosed', 'point in time', 'portion', 'preclude', 'previously', 'prioritize', 'proficiency', 'progress something', 'put simply', 'qualify for', 'readily apparent', 'reconsider', 'refer back', 'refer to', 'relating to', 'relocate', 'represent', 'requirement', 'satisfy', 'shall', 'should you wish', 'similar to', 'solicit', 'span across', 'strategize', 'subsequent', 'successfully complete', 'take pleasure in', 'tenant', 'that being the case', 'therefore', 'time period', 'took advantage of', 'transpire', 'ultimately', 'until such time', 'until such time as', 'utilization', 'utilize', 'validate', 'variation', 'various different', 'ways and means', 'whilst', 'with the exception of', 'witnessed', 'you are requested', 'your attention is drawn']
####

# A list of be verbs to avoid
be_verbs        = ["am", "is", "are", "was", "were", "be", "being", "been", "you're", "they're"]
# A list of words to exclude from word repetition highlighting
exclude         = ["the", "a", "or", "my", "and", "to", "we", "I", "for", "i", "what", "of", "that", "it", "you", "your", "have", "which"] + be_verbs

# Global variables for pasring Markdown
types = ["", "", ""]
active = ""

# Method: Markdown
# Purpose: Take a raw string from a file, formatted in Markdown, and parse it into HTML.
# Parameters:
# - Line: Line to be parsed. (String)
def Markdown(line):
    # Make global variables accessible in the method, and initialize method variables.
    # Must be global to persist between method calls.
    global types, active
    start = 1

    # Use {} to enclose an article series reference. Enclosed text identifies the article series, in the form of a file that the parser
    # opens, reads, and inserts into the actual article.
    # If line starts with {}, open target file, and return the contents with a return statement. Skip the rest w/ a return statement.

    # Part of a series
    if (line.startswith("{")):
        fd = open("Content/System/"+line.lstrip("{").replace("}", "").strip(), "r")
        line = "<ul style=\"border:1px dashed gray\" id=\"series_index\">\n"
        for each in fd.read().split("\n"):
            line += "    <li>"+Markdown(each)+"</li>\n"
        line += "</ul>"
        types.append("RAW HTML")
        fd.close()
    # Header elements, <h1>-<h6>
    elif (line.startswith("#")):
        line = ("<h%d>"+line.replace("#", "").strip()+"</h%d>") % (line.split(" ")[0].count("#"), line.split(" ")[0].count("#"))+"\n"
        types.append("<h>,,</h>")
    # Images
    elif (line.startswith("![")):
        types.append("<img>,,</img>")
    # Footnote
    elif (re.match("(\[>[0-9]+\])", line) != None):
        types.append("<div class=\"footnote\">,,</div>")
    # Blockquotes
    elif (re.match(">|\s{4}", line) != None):
        if ((types[-1] == "<blockquote>,,</blockquote>") or (types[-1] == "<bqt>,,</bqt>")):
            types.append("<bqt>,,</bqt>")
        else:
            types.append("<blockquote>,,</blockquote>")
    # Unordered lists
    elif (re.match("\*\s", line) != None):
        line = line.replace("* ", "")
        if ((types[-1] == "<ul>,,</ul>") or (types[-2] == "<ul>,,</ul>") or (types[-3] == "<ul>,,</ul>") or (types[-1] == "<li>,,</li>") or (types[-2] == "<li>,,</li>") or (types[-3] == "<li>,,</li>")):
            types.append("<li>,,</li>")
        else:
            types.append("<ul>,,</ul>")
    # Ordered lists
    elif (re.match("[0-9]+", line) != None):
        start = line.split(".")[0]
        line = re.sub("[0-9]+\.\s", "", line)
        if ((types[-1] == "<ol>,,</ol>") or (types[-2] == "<ol>,,</ol>") or (types[-3] == "<ol>,,</ol>")):
            types.append("<li>,,</li>")
        else:
            types.append("<ol>,,</ol>")
    # Paragraphs
    elif (re.match("[a-zA-Z_\[\*\"]", line) != None):
        types.append("<p>,,</p>")
    # Raw HTML code.
    elif (re.match("<", line) != None or re.match("#", line) != None):
        types.append("RAW HTML")
    # A blank line. Two blank lines in a row is a linebreak.
    else:
        if (line.strip() == "" and types[-1] == "<blank>,,</blank>"):
            types.append("<br />")
        else:
            types.append("<blank>,,</blank>")

    # Managerial code to keep the 'types' tuple to 3 elements.
    if (len(types) == 4):
        types.pop(0)

    # Admin variables, for clarity's sake.
    current = types[-1]
    second = types[-2]
    third = types[-3]

    if (current != "RAW HTML"):
        # If I've already escaped a ascii code, pass; otherwise escape it.
        if (re.search("&[a-z]{4}\;", line) != None):
            pass
        elif (re.search("(\&)", line) != None):
            line = line.replace("&", "&#38;")

        # Horizontal rules
        if (re.match("---", line) != None):
            line = line.replace("---", "<hr style='margin:50px auto;width:50%;border:0;border-bottom:1px dashed #ccc;background:#999;' />")
        # Emdashes
        if (re.search("(--)", line)):
            line = line.replace("--", "&#160;&#8212;&#160;")
        # Parse double-quote quotations
        for each in re.findall("([\s\<\>\\\*\/\[\-\(]+\"[\[\w\%\#\\*<\>]+)", line):
            ftxt = each.replace("\"", "&#8220;", 1)
            line = line.replace(each, ftxt)
        for each in re.findall("([\)\w+\.]+\"[\s\)\]\<\>\.\*\-\,])", line):
            ftxt = each.replace("\"", "&#8221;", 1)
            line = line.replace(each, ftxt)
        # Parse single-quote quotations
        for each in re.findall("(\w+'[\w+|\s+])", line):
            ftxt = each.replace("\'", "&#8217;")
            line = line.replace(each, ftxt)
        for each in re.findall("([\s\(]'\w+)", line):
            ftxt = each.replace("\'", "&#8216;", 1)
            line = line.replace(each, ftxt)
        # Interpret <strong> tags
        for each in re.findall("\*\*{1}[\w:\"\.\+'\s\.|#\\&=,\$\!\?\;\-\[\]]+\*\*{1}", line):
            ftxt = each
            line = line.replace(each, "&&TK&&")
            ftxt = each.replace("**", "<strong>", 1)
            ftxt = ftxt.replace("**", "</strong> ", 1).strip()
            line = line.replace("&&TK&&", ftxt)            
        # Interpret <em> tags
        for each in re.findall("\*{1}[\w:\"\.\+'\s\.|#\\&=,\$\!\?\;\-\[\]]+\*{1}", line):
            ftxt = each
            line = line.replace(each, "&&TK&&")
            ftxt = each.replace("*", "<em>", 1)
            ftxt = ftxt.replace("*", "</em> ", 1).strip()
            line = line.replace("&&TK&&", ftxt)
        # Parse images, both local and remote
        for each in re.findall("(\!\[[\w\@\s\"'\|\<\>\.\#?\*\;\%\+\=!\,-:$&]+\]\(['\(\)\#\;?\@\%\w\&:\,\./\~\s\"\!\#\=\+-]+\))", line):
            desc = each.split("]")[0].lstrip("![")
            url = each.split("]")[1].split(" ")[0].lstrip("(").rstrip(")")
            if (url.startswith("http://zacjszewczyk.com/")):
                # print url.split("/")[-1]
                url = """/Static/Images/%s""" % (url.split("/")[-1])
            alt = each.split("]")[1].split(" &#8220;")[1].rstrip("&#8221;)")
            line = line.replace(each, "<div class=\"image\"><img src=\""+url+"\" alt=\""+alt+"\" title=\""+desc+"\"></div>")
        # This needs some attention to work with the new URL scheme
        # Parse links, both local and remote
        for each in re.findall("""(\[[\w\@\s\"'\|\<\>\.\#?\*\;\%\+\=!\,-:$&]*\])(\(\s*(<.*?>|((?:(?:\(.*?\))|[^\(\)]))*?)\s*((['"])(.*?)\12\s*)?\))""", line):
            desc = each[0].lstrip("[").rstrip("]")
            url = each[1].lstrip("(").rstrip(")").replace("&", "&amp;").strip()

            if (not url.startswith("http://") and not url.startswith("https://")):
                if (not url.endswith(".txt")):
                    if (url.endswith(".htm")):
                        url = "/blog/"+url.replace(" ", "-").replace(".htm", "").lower()
                else:
                    url = "/blog/"+url.replace(" ", "-").replace(".txt", "").lower()

            if (url.endswith(".txt") == True):
                url = url.replace(".txt", "").replace(" ", "-").replace("&#8220;", "").replace("&#8221;", "").replace("&#8217;", "").replace("&#8216;", "").replace("&#8217;", "")
                line = line.replace(each[0]+each[1], "<a class=\"local\" href=\""+url.replace(" ", "-")+"\">"+desc+"</a>")
            elif (url == ""):
                line = line.replace(each[0]+each[1], "<a class=\"local\" href=\""+desc.replace("<em>", "").replace("</em>", "").replace(" ", "-")+"\">"+desc+"</a>")
            else:
                line = line.replace(each[0]+each[1], "<a href=\""+url+"\">"+desc+"</a>")
        # Parse footnotes
        for each in re.findall("(\[\^[0-9]+\])", line):
            mark = each.lstrip("[^").rstrip("]")
            url = """<sup id="fnref"""+mark+""""><a href="#fn"""+mark+"""" rel="footnote">"""+mark+"""</a></sup>"""
            line = line.replace(each, url)
        # Parse single-line comments
        if (re.match("[/]{2}", line) != None):
            line = line.replace("//","<!--")+" -->"
    else:
        # Account for iframes
        if (line.startswith("<iframe")):
            line = "<div style='text-align:center;'>"+line+"</div>"
        elif (line.startswith("<ul")):
            pass
        # Anything else should be a blockquote
        else:
            line = "<blockquote>"+line+"</blockquote>"
    # If a paragraph
    if (current == "<p>,,</p>"):
        line = active+current.replace(",,", line.strip())
        active = ""
    # If an unordered list
    elif (current == "<ul>,,</ul>"):
        active = "</ul>"
        line = current.split(",,")[0].replace(">", "start='"+str(start)+"'>")+"\n<li>"+line.strip()+"</li>"
    # If an ordered list
    elif (current == "<ol>,,</ol>"):
        active = "</ol>"
        line = current.split(",,")[0]+"\n<li>"+line.strip()+"</li>"
    # If a list item
    elif (current == "<li>,,</li>"):
        line = current.replace(",,", line.strip())
    # If an element following a list item
    elif ((current != "<li>,,</li>") and ((second == "<li>,,</li>") or (second == "<ul>,,</ul>") or (second == "<ol>,,</ol>"))):
        line = line.strip()+active+"\n"
        active = ""
    # If a blockquote
    elif (current == "<blockquote>,,</blockquote>"):
        active = "</blockquote>"
        line = current.split(",,")[0]+"\n<p>"+line[2:].strip()+"</p>"
    # If the continuation of a blockquote
    elif (current == "<bqt>,,</bqt>"):
        line = "<p>"+line.strip().replace("> ", "")+"</p>"
    # If an element following a blockquote
    elif ((current != "<bqt>,,</bqt>") and ((second == "<bqt>,,</bqt>") or (second == "<blockquote>,,</blockquote>"))):
        line = line.strip().replace("> ", "")+"</blockquote>\n"
        active = ""
    # If a footnote
    elif ((current == "<div class=\"footnote\">,,</div>")):
        active = "</div>"
        mark = int(line.split("]")[0].lstrip("[>"))
        line = line.split("]")[1]
        # If the first footnote
        if (mark == 1): 
            line = current.split(",,")[0].replace("div ", "div id=\"fn"+str(mark)+"\" ")+"\n<p>"+line.strip()+"""</p><a class="fn" title="return to article" href="#fnref"""+str(mark)+"""">&#x21a9;</a>"""
        # If a later footnote
        else: 
            line = "</div>"+current.split(",,")[0]+"<p>"+line.strip()+"</p>"
            line = line.replace("div ", "div id=\"fn"+str(mark)+"\" ")+"""<a class="fn" title="return to article" href="#fnref"""+str(mark)+"""\">&#x21a9;</a>"""
    # Blank line
    else: 
        if (current == "<br />"):
            line = "<br />"
        else:
            line = line.strip()

    # Return the parsed line, now formatted with HTML.
    return line

# Method: GenFile
# Purpose: Generate an HTML file for proofing
# Parameters:
# - iname: Name of content file. (String)
def GenFile(iname):
    # Instantiate document statistics
    #   word_count is a by-paragraph word count
    #   total_word_count is the word count for the entire document
    #   total_overused_words is the count of overused words
    #   total_repeated_words is the count of unique repeated words in the document,
    #       not including the individual repeats
    #   total_avoid_words is the ocunt of words to avoid in the document
    word_count = []
    total_word_count = 0
    total_overused_words = 0
    total_repeated_words = 0
    total_avoid_words = 0

    # Open th template file, read its contents, and split them for easy access later
    template_fd = open("template.html", "r")
    template = template_fd.read().split("<!--Divider-->")
    template_fd.close()

    # Clear the output file, then write the opening HTML tags
    o_fd = open("index.html", "w").close()
    o_fd = open("index.html", "a")
    o_fd.write(template[0])

    # Open the source file
    fd = open(iname, "r")
    
    # Read the title from the source file
    title = "<h2>"+fd.readline()+"</h2>"
    
    # Get rid of the title separator (=) and the following blank line
    fd.readline()
    fd.readline()

    # Write the opening <article> tag and article title
    o_fd.write("<article>")
    o_fd.write(title)

    # Iterate over each line in the file
    for line in iter(fd.readline, ""):
        # Save a "backup" of the line, for searching a sanitized version of it
        backup = line
        
        # If we're looking at an empty line, just skip over it; else continue
        if (line.count(" ") == 0):
            continue

        # Count the occurences of word separating characters, " " and "-", and
        # add 1 to get the total word count
        word_count.append(line.count(" ")+line.count("-")+1)
        
        # Instantiate paragraph-specific statistics
        overused_words = 0 # Number of overused words
        repeated_words = 0 # Number of repeated words
        avoid_words = 0 # Number of words to avoid
        dict_count = {} # A dictionary that will count occurences of each word

        # For each word in the list of overused words to avoid, search the
        # paragraph case insensitively. If a match is found, increment the count
        # of overused words in the paragraph and document, then highlight it.
        for word in overlap:
            m = re.search("[^\w]"+word+"[^\w]", line, re.IGNORECASE)
            if (m):
                overused_words += line.lower().count(word)
                total_overused_words += overused_words

                # The first replace will capture matches with uppercase letters
                # that start a sentence, or regular lowercase words; if the first
                # replace targeted matches with uppercase letters that start a
                # sentence, the second replace will capture all other occurences of
                # that word that may exist throughout the document.
                line = line.replace(m.group(0), " <span class='replace'>"+m.group(0).strip()+"</span> ")
                if (m.group(0) != m.group(0).lower()):
                    line = line.replace(m.group(0).lower(), " <span class='replace'>"+m.group(0).lower().strip()+"</span> ")

        # For each word in the sentence, count repetitions. If there are three or more
        # of the same word in a sentnece, highlight all occurences. Also check for be
        # verbs as well, and highlight them accordingly.
        for word in backup.split(" "):
            
            # This strips any special characters from the word, such as punctuation.
            stripped = re.compile('[\W_]+').sub('', word.replace("'s", ""))
            
            if (len(stripped) == 0):
                continue

            # First check if we have decided to exclude the word, as in the case of "the",
            # "of", "a", "for", or similar words. If true, skip the word; else, proceed.
            if (stripped.lower() not in exclude):
                # If the word already exists in the dictionary, increment its count; else
                # instantiate it to 1
                if (stripped.lower() in dict_count):
                    dict_count[stripped.lower()] += 1
                else:
                    dict_count[stripped.lower()] = 1

                # Once there are at least three occurences of a word in the paragraph,
                # highlight it as a repeat word and incrememnt the number of unique words
                # repeated in the document.
                if (dict_count[stripped.lower()] == 3):
                    line = re.sub(r"([^\w])"+stripped+r"([^\w])", r"\1<span class='repeat "+stripped+"'>"+stripped+r"</span>\2", line)
                    repeated_words += 1
                    total_repeated_words += 1

            # Check for be verbs in the document. If found, highlight them and increment
            # the be verb count.
            if (stripped.lower() in be_verbs) or (stripped.lower().endswith("ly")):
                line = re.sub(r"([^\w])"+stripped+r"([^\w])", r"\1<span class='avoid'>"+stripped+r"</span>\2", line)
                avoid_words += 1
                total_avoid_words += 1

        # Write the paragraph stats div to the output file, then the parsed line.
        o_fd.write("<div class='floating_stats'><div>Word count: %d</div><div>Overused phrase: %d</div><div>Repeated: %d; Avoid: %d</div></div>" % (word_count[-1], overused_words, repeated_words, avoid_words))
        o_fd.write(Markdown(line))

    # Close the source file
    fd.close()

    # Write closing <article> tag
    o_fd.write("</article>")
    
    # Sum the paragraph word counts into a single count, for document stats
    for num in word_count:
        total_word_count += int(num)

    # Get a timestamp for the document stats
    d = datetime.datetime.now()
    utime = "%d-%d-%d %d:%d:%d" % (d.year,d.month,d.day,d.hour,d.minute,d.second)

    # Write the closing HTML to the output file, with document stats. Close it.
    o_fd.write(template[1] % (utime, utime, total_word_count, len(word_count), total_word_count/len(word_count), total_overused_words, total_repeated_words, total_avoid_words))
    o_fd.close()

if (__name__ == "__main__"):
    if (len(sys.argv) <= 1):
        print "Provide text file."
        sys.exit(1)

    f = sys.argv[1]

    if (not os.path.isfile(f)):
        print "Provide valid file."
        sys.exit(1)

    f_s = []

    while True:
        n_s = os.stat(f)
        n_s = [n_s.st_mtime, n_s.st_ctime]

        if (f_s == n_s):
            sleep(1)
            continue
        
        # File has changed
        print "Building..."
        GenFile(f)

        f_s = n_s