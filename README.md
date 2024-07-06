# trim
Trims LLM instance messages.

```haskell
$ itslight i trim
```

## Usage
```python
from its.trim import trim, count_tokens

messages = [
    {
        "role": "user",
        "content": "How can you assist me today?"
    }
]

count_tokens(messages)
trim(
    messages,
    max_tokens=7000,
    preserve_ratio=0.75
)
```
