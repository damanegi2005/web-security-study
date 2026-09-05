2. <Reflected XSS into HTML context with nothing encoded>
goal: perform a cross-site scripting attack that calls the alert function 

검색창에 치는대로 다음 화면에 "0 serch result for 'blablabla'" 이렇게 뜸.
개발자도구의 요소 화면을 보면, inject한 html 구문이 기존 행을 벗어나 다음 행에 따로 삽입돼있음.

혹은, 주소창에서도 공격 가능
https://0a7b00fb043d31f3806a3f700099005c.web-security-academy.net/?search=%3Ch1%3Ehi%3C%2Fh1%3E




3. <Stored XSS into HTML context with nothing encoded>
goal: submit a comment that calls the alert function when the blog post is viewed

역시나 개발자도구-요소에서 댓글 부분을 보니, 댓글로 작성한 내용이 <p></p>안에 들어감. 
html에서 <script>를 실행하기 위해 <script>alert(1)</script> 작성.

**reflected xss VS stored xss
reflected: 바로 실행됨
stored: 다른곳에 저장됐다가 실행됨. (ex. 데이터베이스). 
    db에 숨어있다가 수동적으로 지워지기 전까지 이 블로그 접속하는 사람들이 다 희생자됨 ! persistent
     xss라고 불리기도. 쨋든 더 위험해. session(로그인여부같은) 없어도 공격당함

