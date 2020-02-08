from collections import Counter
from TextSummarization.ProcessStopwords import processStopwords
from TextSummarization.BaseNewsArticle import BaseNewsArticle
from TextSummarization.Utils import convertListToString
from textblob import TextBlob


class ProcessSentences:

    def __init__(self, newsArticle: BaseNewsArticle):
        self.newsArticle = newsArticle

    def getTokenizedSentences(self):
        if self.newsArticle.article == "":
            return

        textBlob = self.newsArticle.getTextBlob()
        # print(f"\nTotal Number of words in article: {len(list(textBlob.words))}\n")
        sentences = list()
        for sentence in textBlob.sentences:
            sentences.append(str(sentence))

        return sentences

    def calculateTermFrequency(self):
        if self.newsArticle.getArticle() == "":
            print("No Article from calculateTermFrequency")
            return

        termCounterDictionary = dict()
        termFrequencyDictionary = dict()
        sentences = self.getTokenizedSentences()
        docWordList = processStopwords(self.newsArticle)
        # print(f'\nList of important words: {docWordList}\n')
        # print(f'\nTotal number of important words: {len(docWordList)}\n')
        for word in docWordList:
            for sentence in sentences:
                if word in sentence:
                    if word in termCounterDictionary:
                        termCounterDictionary[word] = termCounterDictionary[word] + 1
                    else:
                        termCounterDictionary[word] = 1

                    termFrequencyDictionary[word] = \
                        termCounterDictionary[word] / len(self.newsArticle.getArticle())

        return termFrequencyDictionary

    # TODO
    def checkDate(self):
        pass

    """IDF refers to inverse document frequency and can be calculated as follows:

    IDF: 
    (Total number of sentences (documents)) / (Number of sentences (documents) containing the word)
    """

    def calculateInverseDocumentFrequency(self):
        wordInSentenceDictionary = {}
        inverseDocumentFrequencyDictionary = {}
        wordList = processStopwords(self.newsArticle)
        sentences = self.getTokenizedSentences()
        # print(f'\nWords: {wordList}')
        # print(f'\n Sentences: {sentences}')
        for word in wordList:
            for sentence in sentences:
                try:
                    if word in sentence:
                        if word in wordInSentenceDictionary:
                            wordInSentenceDictionary[word] += 1
                        else:
                            wordInSentenceDictionary[word] = 1

                    inverseDocumentFrequencyDictionary[word] = \
                        len(sentences) / wordInSentenceDictionary[word]

                except KeyError:
                    if word in wordInSentenceDictionary:
                        wordInSentenceDictionary.pop(word)
                    if word in inverseDocumentFrequencyDictionary:
                        inverseDocumentFrequencyDictionary.pop(word)

        return inverseDocumentFrequencyDictionary

    def calculateTermUniqueness(self):
        # print("Word Frequency counter Triggered")
        wordCounter = Counter(self.newsArticle.getTextBlob().words)
        return wordCounter

    def scoreSentences(self) -> dict:
        freqTable = Counter(processStopwords(self.newsArticle))
        sentences = self.getTokenizedSentences()
        sentenceValue = dict()

        for sentence in sentences:
            textBlob = TextBlob(sentence)
            word_count_in_sentence = len(textBlob.words)  # (len(word_tokenize(sentence)))
            # print(f'word count in sentence: {word_count_in_sentence}')
            for wordValue in freqTable:
                if wordValue in sentence.lower():
                    if sentence[:10] in sentenceValue:
                        sentenceValue[sentence[:10]] += freqTable[wordValue]
                    else:
                        sentenceValue[sentence[:10]] = freqTable[wordValue]

            sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] // word_count_in_sentence

        return sentenceValue

    def findAverageScore(self) -> int:
        sentenceValue = self.scoreSentences()
        # print(f'ScoreSentences: {sentenceValue}')
        sumValues = 0
        for entry in sentenceValue:
            sumValues += sentenceValue[entry]
            # print(f' sumValues: {sumValues}\tentry {entry}')
        # Average value of a sentence from original text
        average = int(sumValues / len(sentenceValue))

        return average

    """
    Step 1: Create word frequency table.
    Step 2: Tokenize Sentences
    Step 3: Score the sentences: Term frequency
            We’re using the Term Frequency method to score each sentence.
            Basic Algorithm: score a sentence by its words, adding the frequency of every non-stop 
            word in a sentence.
            Notice that a potential issue with our score algorithm is that long sentences will have 
            an advantage over short sentences.
            To solve this, we’re dividing every sentence score by the number of words in 
            the sentence.
            Note that here sentence[:10] is the first 10 character of any sentence, this is to save 
            memory overhead while saving keys of the dictionary. The dictionary would look something 
            like below.
    Step 4: Find the threshold
    Step 5: Generate Summary
            Basic Algorithm: Select a sentence for a summarization, If the sentence score is more 
            than the average score.
     """
    def generate_summary(self, value=1.5) -> str:
        sentences = self.getTokenizedSentences()
        # print(f'Sentences: {sentences}')
        sentenceValue = self.scoreSentences()
        threshold = self.findAverageScore() * value  # value = 1.5(default), 1.3 and 1.8
        print(f'SentenceValue: {sentenceValue}')
        print(f'Threshold: {threshold}')
        print(f'Average: {self.findAverageScore()}')
        sentence_count = 0
        summary = ''

        for sentence in sentences:
            if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > threshold:
                summary += " " + sentence
                sentence_count += 1

        return summary

#
# hindi_text = """देखने गए लोगों का फ़िल्म देखने के बाद इस कहावत से राब्ता हो सकता है. बाहुबली
# फ़िल्म के बाद अभिनेता प्रभास की धमाकेदार एंट्री की उम्मीद लेते हुए जब हम 'साहो' देखने पहुंचे तो
# केवल मायूसी ही हाथ लगी. ये फ़िल्म चार भाषाओं में एक साथ रिलीज़ हुई है. ज़ाहिर है प्रभास के इतने
# फैन्स हैं कि हर शहर में लोगों ने पहले ही इस फ़िल्म की बुकिंग करा रखी थी. 'बाहुबली' के बाद कुछ
# लोगों को इंतज़ार था कि इतने बड़े पैमाने की फ़िल्म के बाद ये फ़िल्म भी बॉक्स ऑफिस पर खरी उतरेगी.
# ऐसा नहीं है कि फ़िल्म में वैसा मसाला नहीं है जो इस तरह की फ़िल्म में होना चाहिए. फ़िल्म में साथी
# कलाकार के रूप में जैकी श्रॉफ, टीनू आनंद, चंकी पांडे, मंदिरा बेदी, अरुण विजय, प्रकाश बेलावाडी जैसे
# कई मंझे हुए कलाकार हैं. पर उनके पास फ़िल्म में कुछ ख़ास करने के लिए नहीं है. एक तरह से देखा जाए
# तो ये सब केवल कुछ पात्रों को भरने के लिए ही रखे गए हैं. फ़िल्म एक काल्पनिक शहर वाजीपुर से शुरू
# होती है. जहां पर जैकी श्रॉफ रॉय नाम का अंपायर चलाते हैं. वो काला धंधा करते हैं और उनकी शाखाएं
# देश-विदेश में फैली हुई हैं. पर कुछ इज़्जत कमाने के लिए वो स्टील की एक फैक्ट्री लगाना चाहते हैं
# जिसके लिए उनको कुछ राजनीतिज्ञों की मदद की ज़रूरत पड़ती है. उनके दल के कुछ सदस्य ऐसे हैं जो उनसे
# बदला लेना चाहते हैं. इस रंजिश में जैकी श्रॉफ की हत्या हो जाती है. इसके बाद कहानी कई देशों में
# घूमती है. जहां चीन, अफ्रीका और कुछ भारत के लोग भी शामिल हैं. दूसरी ओर बंबई में कुछ पुलिस अफसर हैं
# जो रॉय अंपायर के फैले धंधे से परेशान हैं. इनमें शामिल हैं मुरली, श्रद्धा कपूर और प्रभास. जब
# प्रभास ठान लेते हैं कि वो रॉय अंपायर का खात्मा कर देंगे तब शुरू होती है लड़ाई पुलिस और अंडरवर्ल्ड
# की. रॉय अंपायर एक ब्लैकबॉक्स की तलाश में होता है जिसके खुलने से उनके हाथ बहुत-सी पूंजी लगेगी.
# लेकिन इस ब्लैकबॉक्स के बारे में पुलिस को पहले से ही पता होता है. प्रभास: मैं हिन्दी में लिखता और
# पढ़ता हूँ विद्या बालन ने क्यों कहा- वो ख़ुद को धार्मिक नहीं बताना चाहतीं इसके बाद फ़िल्म की कहानी
# रुक जाती है और चूहे-बिल्ली के खेल की तरह पुलिस और अंडरवर्ल्ड के बीच तनाव शुरू हो जाता है. इसके
# अलावा प्लॉट के नाम पर फ़िल्म शून्य है. हालांकि फ़िल्म की गति तो तेज़ हो जाती है लेकिन उस दौरान हम
# सिर्फ़ तमाम गाड़ियां उड़ते हुए देखते हैं और बहुत तेज़ एक्शन के चलते कुछ किरदारों को आते-जाते
# देखते हैं. इसी बीच फ़िल्म में दो-तीन गाने और नाच ठूंसा गया है. ज़ाहिर है कि प्रभास के साथ श्रद्धा
# कपूर का रोमांस फिल्म में जोड़ना ज़रूरी था. इसी दौरान हमें नील नितिन मुकेश भी नज़र आते हैं जिनको
# लेकर ये संशय बना रहता है कि वो पुलिस के आदमी हैं या अंडरवर्ल्ड के. प्रभास पूरी फ़िल्म में छाए
# रहते हैं और कुछ सस्पेंस रखते हुए हमें ये भी नहीं पता चल पाता कि वो पुलिस में हैं भी या नहीं. ऐसे
# कई सीन हैं जहां डायलॉग की कमी खलती है. शायद उनकी हिंदी इतनी अच्छी नहीं है इसी वजह से वो एक्शन
# करते हुए ज़्यादा नज़र आते हैं. फ़िल्म में सीजीआई (कंप्यूटर जेनरेटेड इमेज़री) के ज़रिए कुछ रोमांच
# से भरे दृश्य ज़रूर हैं जो वास्तविकता से बहुत दूर हैं और केवल दर्शकों को खुश करने के लिए रखे गए
# हैं. तकनीकी दृष्टि से देखा जाए तो ये सीन किसी भी हॉलीवुड फ़िल्म की टक्कर के हैं. कमी है तो सिर्फ़
# एक कहानी की. क्योंकि केवल एक्शन के बल पर तीन घंटे फ़िल्म को झेलना मुश्किल हो जाता है. प्रभास को
# एक लोकप्रिय बॉलीवुड निर्देशक की फ़िल्म से शुरुआत करनी चाहिए थी. लेकिन शायद बाहुबली का प्रभाव इतना
# अधिक है कि वो उसी में अपने आप को ढाले हुए हैं. कुछ सलमान और अक्षय कुमार की फ़िल्मों का भी असर
# होगा. इसके अलावा उत्तर भारत में अपना रंग जमाने के उद्देश्य से ही उन्होंने ऐसी फ़िल्म का चयन किया
# है जिसमें केवल उनके सिक्स पैक्स एब्स, एक लाइन की कहानी, तीन गाने और बहुत सारा एक्शन ही फ़िल्म में
# मौजूद है. फ़िल्म देखने के बाद बस एक ही बात दिल से निकलती है कि काश फ़िल्म में एक प्लॉट भी होता. """
#
# """generated Summary:
#
# पर उनके पास फ़िल्म में कुछ ख़ास करने के लिए नहीं है. फ़िल्म एक काल्पनिक शहर वाजीपुर से शुरू
# होती है. जहां पर जैकी श्रॉफ रॉय नाम का अंपायर चलाते हैं. वो काला धंधा करते हैं और उनकी शाखाएं
# देश-विदेश में फैली हुई हैं. इसके बाद कहानी कई देशों में
# घूमती है. जहां चीन, अफ्रीका और कुछ भारत के लोग भी शामिल हैं. इनमें शामिल हैं मुरली, श्रद्धा कपूर और प्रभास. लेकिन इस ब्लैकबॉक्स के बारे में पुलिस को पहले से ही पता होता है. इसके
# अलावा प्लॉट के नाम पर फ़िल्म शून्य है. इसी बीच फ़िल्म में दो-तीन गाने और नाच ठूंसा गया है. ऐसे
# कई सीन हैं जहां डायलॉग की कमी खलती है. तकनीकी दृष्टि से देखा जाए तो ये सीन किसी भी हॉलीवुड फ़िल्म की टक्कर के हैं. कमी है तो सिर्फ़
# एक कहानी की.
# """
#
# """Multilangsummary
#
# ज़ाहिर है प्रभास के इतने फैन्स हैं कि हर शहर में लोगों ने पहले ही इस फ़िल्म की
# पर उनके पास फ़िल्म में कुछ
# एक तरह से देखा जाए तो ये सब केवल कुछ पात्रों को भरने के लिए ही रखे गए
# जहां चीन, अफ्रीका और कुछ भारत के लोग भी शामिल हैं.
# दूसरी ओर बंबई में कुछ पुलिस अफसर हैं जो रॉय अंपायर के फैले धंधे से परेशान हैं.
# जब प्रभास ठान लेते हैं कि वो रॉय अंपायर का खात्मा कर देंगे तब शुरू
# चाहतीं इसके बाद फ़िल्म की कहानी रुक जाती है और चूहे-बिल्ली के खेल की तरह पुलिस और अंडरवर्ल्ड के
# तेज़ हो जाती है लेकिन उस दौरान हम सिर्फ़ तमाम गाड़ियां उड़ते हुए देखते हैं और बहुत तेज़ एक्शन के
# इसी बीच फ़िल्म में दो-तीन गाने और नाच ठूंसा गया है.
# प्रभास पूरी फ़िल्म में छाए रहते हैं और कुछ सस्पेंस रखते हुए हमें ये भी नहीं पता चल पाता कि वो
# पुलिस में हैं भी या नहीं.
# नहीं है इसी वजह से वो एक्शन करते हुए ज़्यादा नज़र आते हैं.
# लेकिन शायद बाहुबली का प्रभाव इतना अधिक है कि वो उसी में अपने आप को ढाले हुए हैं.
# तीन गाने और बहुत सारा एक्शन ही फ़िल्म में मौजूद है.
#
# """
#
#
# ps = ProcessSentences(BaseNewsArticle(hindi_text))
# # print(ps.calculateTermFrequency())
# # print(ps.calculateInverseDocumentFrequency())
# # print(f'Word Counter: {ps.calculateTermUniqueness()}')
# print(f'Print Article: \n{ps.newsArticle.getArticle()}\n\n')
# print(f'Total number of words: {len(ps.newsArticle.getTextBlob().words)}')
# values = [1.2, 1.3, 1.5, 1.8, 2]
# for i in values:
#     generated_summary = ps.generate_summary(i)
#     print(f'\nSummary with value({i}) and length({len(generated_summary)}): {generated_summary}')
#
# multi_lang_summary = """ज़ाहिर है प्रभास के इतने फैन्स हैं कि हर शहर में लोगों ने पहले ही इस फ़िल्म की
# पर उनके पास फ़िल्म में कुछ
# एक तरह से देखा जाए तो ये सब केवल कुछ पात्रों को भरने के लिए ही रखे गए
# जहां चीन, अफ्रीका और कुछ भारत के लोग भी शामिल हैं.
# दूसरी ओर बंबई में कुछ पुलिस अफसर हैं जो रॉय अंपायर के फैले धंधे से परेशान हैं.
# जब प्रभास ठान लेते हैं कि वो रॉय अंपायर का खात्मा कर देंगे तब शुरू
# चाहतीं इसके बाद फ़िल्म की कहानी रुक जाती है और चूहे-बिल्ली के खेल की तरह पुलिस और अंडरवर्ल्ड के
# तेज़ हो जाती है लेकिन उस दौरान हम सिर्फ़ तमाम गाड़ियां उड़ते हुए देखते हैं और बहुत तेज़ एक्शन के
# इसी बीच फ़िल्म में दो-तीन गाने और नाच ठूंसा गया है.
# प्रभास पूरी फ़िल्म में छाए रहते हैं और कुछ सस्पेंस रखते हुए हमें ये भी नहीं पता चल पाता कि वो
# पुलिस में हैं भी या नहीं.
# नहीं है इसी वजह से वो एक्शन करते हुए ज़्यादा नज़र आते हैं.
# लेकिन शायद बाहुबली का प्रभाव इतना अधिक है कि वो उसी में अपने आप को ढाले हुए हैं.
# तीन गाने और बहुत सारा एक्शन ही फ़िल्म में मौजूद है."""
#
# # print(f"Generated Summary length: {len(generated_summary)}")
# print(f"\n\nMultiLangSummary Summary length({len(multi_lang_summary)}): {multi_lang_summary}")
#
