[portswigger] Username enumeration via different responses
goal: enumerate a valid username, brute-force the user's password, then access their account page.
풀이: Burp Suite Intruder로 brute-force 공격하는것!!!
원하는 인자 intruder로 보내기 -> payloads 구성. candidate list 넣고 공격실행. 

length가 특정 후보만 좀 다름. 걔네가 valid username, password.


[portswigger] 2FA simple bypass
goal: 2FA verification code 없이 Carlos의 account page에 접근해라. 내 credential, carlos의 credential은 주어짐.
풀이: 내 credential로 로그인, email client에서 4자리 코드 입력하여 내 account page(/my-account) 접속. 
carlos로 로그인하여 바로 url에 /my-account 치면 carlos의 account page로 이동~

*Burp는 테스트 환경에서 자체 CA 인증서를 브라우저가 신뢰하도록 구성해서 브라우저 - Burp - 서버 형태로 TLS 연결을 중개함. Burp 내장 브라우저는 이 설정이 미리 되어 있어서 HTTPS 테스트가 바로 가능함.


[portswigger] Password reset broken logic
goal: reset Carlos's password 
풀이: 우선 내 계정의 비번 바꾸기를 시도해. username에 wiener눌러서 change하는 페이지로 이동. 그 페이지에서 new password/ confirm password 아무거나 넣고 send. 를 repeater로 확인해. 거기서 페이로드 수정하면됨.
(password token은 여기선 다행히 아무의미 없던걸로 추정)

*핵심은 어느 페이지를 엿볼거냐를 잘 생각해. 아무래도 비번을 편히 내가 바꿔야하니 비번 바꿔서 보내는 창을 repeater 해야겠지?
