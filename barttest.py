from transformers import BartForConditionalGeneration, BartTokenizer
import torch

model_name = "facebook/bart-large-cnn"

# Carrega modelo e tokenizer
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name).to("cuda")

# Texto de entrada (pode ser um .txt lido com open())
texto = """
E nÒo precisa fazer um circuito muito grande E Y e Z A gente jß tinha feito ali E esses dois aqui? Ah, por isso que vocÛ nÒo tinha no desenho NÒo tinha? Mas a gente sabe, por exemplo, a saÝda ali o n¾r? o n¾r Olha, vou fazer aqui Abre 01, 01 001 Se fosse o n¾r Seria 01, 01 Seria 01, 01 Na hora que inverto Ou seja, que eu nego a saÝda tem o quÛ? 00, 00 nesse caso Nesse caso essa primeira abraþÒo De S A mais B ? Mas tem outro jeito nenhum Vamos fazer a segunda graþa A e B 01, 01 001 Se eu fosse fazer um AND Daria 00, 01 00, 01 00, 01 X e O E o AND 11, 01 0 Isso aqui 1S Igual a A, B E B E A tambÚm E como que a gente consegue chegar nesse resultado aqui tambÚm? Eu quero chegar ali em 1, 00, 00 Se eu tiver isso aqui Eu consigo ter essa saÝda NÒo sei eu vocÛ nega E para dar 0 E para os outros Tem que ser 0,00 tem que ser 0,00 Se eu jß comecei com 01 Uma grande chance de ser isso aqui, nÒo ? NÒo ? S¾ que daÝ obviamente Eu tenho A e B negado Ou seja, eu tenho a negaþÒo da entrada NÒo isso? O que na verdade comprova o que vocÛ tinha perguntado agora a pouco A negaþÒo da saÝda diferente Do que ter as negaþ§es das varißveis de entrada E realizar operaþÒo justamente aqui Eu coloquei essa primeira para mostrar para vocÛs que a gente tem vßrias opþ§es Para chegar na mesma saÝda eu tenho as equaþ§es equivalentes E aqui justamente, aproveitando o fato de Mostrar que uma coisa nÒo igual a outra Meninas O nosso As nossas bombinhas aqui A nossa caixa de ßgua jß tinha feito em cima passada, ? E na semana retrasada A gente viu que a bombinha Enchendo, ? O sensor para encher a bomba O sensor para encher a caixa Enchendo, toda a coisa na hora toda na final da hist¾ria n¾s temos isso aqui NÒo ? Suscensores nÒo nacionais Vamos lß Ligar a bomba 1 e ligar a bomba 2 para ligar a bomba 1 e 2 Eu tenho que vir aqui e Eu pego a aqui a 0 Pego b aqui a 0 E tem uma saÝda da bomba 1, ? Na segunda linha eu tambÚm tenho uma situaþÒo que a bomba nÒo liga, nÒo tem? S¾ a bomba 1, bomba 2 nÒo liga na segunda linha Na bomba, na linha 2 Na linha 2 eu tenho a 1 E b2 E b0 A 1 E b0 Mais uma saÝda, s¾ que eu nÒo posso ter duas saÝdas Para a mesma coisa eu junto as duas, considerando que ela vai ligar Ou numa situaþÒo ou na outra Ë, como aqui tem a saÝda bomba 1 ? com esse eu ligo a bomba E tem que lembrar aqui Que a representa 1 E a negado representa 0 ? A gente sabe que Em 0 nada liga, ? por isso que Essa linha da negaþÒo VocÛ tem uma inversora aqui E aÝ a pergunta que eu mais ouþo Em sa·ra tambÚm sempre foi, professor E quando a bomba estß desligada? NÒo, quando a bomba estß desligada ela estß desligada A gente representa aqui quando a bomba liga Entendeu? Quando estß desligada Ligou tudo, parou tudo Vou representar que ela estß desligada Vou representar o modo que o A, liga Quando a saÝda em estado l¾gico Alto Que daÝ como a gente tem aqui a entrada 00 A gente tambÚm tem a tal da VAR negada E quando a gente tem 1 e 1 A gente tem VAR direto daÝ bom? E a bomba 2 A bomba 2 vai ligar na mesma situaþÒo Da bomba 1 Quando A 0 e B 0 Que mais que a gente podia representar aqui? Lembra que eu mostrei pra vocÛs? O erro O.
"""

# Tokeniza o texto
inputs = tokenizer([texto], max_length=1024, return_tensors="pt", truncation=True).to("cuda")

# Gera o resumo
summary_ids = model.generate(inputs["input_ids"], max_length=200, min_length=60, length_penalty=2.0, num_beams=4, early_stopping=True)

# Decodifica o resultado
resumo = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print("\nResumo gerado:\n", resumo)
