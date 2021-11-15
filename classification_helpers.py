import pickle
from transformers import DistilBertTokenizer, TFDistilBertForSequenceClassification
import numpy as np


def softmax(outputs):
    maxes = np.max(outputs, axis=-1, keepdims=True)
    shifted_exp = np.exp(outputs - maxes)
    return shifted_exp / shifted_exp.sum(axis=-1, keepdims=True)


def load_label_encoder(dir_path):
      with open(dir_path + '/label_encoder.pickle', 'rb') as f:
        return pickle.load(f)


def make_classify():
  model_path = 'models/iva_distilber_v5_tf'
  tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
  model = TFDistilBertForSequenceClassification.from_pretrained(model_path)
  encoder = load_label_encoder(model_path)
  
  def classify(utterance):
    tokenized_sentence = tokenizer(
      utterance, 
      add_special_tokens = True,
      max_length = 64,
      padding='max_length',
      return_attention_mask = True,
      return_tensors = 'tf'
    )
    predictions = model(**tokenized_sentence).logits.numpy().flatten()
    softmaxed_predictions = softmax(predictions)
    return {
      intent: confidence.item() for intent, confidence in zip(encoder.categories_[0], softmaxed_predictions)
    }

  return classify
