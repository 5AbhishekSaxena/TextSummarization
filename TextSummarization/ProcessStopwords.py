import re
from TextSummarization import nltk_implementation as ck
from textblob import TextBlob
from textblob.taggers import NLTKTagger
from textblob.tokenizers import SentenceTokenizer
from TextSummarization import BaseNewsArticle as bsa

"""
Heading:
रोहित शेखर तिवारी की हत्याकांड : पुलिस अधिकारी ने बताया, अपूर्वा अजीब व्यवहार कर रही हैं    

Summary:
पुलिस की हिरासत में है अपूर्वा
रोहित शेखर की हत्या का आरोप
पूछताछ कर रही है पुलिस 

Article:
पत्र में यह भी कहा गया है कि अपूर्वा को इसलिए फंसाया गया होगा क्योंकि तिवारी परिवार उसे अपनी जायदाद में कोई हिस्सा नहीं देना चाहता. सूत्रों ने बताया कि हालांकि परिवार ने दावा किया कि यह पत्र अपूर्वा के पिता की ओर से लिखा गया है जो इंदौर में जाने-माने वकील हैं और बार एसोसिएशन में ऊंचे पद पर हैं. पुलिस ने तिवारी के डिफेंस कॉलोनी आवास के लैंडलाइन नंबर की जानकारियां मांगी है. 
उन्होंने अपूर्वा के नाखून के नमूने भी लिए हैं ताकि यह पता लगाया जा सके कि क्या लड़ाई के दौरान तिवारी की त्वचा नाखूनों में फंसी थी या वहां कोई अन्य डीएनए मौजूद था. हालांकि सूत्रों ने बताया कि कोई सुराग मिलने की संभावना कम है क्योंकि नमूने हत्या के कुछ दिनों बाद लिए गए. इस मामले की पहले छानबीन करने वाली दक्षिण जिला पुलिस ने तिवारी को मृत घोषित किए जाने के बाद 16 अप्रैल को कमरा सील कर दिया था. शुरुआत में ऐसा संदेह था कि उनकी मौत स्वाभाविक कारणों से हुई, लेकिन पोस्टमार्टम में यह साफ हो गया कि उनकी तकिये से ‘‘गला घोंटकर'' हत्या की गई.  पुलिस ने बताया कि अपूर्वा देर रात करीब एक बजे तिवारी की हत्या करने के बाद कई बार कमरे में गई तो घटनास्थल के साथ छेड़छाड़ करने की संभावना बहुत अधिक है. पुलिस अधिकारी ने कहा, ‘‘उसने बेडशीट और तकियों के साथ छेड़छाड़ की कोशिश की होगी और सबूत नष्ट करने के लिए कमरा साफ करने की कोशिश की होगी.'' उनके अनुसार, अपूर्वा ने अपने हाथों से तिवारी का गला घोंटा और फिर तकिये का इस्तेमाल किया ताकि वह मदद के लिए ना चिल्ला सके. उसने करीब 14 घंटे तक तिवारी की मौत की बात छिपाए रखी. 
अपूर्वा को बुधवार को डिफेंस कॉलोनी स्थित आवास ले जाया गया जहां पुलिस ने घटना का नाटकीय रूपांतरण किया तिवारी के परिवार के सदस्यों को संदेह है कि हत्या से पहले अपूर्वा ने कथित तौर पर उसे नशा दिया. विसरा रिपोर्ट से ही यह पुष्टि हो पाएगी कि क्या उन्हें नशा दिया गया था या नहीं. बेडशीट, तकिये और तिवारी के कपड़ों को फॉरेंसिक जांच के लिए भेज दिया गया है. पुलिस ने बताया कि तिवारी को जल्दी गुस्सा आ जाता था और शादी के एक साल में ही उनके बीच मामूली मुद्दों को लेकर अक्सर झगड़ा होता था. पुलिस अधिकारी ने अपूर्वा की मनोचिकित्सा जांच की किसी भी संभावना को खारिज कर दिया.
"""


def getListOfAllStopWords():
    return list(ck.get_hindi_stop_words())


def processStopwords(baseNewsArticle: bsa.BaseNewsArticle):
    """
    :param baseNewsArticle:
    :return list: It returns a list of unique important words from the news article.
    """
    # looking for all unique stopwords that are present in our corpus
    docWordList = set(baseNewsArticle.getTextBlob().words)
    stopWordList = getListOfAllStopWords()

    if '' in docWordList:
        docWordList.remove('')
    if " " in docWordList:
        docWordList.remove(" ")

    # removing stopwords
    for word in stopWordList:
        if word in docWordList:
            docWordList.remove(word)
    # print(f'List of important words: {docWordList}')
    return docWordList

# TODO: Remove after testing


# article = """पत्र में यह भी कहा गया है कि अपूर्वा को इसलिए फंसाया गया होगा क्योंकि तिवारी परिवार
# उसे अपनी जायदाद में कोई हिस्सा नहीं देना चाहता. सूत्रों ने बताया कि हालांकि परिवार ने दावा किया
# कि यह पत्र अपूर्वा के पिता की ओर से लिखा गया है जो इंदौर में जाने-माने वकील हैं और बार एसोसिएशन
# में ऊंचे पद पर हैं. पुलिस ने तिवारी के डिफेंस कॉलोनी आवास के लैंडलाइन नंबर की जानकारियां मांगी
# है.  उन्होंने अपूर्वा के नाखून के नमूने भी लिए हैं ताकि यह पता लगाया जा सके कि क्या लड़ाई के
# दौरान तिवारी की त्वचा नाखूनों में फंसी थी या वहां कोई अन्य डीएनए मौजूद था. हालांकि सूत्रों ने
# बताया कि कोई सुराग मिलने की संभावना कम है क्योंकि नमूने हत्या के कुछ दिनों बाद लिए गए. इस मामले
# की पहले छानबीन करने वाली दक्षिण जिला पुलिस ने तिवारी को मृत घोषित किए जाने के बाद 16 अप्रैल को
# कमरा सील कर दिया था. शुरुआत में ऐसा संदेह था कि उनकी मौत स्वाभाविक कारणों से हुई,
# लेकिन पोस्टमार्टम में यह साफ हो गया कि उनकी तकिये से ‘‘गला घोंटकर'' हत्या की गई.  पुलिस ने बताया
# कि अपूर्वा देर रात करीब एक बजे तिवारी की हत्या करने के बाद कई बार कमरे में गई तो घटनास्थल के साथ
# छेड़छाड़ करने की संभावना बहुत अधिक है. पुलिस अधिकारी ने कहा, ‘‘उसने बेडशीट और तकियों के साथ
# छेड़छाड़ की कोशिश की होगी और सबूत नष्ट करने के लिए कमरा साफ करने की कोशिश की होगी.'' उनके अनुसार,
# अपूर्वा ने अपने हाथों से तिवारी का गला घोंटा और फिर तकिये का इस्तेमाल किया ताकि वह मदद के लिए ना
# चिल्ला सके. उसने करीब 14 घंटे तक तिवारी की मौत की बात छिपाए रखी.  अपूर्वा को बुधवार को डिफेंस
# कॉलोनी स्थित आवास ले जाया गया जहां पुलिस ने घटना का नाटकीय रूपांतरण किया तिवारी के परिवार के
# सदस्यों को संदेह है कि हत्या से पहले अपूर्वा ने कथित तौर पर उसे नशा दिया. विसरा रिपोर्ट से ही यह
# पुष्टि हो पाएगी कि क्या उन्हें नशा दिया गया था या नहीं. बेडशीट, तकिये और तिवारी के कपड़ों को
# फॉरेंसिक जांच के लिए भेज दिया गया है. पुलिस ने बताया कि तिवारी को जल्दी गुस्सा आ जाता था और शादी
# के एक साल में ही उनके बीच मामूली मुद्दों को लेकर अक्सर झगड़ा होता था. पुलिस अधिकारी ने अपूर्वा की
# मनोचिकित्सा जांच की किसी भी संभावना को खारिज कर दिया. """
#
# print(processStopwords(bsa.BaseNewsArticle(article)))
