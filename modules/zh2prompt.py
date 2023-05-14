import requests, json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class BaiduTrans:
    def __init__(self):
        self.token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=eObEtaf2mBHg4x4RqGOHOWXT&client_secret=HbA9TmhykS2PtnpaMSHsmKcccXSvOhb3'
        self.trans_url = 'https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token='

    def get_token(self):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = requests.request("POST", self.token_url, headers=headers, data='')
        return json.loads(response.text)['access_token']

    def trans(self, text):
        r = requests.post(self.trans_url + self.get_token(),
                          params={'q': text, 'from': 'zh', 'to': 'en', 'termIds': ''},
                          headers={'Content-Type': 'application/json'})
        return r.json()['result']['trans_result'][0]['dst']

class MagicPrompt:
    def __init__(self):
        tokenizer = AutoTokenizer.from_pretrained("Gustavosta/MagicPrompt-Stable-Diffusion")
        model = AutoModelForCausalLM.from_pretrained("Gustavosta/MagicPrompt-Stable-Diffusion")
        self.magic_prompt = pipeline("text-generation", model=model, tokenizer=tokenizer)

    def gen_prompt(self, input):
        return self.magic_prompt(input)[0]['generated_text']

tanslater = BaiduTrans()
magic_prompt = MagicPrompt()
def zh2prompt_gen(zh_input):
    if not zh_input.strip():
        return ''
    en_input = tanslater.trans(zh_input)
    prompt = magic_prompt.gen_prompt(en_input)
    return prompt