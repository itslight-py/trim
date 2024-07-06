"""Trimmer."""

from typing import List

import tiktoken


enc = tiktoken.get_encoding("cl100k_base")


def get_tokens(text: str) -> List[int]:
    return enc.encode(text)


def tokens_to_text(tokens: List[int]) -> str:
    return enc.decode(tokens)


def trim(
    conversation: List[dict], *, max_tokens: int = 7000, preserve_ratio: float = 0.75
):
    boundary = int(max_tokens * preserve_ratio)
    past_tokens = []

    for message in conversation:
        tokens = get_tokens(message["content"])
        past_tokens.append(len(tokens))

    while sum(past_tokens) > boundary:
        # print("out of boundary at", sum(past_tokens), "index is unknown")
        # print(
        #     "getting the first conversation token from past_tokens, there are",
        #     past_tokens[0],
        #     "tokens",
        # )
        if sum(past_tokens) - past_tokens[0] > boundary:
            # print(
            #    "even if i remove the first token count, still out of boundary (would be %i)"
            #    % (sum(past_tokens) - past_tokens[0])
            #)
            # print("therefore im going to remove it")
            conversation.pop(0)
            past_tokens.pop(0)

        elif sum(past_tokens) - past_tokens[0] == boundary:
            # print(
            #    "if i remove the first token count, then it is exactly equal to the boundary"
            #)
            conversation.pop(0)
            past_tokens.pop(0)
            # print("im returning it!")
            break

        elif sum(past_tokens) - past_tokens[0] < boundary:
            # print(
            #    "if i remove the first token count, itd be less than the boundary (itd be %i)"
            #    % (sum(past_tokens) - past_tokens[0])
            #)
            # print("therefore im going to trim it (%i)" % (sum(past_tokens) - boundary))
            # - boundary - sum(past_tokens)
            new_tokens = get_tokens(conversation[0]["content"])[
                sum(past_tokens) - boundary :
            ]

            conversation[0].update({"content": tokens_to_text(new_tokens)})
            past_tokens[0] = len(new_tokens)

            break

        # print()

    return conversation


def count_tokens(messages: List[dict]):
    tokens = 0
    for message in messages:
        tokens += len(get_tokens(message["content"]))

    return tokens

