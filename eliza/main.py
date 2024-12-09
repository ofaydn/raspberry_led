import nltk
from nltk.chat.util import Chat, reflections

pairs = [
    [
        r"Merhaba(.*)",
        ["Merhaba! Nasılsınız?",]
    ],
    [
        r"(.*)Nasılsın(.*)",
        ["İyiyim, teşekkürler! Siz nasılsınız?",]
    ],
    [
        r"(.*) (mutlu|üzgün|kızgın|heyecanlı)(.*)",
        ["Neden %2 hissediyorsunuz?",]
    ],
    [
        r"Çıkış",
        ["Görüşmek üzere!"]
    ],
]

def eliza_chat():
    print("Merhaba! Ben ELIZA. Çıkmak için 'Çıkış' yazın.")
    chat = Chat(pairs, reflections)
    chat.converse()

if __name__ == "__main__":
    eliza_chat()
