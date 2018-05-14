# You Already Know, web

## Problem

Stop overthinking it, you already know the answer here.

You already have the flag.

**Seriously**, _if you can read this_, then you have the flag.

Submit it!

## Solution

Every popup you open from the main page of the competition (https://scoreboard.oooverflow.io) is in fact an AJAX request of the form `https://h54exijeu1.execute-api.us-east-2.amazonaws.com/prod/challenge/youalreadyknow/YOUR_TOKEN` where `YOUR_TOKEN` comes from `localStorage.token`.

Response is a JSON that contains markdown in a field called message, which I suspect is then rendered to the page with some markdown-to-html library, but that does not matter much.

The response looks like

```json
{
  "success": true, 
  "message": "Stop overthinking it, you already know the answer here.\n\n[comment]: <> (OOO{Sometimes, the answer is just staring you in the face. We have all been there})\n\nYou already have the flag.\n\n**Seriously**, _if you can read this_, then you have the flag.\n\nSubmit it!\n"
}
```


**Flag: OOO{Sometimes, the answer is just staring you in the face. We have all been there}**



