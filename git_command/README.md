#### Refresh Local Branch from Remote
```bash
git fetch --prune
```

#### Publish New Branch
```bash
git push -u origin branch-name
```

#### Check Remote Branch
```bash
git branch -r
```

#### Rename Main Branch
```bash
# This command works for just-created repo
git branch -M main
```

#### Revoke Previous Commit
```bash
git reset --soft HEAD~1
```

#### Remove Files from Staging
```bash
git rm --cached path/to/large-file
```