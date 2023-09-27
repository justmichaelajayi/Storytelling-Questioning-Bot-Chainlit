import chainlit as cl
import openai
import os

def get_gpt_output(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "you are an writer that is obsessed with storytelling and will never stop talking about them"},
            {"role": "user", "content": user_message}
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )

    return response


@cl.on_message
async def main(message: str):
    await cl.Message(content=f"{get_gpt_output(message)['choices'][0]['message']['content']}",).send()
