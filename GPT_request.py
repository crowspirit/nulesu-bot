import openai


openai.api_key = "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"

def request(prompt):
    model = "text-davinci-003"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return (response.choices[0].text)