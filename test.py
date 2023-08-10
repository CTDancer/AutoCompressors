from transformers import AutoTokenizer
from auto_compressor import AutoCompressorModel
import pdb

# Load a model pre-trained on 6k tokens in 4 compression steps
tokenizer = AutoTokenizer.from_pretrained("princeton-nlp/AutoCompressor-2.7b-6k")
model = AutoCompressorModel.from_pretrained("princeton-nlp/AutoCompressor-2.7b-6k").eval()

pdb.set_trace()
prompt = 'The first name of the current US president is "'
prompt_tokens = tokenizer(prompt, return_tensors="pt").input_ids

context = """Joe Biden, born in Scranton, Pennsylvania, on November 20, 1942, had a modest upbringing in a middle-class family. He attended the University of Delaware, where he double-majored in history and political science, graduating in 1965. Afterward, he earned his law degree from Syracuse University College of Law in 1968.\nBiden's early political career began in 1970 when he was elected to the New Castle County Council in Delaware. In 1972, tragedy struck when his wife Neilia and 1-year-old daughter Naomi were killed in a car accident, and his two sons, Beau and Hunter, were injured. Despite this devastating loss, Biden chose to honor his commitment and was sworn in as a senator by his sons' hospital bedsides.\nHe went on to serve as the United States Senator from Delaware for six terms, from 1973 to 2009. During his time in the Senate, Biden was involved in various committees and was particularly known for his expertise in foreign affairs, serving as the chairman of the Senate Foreign Relations Committee on multiple occasions.\nIn 2008, Joe Biden was selected as the running mate for Barack Obama, who went on to win the presidential election. As Vice President, Biden played an integral role in the Obama administration, helping to shape policies and handling issues such as economic recovery, foreign relations, and the implementation of the Affordable Care Act (ACA), commonly known as Obamacare.\nAfter completing two terms as Vice President, Joe Biden decided to run for the presidency in 2020. He secured the Democratic nomination and faced the incumbent President Donald Trump in the general election. Biden campaigned on a platform of unity, promising to heal the divisions in the country and tackle pressing issues, including the COVID-19 pandemic, climate change, racial justice, and economic inequality.\nIn the November 2020 election, Biden emerged victorious, and on January 20, 2021, he was inaugurated as the 46th President of the United States. At the age of 78, Biden became the oldest person to assume the presidency in American history.\nAs President, Joe Biden has worked to implement his agenda, focusing on various initiatives, such as infrastructure investment, climate action, immigration reform, and expanding access to healthcare. He has emphasized the importance of diplomacy in international relations and has sought to rebuild alliances with global partners.\nThroughout his long career in public service, Joe Biden has been recognized for his commitment to bipartisanship, empathy, and his dedication to working-class issues. He continues to navigate the challenges facing the nation, striving to bring the country together and create positive change for all Americans."""

context_tokens = tokenizer(context, return_tensors="pt").input_ids
summary_vectors = model(context_tokens, output_softprompt=True).softprompt
print(f"Compressing {context_tokens.size(1)} tokens to {summary_vectors.size(1)} summary vectors")
# >>> Compressing 535 tokens to 50 summary vectors

next_token = model(prompt_tokens, softprompt=summary_vectors).logits[0,-1].argmax()
print("Next token w/ summary vectors:\n" + prompt + tokenizer.decode(next_token))
# >>> Next token w/ summary vectors:
# >>> The first name of the current US president is "Joe

next_token_without_context = model(prompt_tokens).logits[0,-1].argmax()
print("Next token w/o context:\n" + prompt + tokenizer.decode(next_token_without_context))
# >>> Next token w/o context:
# >>> The first name of the current US president is "Bar