# Git - misc

## Problem

My file lost!

attachment: https://drive.google.com/open?id=1Mo3uN2FV1J-lbqjQZvvXitWagZqjD1Xi

Inside there is a zip file with the following contents

```
.git
HelloWorld.txt
```

Hello World is empty. `git log` shows that the repo only has the initial commit.

## Tools used

- `strings`

## Solution

Part of my initial checklist is running strings on everything, just to see interesting stuff. It's a mindless part of every challenge.

Run:

```bash
find . -type f -exec strings {} \; > ../result.txt
cat ../result.txt
```

Looking through it, this line caught my eye

```
22d3349a5c6fe45758daba276108137382a01caa f4d0f6ddf6660f5c9273c84f3de64840a407bef1 zsx <zsx@zsxsoft.com> 1526187319 +0800	commit: Flag
```

Not really sure what each of the two commit hashes mean, but I assume one is the commit blob and the other one is the parent. Checking them both.

```bash
git checkout f4d0f6ddf6660f5c9273c84f3de64840a407bef1
ls
cat flag.txt
```

**Flag: RCTF{gIt_BranCh_aNd_l0g}**
