# Frames

Frames are Gogh's built-in functions.

Symbol|Arity|Function|Note
------|-----|--------|----
` `|0|No-op
`¤`|0|Empty the stack.
`¦`|0|Swap the top two stack elements.|Needs at least 2 elements on the stack.
`©`|0,1|Copy the `n`th-from-top stack element.|Needs at least `n` elements on the stack. `n` defaults to `0`.
`®`|0|Rotate the top 3 stack elements leftward.|Needs at least 3 elemets on the stack.
`×`|0|Discard the top stack element.|Needs at least 1 element on the stack.
`÷`|0|Duplicate the top stack element.|Needs at least 1 element on the stack.
`«`|0,1|Rotate the stack `n` elements leftward.|`n` defaults to 1.
`»`|0,1|Rotate the stack `n` elements rightward.|`n` defaults to 1.