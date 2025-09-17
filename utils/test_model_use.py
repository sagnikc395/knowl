from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# loading model and tokenizer
model_name = "microsoft/DialoGPT-medium"  # or local path
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

## generate response
def generate_response(prompt, max_length=100):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response[len(prompt):].strip()

# useage
# only taking the first 100 characters to reduce waste
prompt = input("> ")
print = generate_response(prompt)
print(response)
