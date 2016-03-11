# Frames

Frames are Gogh's built-in functions.

Symbol|Arity|Function|Note
------|-----|--------|----
` `|0|No-op
`¤`|0|Empty the stack.
`¦`|0|Swap the top two stack elements.|Needs at least 2 elements on the stack.
`©`|1|Copy the `n`th-from-top stack element.|Needs at least `n` elements on the stack. `n` defaults to `0`.
`®`|0|Rotate the top 3 stack elements leftward.|Needs at least 3 elemets on the stack.
`×`|0|Discard the top stack element.|Needs at least 1 element on the stack.
`÷`|0|Duplicate the top stack element.|Needs at least 1 element on the stack.
`«`|1|Rotate the stack `n` elements leftward.|`n` defaults to 1.
`»`|1|Rotate the stack `n` elements rightward.|`n` defaults to 1.
`s`|0|Convert the top stack element to a string.|Needs at least 1 element on the stack.
`n`|0|Convert the top stack element to a number.|Needs at least 1 element on the stack. Distinction between decimal and integer is made internally.
`a`|0|Convert the top stack element to an array.|Needs at least 1 element on the stack.
