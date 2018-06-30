# git-dumb

Have you ever accidentally merged away your diligent local changes and cried tears of frustration??  
Or, are you tired of people stereotyping you as smart just because you're a programmer??  
If so, it's time to **git dumb**.

### Introducing git-dumb, probably the best personal version control system you'll ever find.

It simply backs up different versions of files and nested directories in any directory you use it in. It's designed for coNvEniEnCe: the backups are plopped straight into your same directory and are organized by the time they that they're captured. Did that not make sense? Just try it! I bet it's great for use on sketchy hackathon projects, when you're _moving fast and breaking things_, or when you're just feeling particularly dumb. ¯\\\_(ツ)\_/¯

### How to use:

1.  Download this shit and put git-dumb.py in the same directory as the files and stuff you want to dumbly save.
2.  Run `python3 git-dumb.py` (or something like that) in that same directory.
    Options you can use:

| Option          | What it is                                                                      |
| --------------- | ------------------------------------------------------------------------------- |
| --freq [int]    | Amount of time between saving new versions (in sec). Default: 1800 (30 min)     |
| --timeout [int] | Amount of time to run until git-dumb terminates (in sec). Default: 10800 (3 hr) |
| --dir [String]  | Name of directory where all versions are stored. Default: "versions"            |

3.  Modify files as you please. Enjoy!
