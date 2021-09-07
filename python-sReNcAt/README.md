파이썬 코드내 yml 폴더내에서 yml 파일을 읽어와 owner와 repo를 판단하여 user를 초대,

멤버삭제의 경우 print('\n\'s not found this member info in users.yml') 라인에 코드추가시 멤버 자동삭제 기능도 추가 구현가능

```yaml
-- yml
    |
    ----- srencat (Owner)
            |
            |
            ------ github-org-member-manage-action (Repo)
                    |
                    |
                    -------- users.yml (https://github.com/sReNcAt/github-org-member-manage-action Repo의 collabo 설정)
```